# -*- coding: utf-8 -*-
"""Core logic for computing subtrees."""

# standard library imports
import contextlib
import os
import sys
from collections import Counter
from collections import OrderedDict
from datetime import datetime
from itertools import chain
from itertools import combinations
from pathlib import Path

# third-party imports
import click
import dask.bag as db
import networkx as nx
import numpy as np
import pandas as pd
from Bio import SeqIO
from dask.diagnostics import ProgressBar

# first-party imports
import sh
from loguru import logger

# module imports
from . import cli
from . import click_loguru
from .common import cluster_set_name
from .common import fasta_records
from .common import get_paths_from_file
from .common import homo_degree_dist_filename
from .common import protein_file_stats_filename
from .common import protein_properties_filename
from .common import write_tsv_or_parquet
from .protein import Sanitizer

# global constants
NAME = "azulejo"
STATFILE_SUFFIX = f"-{NAME}_stats.tsv"
ANYFILE_SUFFIX = f"-{NAME}_ids-any.tsv"
ALLFILE_SUFFIX = f"-{NAME}_ids-all.tsv"
CLUSTFILE_SUFFIX = f"-{NAME}_clusts.tsv"
SEQ_FILE_TYPE = "fasta"
UNITS = {
    "Mb": {"factor": 1, "outunits": "MB"},
    "Gb": {"factor": 1024, "outunits": "MB"},
    "s": {"factor": 1, "outunits": "s"},
    "m": {"factor": 60, "outunits": "s"},
    "h": {"factor": 3600, "outunits": "s"},
}
SEQ_IN_LINE = 6
IDENT_STATS_LINE = 7
FIRST_LOG_LINE = 14
LAST_LOG_LINE = 23
STAT_SUFFIXES = ["size", "mem", "time", "memory"]
RENAME_STATS = {
    "throughput": "throughput_seq_s",
    "time": "CPU_time",
    "max_size": "max_cluster_size",
    "avg_size": "avg_cluster_size",
    "min_size": "min_cluster_size",
    "seqs": "unique_seqs",
    "singletons": "singleton_clusters",
}
ID_SEPARATOR = "."
IDENT_LOG_MIN = -3
IDENT_LOG_MAX = 0
DEFAULT_STEPS = 16

FASTA_EXT_LIST = [".faa", ".fa", ".fasta"]
FAA_EXT = "faa"

# Classes
class ElapsedTimeReport:

    """Report time elapsed since last invocation."""

    def __init__(self, name):
        """Set name and start time of phase."""
        self.start_time = datetime.now()
        self.name = name

    def elapsed(self, next_name):
        """Return elapsed time in this phase and start a new one."""
        now = datetime.now()
        seconds = (now - self.start_time).total_seconds()
        report = f"{self.name} phase took {seconds:.1f} seconds"
        self.start_time = now
        self.name = next_name
        return report


def read_synonyms(filepath):
    """Read a file of synonymous IDs into a dictionary."""
    synonym_dict = {}
    try:
        synonym_frame = pd.read_csv(filepath, sep="\t")
    except FileNotFoundError:
        logger.error(f'Synonym tsv file "{filepath}" does not exist')
        sys.exit(1)
    except pd.errors.EmptyDataError:
        logger.error(f'Synonym tsv "{filepath}" is empty')
        sys.exit(1)
    if len(synonym_frame) > 0:
        if "#file" in synonym_frame:
            synonym_frame.drop("#file", axis=1, inplace=True)
        key = list(
            set(("Substr", "Dups")).intersection(set(synonym_frame.columns))
        )[0]
        for group in synonym_frame.groupby("id"):
            synonym_dict[group[0]] = group[1][key]
    return synonym_dict


def parse_usearch_log(filepath, rundict):
    """Parse the usearch log file into a stats dictionary."""
    with filepath.open() as logfile:
        for lineno, line in enumerate(logfile):
            if lineno < FIRST_LOG_LINE:
                if lineno == SEQ_IN_LINE:
                    split = line.split()
                    rundict["seqs_in"] = int(split[0])
                    rundict["singleton_seqs_in"] = int(split[4])
                if lineno == IDENT_STATS_LINE:
                    split = line.split()
                    rundict["max_identical_seqs"] = int(split[6].rstrip(","))
                    rundict["avg_identical_seqs"] = float(split[8])
                continue
            if lineno > LAST_LOG_LINE:
                break
            split = line.split()
            if split:
                stat = split[0].lower()
                if split[1] in STAT_SUFFIXES:
                    stat += "_" + split[1]
                    val = split[2]
                else:
                    val = split[1].rstrip(",")
                # rename poorly-named stats
                stat = RENAME_STATS.get(stat, stat)
                # strip stats with units at the end
                conversion_factor = 1
                for unit in UNITS:
                    if val.endswith(unit):
                        val = val.rstrip(unit)
                        conversion_factor = UNITS[unit]["factor"]
                        stat += "_" + UNITS[unit]["outunits"]
                        break
                # convert string values to int or float where possible
                try:
                    val = int(val)
                    val *= conversion_factor
                except ValueError:
                    try:
                        val = float(val)
                        val *= conversion_factor
                    except ValueError:
                        pass
                rundict[stat] = val


@contextlib.contextmanager
def in_working_directory(path):
    """Change working directory and return to previous wd on exit."""
    original_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_cwd)


def get_fasta_ids(fasta):
    """Get the IDS from a FASTA file."""
    idset = set()
    with fasta.open() as fasta_fh:
        for line in fasta_fh:
            if line.startswith(">"):
                idset.add(line.split()[0][1:])
    return list(idset)


def parse_chromosome(ident):
    """Parse chromosome identifiers."""
    # If ident contains an underscore, work on the
    # last part only (e.g., MtrunA17_Chr4g0009691)
    undersplit = ident.split("_")
    if len(undersplit) > 1:
        ident = undersplit[-1].upper()
        if ident.startswith("CHR"):
            ident = ident[3:]
    # Chromosome numbers are integers suffixed by 'G'
    try:
        chromosome = "Chr" + str(int(ident[: ident.index("G")]))
    except ValueError:
        chromosome = None
    return chromosome


def parse_subids(ident):
    """Parse the subidentifiers from identifiers."""
    subids = ident.split(ID_SEPARATOR)
    subids += [
        chromosome
        for chromosome in [parse_chromosome(ident) for ident in subids]
        if chromosome is not None
    ]
    return subids


def parse_clusters(outdir, delete=True, count_clusters=True, synonyms=None):
    """Parse clusters, counting occurrances."""
    if synonyms is None:
        synonyms = {}
    cluster_list = []
    id_list = []
    degree_list = []
    size_list = []
    degree_counter = Counter()
    any_counter = Counter()
    all_counter = Counter()
    graph = nx.Graph()
    for fasta in outdir.glob("*"):
        cluster_id = int(fasta.name)
        ids = get_fasta_ids(fasta)
        if len(synonyms) > 0:
            syn_ids = set(ids).intersection(synonyms.keys())
            for i in syn_ids:
                ids.extend(synonyms[i])
        n_ids = len(ids)
        degree_list.append(n_ids)
        degree_counter.update({n_ids: 1})
        id_list += ids
        cluster_list += [cluster_id] * n_ids
        size_list += [n_ids] * n_ids
        # Do 'any' and 'all' counters
        id_counter = Counter()
        id_counter.update(
            chain.from_iterable([parse_subids(id) for id in ids])
        )
        if count_clusters:
            any_counter.update(id_counter.keys())
            all_counter.update(
                [id for id in id_counter.keys() if id_counter[id] == n_ids]
            )
        elif n_ids > 1:
            any_counter.update({s: n_ids for s in id_counter.keys()})
            all_counter.update(
                {
                    id: n_ids
                    for id in id_counter.keys()
                    if id_counter[id] == n_ids
                }
            )
        # Do graph components
        graph.add_nodes_from(ids)
        if n_ids > 1:
            edges = combinations(ids, 2)
            graph.add_edges_from(edges, weight=n_ids)
        if delete:
            fasta.unlink()
    if delete:
        outdir.rmdir()
    return (
        graph,
        cluster_list,
        id_list,
        size_list,
        degree_list,
        degree_counter,
        any_counter,
        all_counter,
    )


def prettyprint_float(val, digits):
    """Print a floating-point value in a nice way."""
    format_string = "%." + f"{digits:d}" + "f"
    return (format_string % val).rstrip("0").rstrip(".")


@cli.command()
@click_loguru.init_logger()
@click.argument("seqfile")
@click.option(
    "--identity",
    "-i",
    default=0.0,
    help="Minimum sequence identity (float, 0-1). [default: lowest]",
)
@click.option(
    "--min_id_freq",
    "-m",
    default=0,
    show_default=True,
    help="Minimum frequency of ID components.",
)
@click.option(
    "--delete/--no-delete",
    "-d/-n",
    is_flag=True,
    default=True,
    help="Delete primary output of clustering. [default: delete]",
)
@click.option(
    "--write_ids/--no-write_ids",
    "-w",
    is_flag=True,
    default=False,
    help="Write file of ID-to-clusters. [default: delete]",
)
@click.option(
    "--do_calc/--no-do_calc",
    "-c/-x",
    is_flag=True,
    default=True,
    help="Write file of ID-to-clusters. [default: do_calc]",
)
@click.option(
    "--substrs", help="subpath to file of substrings. [default: none]"
)
@click.option("--dups", help="subpath to file of duplicates. [default: none]")
def homology_cluster(
    seqfile,
    identity,
    delete=True,
    write_ids=False,
    do_calc=True,
    min_id_freq=0,
    substrs=None,
    dups=None,
    cluster_stats=True,
    outname=None,
):
    """Cluster at a global sequence identity threshold."""
    try:
        usearch = sh.Command("usearch")
    except sh.CommandNotFound:
        logger.error("usearch must be installed first.")
        sys.exit(1)
    try:
        inpath, dirpath = get_paths_from_file(seqfile)
    except FileNotFoundError:
        logger.error(f'Input file "{seqfile}" does not exist!')
        sys.exit(1)
    stem = inpath.stem
    dirpath = inpath.parent
    if outname is None:
        outname = cluster_set_name(stem, identity)
    outdir = f"{outname}/"
    logfile = f"{outname}.log"
    outfilepath = dirpath / outdir
    logfilepath = dirpath / logfile
    histfilepath = dirpath / homo_degree_dist_filename(outname)
    gmlfilepath = dirpath / f"{outname}.gml"
    statfilepath = dirpath / f"{outname}-stats.tsv"
    anyfilepath = dirpath / f"{outname}-anyhist.tsv"
    allfilepath = dirpath / f"{outname}-allhist.tsv"
    idpath = dirpath / f"{outname}-ids.tsv"
    if identity == 0.0:
        identity_string = "Minimum"
    else:
        identity_string = f"{prettyprint_float(identity *100, 2)}%"
    logger.info(f'{identity_string} sequence identity cluster "{outname}":')
    if not delete:
        logger.debug(f"Cluster files will be kept in {logfile} and {outdir}")
    if cluster_stats and write_ids:
        logger.debug(
            f"File of cluster ID usage will be written to {anyfilepath} and"
            f" {allfilepath}"
        )
    if not do_calc:
        if not logfilepath.exists():
            logger.error("Previous results must exist, rerun with --do_calc")
            sys.exit(1)
        logger.debug("Using previous results for calculation")
    if min_id_freq:
        logger.debug(
            "Minimum number of times ID's must occur to be counted:"
            f" {min_id_freq}"
        )
    synonyms = {}
    if substrs is not None:
        logger.debug(f"using duplicates in {dirpath / dups}")
        synonyms.update(read_synonyms(dirpath / substrs))
    if dups is not None:
        logger.debug(f"using duplicates in {dirpath/dups}")
        synonyms.update(read_synonyms(dirpath / dups))
    timer = ElapsedTimeReport("usearch")
    if do_calc:
        #
        # Delete previous results, if any.
        #
        if outfilepath.exists() and outfilepath.is_file():
            outfilepath.unlink()
        elif outfilepath.exists() and outfilepath.is_dir():
            for file in outfilepath.glob("*"):
                file.unlink()
        else:
            outfilepath.mkdir()
        #
        # Do the calculation.
        #
        with in_working_directory(dirpath):
            output = usearch(
                [
                    "-cluster_fast",
                    seqfile,
                    "-id",
                    identity,
                    "-clusters",
                    outdir,
                    "-log",
                    logfile,
                ]
            )
            logger.debug(output)
            logger.debug(timer.elapsed("parse"))
    run_stat_dict = OrderedDict([("divergence", 1.0 - identity)])
    parse_usearch_log(logfilepath, run_stat_dict)
    run_stats = pd.DataFrame(
        list(run_stat_dict.items()), columns=["stat", "val"]
    )
    run_stats.set_index("stat", inplace=True)
    write_tsv_or_parquet(run_stats, statfilepath)
    if delete:
        logfilepath.unlink()
    if not cluster_stats:
        file_sizes = []
        file_names = []
        record_counts = []
        logger.debug("Ordering clusters by number of records and size.")
        for fasta_path in outfilepath.glob("*"):
            records, size = fasta_records(fasta_path)
            if records == 1:
                fasta_path.unlink()
                continue
            file_names.append(fasta_path.name)
            file_sizes.append(size)
            record_counts.append(records)
        file_frame = pd.DataFrame(
            list(zip(file_names, file_sizes, record_counts)),
            columns=["name", "size", "seqs"],
        )
        file_frame.sort_values(
            by=["seqs", "size"], ascending=False, inplace=True
        )
        file_frame["idx"] = range(len(file_frame))
        for id, row in file_frame.iterrows():
            (outfilepath / row["name"]).rename(
                outfilepath / f'{row["idx"]}.fa'
            )
        file_frame.drop(["name"], axis=1, inplace=True)
        file_frame.set_index("idx", inplace=True)
        # write_tsv_or_parquet(file_frame, "clusters.tsv")
        # cluster histogram
        cluster_hist = pd.DataFrame(file_frame["seqs"].value_counts())
        cluster_hist.rename(columns={"seqs": "clusters"}, inplace=True)
        cluster_hist.index.name = "n"
        cluster_hist.sort_index(inplace=True)
        total_seqs = sum(file_frame["seqs"])
        n_clusters = len(file_frame)
        cluster_hist["pct_clusts"] = (
            cluster_hist["clusters"] * 100.0 / n_clusters
        )
        cluster_hist["pct_seqs"] = (
            cluster_hist["clusters"] * cluster_hist.index * 100.0 / total_seqs
        )
        cluster_hist.to_csv(
            "cluster_hist.tsv", sep="\t", float_format="%06.3f"
        )
        return n_clusters, run_stats, cluster_hist
    (
        cluster_graph,
        clusters,
        ids,
        sizes,
        unused_degrees,
        degree_counts,
        any_counts,
        all_counts,
    ) = parse_clusters(  # pylint: disable=unused-variable
        outfilepath, delete=delete, synonyms=synonyms
    )
    #
    # Write out list of clusters and ids.
    #
    id_frame = pd.DataFrame.from_dict(
        {
            "id": ids,
            "hom.cluster": pd.array(clusters, dtype=pd.UInt32Dtype()),
            "siz": sizes,
        }
    )
    id_frame.sort_values("siz", ascending=False, inplace=True)
    id_frame = id_frame.reindex(["hom.cluster", "siz", "id",], axis=1)
    id_frame.reset_index(inplace=True)
    id_frame.drop(["index"], axis=1, inplace=True)
    id_frame.to_csv(idpath, sep="\t")
    del ids, clusters, sizes, id_frame
    logger.debug(timer.elapsed("graph"))
    #
    # Write out degree distribution.
    #
    cluster_hist = pd.DataFrame(
        list(degree_counts.items()), columns=["degree", "clusters"]
    )
    cluster_hist.sort_values(["degree"], inplace=True)
    cluster_hist.set_index("degree", inplace=True)
    total_clusters = cluster_hist["clusters"].sum()
    cluster_hist["pct_total"] = (
        cluster_hist["clusters"] * 100.0 / total_clusters
    )
    cluster_hist.to_csv(histfilepath, sep="\t", float_format="%06.3f")
    del degree_counts
    #
    # Do histograms of "any" and "all" id usage in cluster
    #
    hist_value = f"{identity:f}"
    any_hist = pd.DataFrame(
        list(any_counts.items()), columns=["id", hist_value]
    )
    any_hist.set_index("id", inplace=True)
    any_hist.sort_values(hist_value, inplace=True, ascending=False)
    all_hist = pd.DataFrame(
        list(all_counts.items()), columns=["id", hist_value]
    )
    all_hist.set_index("id", inplace=True)
    all_hist.sort_values(hist_value, inplace=True, ascending=False)
    if min_id_freq:
        any_hist = any_hist[any_hist[hist_value] > min_id_freq]
        all_hist = all_hist[all_hist[hist_value] > min_id_freq]
    if write_ids:
        any_hist.to_csv(anyfilepath, sep="\t")
        all_hist.to_csv(allfilepath, sep="\t")
    #
    # Compute cluster stats
    #
    # degree_sequence = sorted([d for n, d in cluster_graph.degree()], reverse=True)
    # degreeCount = Counter(degree_sequence)
    # degree_hist = pd.DataFrame(list(degreeCount.items()),
    #                           columns=['degree', 'count'])
    # degree_hist.set_index('degree', inplace=True)
    # degree_hist.sort_values('degree', inplace=True)
    # degree_hist.to_csv(histfilepath, sep='\t')
    nx.write_gml(cluster_graph, gmlfilepath)
    logger.debug(timer.elapsed("final"))
    return run_stats, cluster_graph, cluster_hist, any_hist, all_hist

@cli.command()
@click_loguru.init_logger()
@click.argument("seqfile")
@click.option(
    "--steps",
    "-s",
    default=DEFAULT_STEPS,
    show_default=True,
    help="# of steps from lowest to highest",
)
@click.option(
    "--min_id_freq",
    "-m",
    default=0,
    show_default=True,
    help="Minimum frequency of ID components.",
)
@click.option(
    "--substrs", help="subpath to file of substrings. [default: none]"
)
@click.option("--dups", help="subpath to file of duplicates. [default: none]")
def cluster_in_steps(seqfile, steps, min_id_freq=0, substrs=None, dups=None):
    """Cluster in steps from low to 100% identity."""
    try:
        inpath, dirpath = get_paths_from_file(seqfile)
    except FileNotFoundError:
        logger.error('Input file "%s" does not exist!', seqfile)
        sys.exit(1)
    stat_path = dirpath / (inpath.stem + STATFILE_SUFFIX)
    any_path = dirpath / (inpath.stem + ANYFILE_SUFFIX)
    all_path = dirpath / (inpath.stem + ALLFILE_SUFFIX)
    logsteps = [1.0] + list(
        1.0 - np.logspace(IDENT_LOG_MIN, IDENT_LOG_MAX, num=steps)
    )
    min_fmt = prettyprint_float(min(logsteps) * 100.0, 2)
    max_fmt = prettyprint_float(max(logsteps) * 100.0, 2)
    logger.info(
        f"Clustering at {steps} levels from {min_fmt}% to {max_fmt}% global"
        " sequence identity"
    )
    stat_list = []
    all_frames = []
    any_frames = []
    for id_level in logsteps:
        (
            stats,
            unused_graph,
            unused_hist,
            any_,
            all_,
        ) = homology_cluster.callback(  # pylint: disable=unused-variable
            seqfile,
            id_level,
            min_id_freq=min_id_freq,
            substrs=substrs,
            dups=dups,
        )
        stat_list.append(stats)
        any_frames.append(any_)
        all_frames.append(all_)
    logger.info(f"Collating results on {seqfile}.")
    #
    # Concatenate and write stats
    #
    stats = pd.DataFrame(stat_list)
    stats.to_csv(stat_path, sep="\t")
    #
    # Concatenate any/all data
    #
    any_ = pd.concat(
        any_frames, axis=1, join="inner", sort=True, ignore_index=False
    )
    any_.to_csv(any_path, sep="\t")
    all_ = pd.concat(
        all_frames, axis=1, join="inner", sort=True, ignore_index=False
    )
    all_.to_csv(all_path, sep="\t")


@cli.command()
@click_loguru.init_logger(logfile=False)
@click.argument("infile")
def clusters_to_histograms(infile):
    """Compute histograms from cluster file."""
    try:
        inpath, dirpath = get_paths_from_file(infile)
    except FileNotFoundError:
        logger.error(f'Input file "{infile}" does not exist!')
        sys.exit(1)
    histfilepath = dirpath / f"{inpath.stem}-sizedist.tsv"
    clusters = pd.read_csv(dirpath / infile, sep="\t", index_col=0)
    cluster_counter = Counter()
    for unused_cluster_id, group in clusters.groupby(
        ["hom.cluster"]
    ):  # pylint: disable=unused-variable
        cluster_counter.update({len(group): 1})
    logger.info(f"Writing to {histfilepath}.")
    cluster_hist = pd.DataFrame(
        list(cluster_counter.items()), columns=["siz", "clusts"]
    )
    total_clusters = cluster_hist["clusts"].sum()
    cluster_hist["%clusts"] = cluster_hist["clusts"] * 100.0 / total_clusters
    cluster_hist["%genes"] = (
        cluster_hist["clusts"] * cluster_hist["siz"] * 100.0 / len(clusters)
    )
    cluster_hist.sort_values(["siz"], inplace=True)
    cluster_hist.set_index("siz", inplace=True)
    cluster_hist.to_csv(histfilepath, sep="\t", float_format="%06.3f")


@cli.command()
@click_loguru.init_logger(logfile=False)
@click.argument("file1")
@click.argument("file2")
def compare_clusters(file1, file2):
    """Compare cluster files."""
    path1 = Path(file1)
    path2 = Path(file2)
    commondir = Path(os.path.commonpath([path1, path2]))
    missing1 = commondir / "notin1.tsv"
    missing2 = commondir / "notin2.tsv"
    clusters1 = pd.read_csv(path1, sep="\t", index_col=0)
    print(f"{len(clusters1):d} members in {file1}")
    clusters2 = pd.read_csv(path2, sep="\t", index_col=0)
    print(f"{len(clusters2):d} members in {file2}")
    ids1 = set(clusters1["id"])
    ids2 = set(clusters2["id"])
    notin1 = pd.DataFrame(ids2.difference(ids1), columns=["id"])
    notin1.sort_values("id", inplace=True)
    notin1.to_csv(missing1, sep="\t")
    notin2 = pd.DataFrame(ids1.difference(ids2), columns=["id"])
    notin2.sort_values("id", inplace=True)
    notin2.to_csv(missing2, sep="\t")
    print("%d ids not in ids1" % len(notin1))
    print("%d ids not in ids2" % len(notin2))
    print(f"{len(clusters1):d} in {file1} after dropping")


def cleanup_fasta(
    set_path,
    fasta_path_or_handle,
    filestem,
    write_fasta=True,
    write_stats=True,
):
    """Sanitize and characterize protein FASTA files."""
    out_sequences = []
    ids = []
    lengths = []
    n_ambigs = []
    m_starts = []
    no_stops = []
    seqs = []
    sanitizer = Sanitizer(filestem)
    if hasattr(fasta_path_or_handle, "read"):
        handle = fasta_path_or_handle
    else:
        handle = fasta_path_or_handle.open("rU")
    with handle:
        for record in SeqIO.parse(handle, SEQ_FILE_TYPE):
            seq = record.seq.upper().tomutable()
            try:
                seq, m_start, no_stop, n_ambig = sanitizer.sanitize(seq)
            except ValueError:  # zero-length sequence after sanitizing
                continue
            seqs.append(str(seq))
            if write_fasta:
                record.seq = seq.toseq()
                out_sequences.append(record)
            ids.append(record.id)
            lengths.append(len(seq))
            n_ambigs.append(n_ambig)
            m_starts.append(m_start)
            no_stops.append(no_stop)
    if write_fasta:
        with (set_path / f"{filestem}.fa").open("w") as output_handle:
            SeqIO.write(out_sequences, output_handle, SEQ_FILE_TYPE)
    properties_frame = pd.DataFrame(
        list(zip(ids, lengths, n_ambigs, m_starts, no_stops, seqs)),
        columns=[
            "ID",
            "prot.len",
            "prot.n_ambig",
            "prot.m_start",
            "prot.no_stop",
            "prot.seq",
        ],
    )
    properties_frame = properties_frame.set_index(["ID"])
    if write_stats:
        propfile_path = set_path / protein_properties_filename(filestem)
        properties_frame.to_csv(propfile_path, sep="\t")
        frame_return = len(properties_frame)
    else:
        propfile_path = None
        frame_return = properties_frame
    return (
        filestem,
        propfile_path,
        frame_return,
        sanitizer.file_stats(),
    )


@cli.command()
@click_loguru.init_logger()
@click_loguru.log_elapsed_time()
@click.argument("setname")
@click.option(
    "--fasta/--no-fasta",
    is_flag=True,
    default=True,
    show_default=True,
    help="Write FASTA output.",
)
@click.argument("fasta_list", nargs=-1, type=click.Path(exists=True))
def prepare_protein_files(
    setname, fasta_list, stemdict=None, fasta=True
):
    """Sanitize and combine protein FASTA files."""
    options = click_loguru.get_global_options()
    set_path = Path(setname)
    set_name = set_path.name
    if stemdict is None or stemdict == ():
        if fasta_list is None or len(fasta_list) < 1:
            logger.error("Empty FASTA_LIST, aborting.")
        stemdict = {}
        for file_path in [Path(p) for p in fasta_list]:
            if file_path.suffix not in FASTA_EXT_LIST:
                logger.error(
                    f"Unrecognized extension {file_path.suffix } in {file_path.name}"
                )
                sys.exit(1)
            stemdict[file_path.name[: -len(FAA_EXT) - 1]] = {
                FAA_EXT: file_path
            }
    if len(stemdict) < 1:
        logger.error("Empty stemdict, aborting.")
        sys.exit(1)
    if set_path.exists() and set_path.is_file():
        set_path.unlink()
    elif not set_path.is_dir():
        logger.info(f'Creating output directory "{set_name}/".')
        set_path.mkdir(parents=True)
    arg_list = []
    for file_stem in stemdict.keys():
        arg_list.append((set_path, stemdict[file_stem][FAA_EXT], file_stem,))
    protein_stats = []
    logger.info(f"Preparing {len(stemdict)} protein FASTA files:")
    for args in arg_list:
        protein_stats.append(cleanup_fasta(*args, write_fasta=fasta))
    file_frame_dict = {}
    propfile_path_dict = {}
    n_seqs = 0
    for frame_id, propfile_path, file_seqs, filestat_dict in protein_stats:
        n_seqs += file_seqs
        file_frame_dict[frame_id] = filestat_dict
        propfile_path_dict[frame_id] = propfile_path
    del protein_stats
    file_frame = pd.DataFrame.from_dict(file_frame_dict).transpose()
    file_frame.sort_values(by=["seqs.n"], ascending=False, inplace=True)
    file_frame["idx"] = range(len(file_frame))
    del file_frame_dict
    logger.info(
        f'{n_seqs} sequences in {len(stemdict)} files in set "{set_name}".'
    )
    file_stats_name = protein_file_stats_filename(set_name)
    logger.debug(f"Writing overall stats to {file_stats_name}")
    file_frame.to_csv(set_path / file_stats_name, sep="\t")
    return file_frame, propfile_path_dict


@cli.command()
@click_loguru.init_logger(logfile=False)
@click.argument("infile")
@click.argument("recordfile")
def add_singletons(infile, recordfile):
    """Add singleton clusters to cluster file."""
    clusters = pd.read_csv(
        infile, header=None, names=["hom.cluster", "id"], sep="\t"
    )
    records = pd.read_csv(recordfile, sep="\t")
    id_set = set(records["id"])
    records.drop(["file", "pos"], axis=1, inplace=True)
    records.set_index("id", inplace=True)
    records.drop(["Unnamed: 0"], axis=1, inplace=True)
    len_dict = records.to_dict("id")
    del records
    outfile = "clusters.tsv"
    ids = []
    cluster_ids = []
    sizes = []
    lengths = []
    n_clusters = 0
    grouping = (
        clusters.groupby("hom.cluster").size().sort_values(ascending=False)
    )
    for idx in grouping.index:
        size = grouping.loc[idx]
        cluster = clusters.loc[(clusters["hom.cluster"] == idx)]
        for gene_id in cluster["id"]:
            id_set.remove(gene_id)
            ids.append(gene_id)
            cluster_ids.append(n_clusters)
            sizes.append(size)
            lengths.append(len_dict[gene_id]["len"])
        n_clusters += 1
    logger.info("%s singletons", len(id_set))
    for singleton in id_set:
        cluster_ids.append(n_clusters)
        ids.append(singleton)
        sizes.append(1)
        lengths.append(len_dict[singleton]["len"])
        n_clusters += 1
    cluster_frame = pd.DataFrame(
        list(zip(cluster_ids, ids, sizes, lengths)),
        columns=["hom.cluster", "id", "siz", "len"],
    )
    cluster_frame.to_csv(outfile, sep="\t")


@cli.command()
@click_loguru.init_logger(logfile=False)
@click.argument("infile")
def adjacency_to_graph(infile):
    """Turn adjacency data into GML graph file."""
    gmlfilepath = "synteny.gml"
    clusters = pd.read_csv(infile, sep="\t", index_col=0)
    graph = nx.Graph()
    grouping = (
        clusters.groupby("hom.cluster").size().sort_values(ascending=False)
    )
    for idx in grouping.index:
        # size = grouping.loc[idx]
        cluster = clusters.loc[(clusters["hom.cluster"] == idx)]
        ids = list(cluster["id"])
        #
        # Do graph components
        #
        graph.add_nodes_from(ids)
        if len(ids) > 1:
            edges = combinations(ids, 2)
            graph.add_edges_from(edges, weight=len(ids))
    nx.write_gml(graph, gmlfilepath)


def compute_subclusters(cluster, cluster_size_dict=None):
    """Compute dictionary of per-subcluster stats."""
    subcl_frame = pd.DataFrame(
        [
            {
                "homo_id": i,
                "mean_len": g["len"].mean(),
                "std": g["len"].std(),
                "sub_siz": len(g),
            }
            for i, g in cluster.groupby("link")
        ]
    )
    subcl_frame["link"] = subcl_frame["homo_id"]
    subcl_frame["cont"] = subcl_frame["sub_siz"] == [
        cluster_size_dict[id] for id in subcl_frame["homo_id"]
    ]
    subcl_frame.loc[subcl_frame["cont"], "link"] = pd.NA
    subcl_frame.sort_values(
        ["sub_siz", "std", "mean_len"],
        ascending=[False, True, False],
        inplace=True,
    )
    subcl_frame["sub"] = list(range(len(subcl_frame)))
    subcl_frame.index = list(range(len(subcl_frame)))
    # normalized length is NaN for first element
    subcl_frame["norm"] = [pd.NA] + list(
        subcl_frame["mean_len"][1:] / subcl_frame["mean_len"][0]
    )
    subcl_dict = subcl_frame.set_index("homo_id").to_dict("index")
    #
    # subcluster attributes are done, now copy them into the cluster frame
    #
    for attr in ["norm", "std", "sub_siz", "sub", "link"]:
        cluster[attr] = [subcl_dict[id][attr] for id in cluster["link"]]
    if subcl_frame["cont"].all():
        cluster["cont"] = 1
    else:
        cluster["cont"] = 0
    return cluster


@cli.command()
@click_loguru.init_logger(logfile=False)
@click.option(
    "--first_n",
    default=0,
    show_default=True,
    help="Only process this many clusters.",
)
@click.option(
    "--clust_size",
    default=0,
    show_default=True,
    help="Process only clusters of this size.",
)
@click.argument("synfile")
@click.argument("homofile")
def combine_clusters(first_n, clust_size, synfile, homofile):
    """Combine synteny and homology clusters."""
    options = click_loguru.get_global_options()
    user_options = click_loguru.get_user_global_options()
    parallel = user_options["parallel"]
    timer = ElapsedTimeReport("reading/preparing")
    syn = pd.read_csv(synfile, sep="\t", index_col=0)
    homo = pd.read_csv(homofile, sep="\t", index_col=0)
    homo_id_dict = dict(zip(homo.id, homo.cluster))
    cluster_size_dict = dict(zip(homo.cluster, homo.siz))
    cluster_count = 0
    arg_list = []
    if first_n:
        logger.debug(f"processing only first {first_n:d} clusters")
    if not options.quiet and clust_size:
        logger.info(f"Only clusters of size {clust_size} will be used.")
    syn["link"] = [homo_id_dict[id] for id in syn["id"]]
    for unused_cluster_id, group in syn.groupby(["hom.cluster"]):
        cluster = group.copy()  # copy, so mutable
        clsize = cluster["siz"].iloc[0]
        if clust_size and (clsize != clust_size):
            continue
        if first_n and cluster_count == first_n:
            break
        arg_list.append(cluster)
        cluster_count += 1
    del syn
    if parallel:
        bag = db.from_sequence(arg_list)
    else:
        cluster_list = []
    if not options.quiet:
        logger.info(f"Combining {cluster_count} synteny/homology clusters:")
        ProgressBar().register()
    if parallel:
        cluster_list = bag.map(
            compute_subclusters, cluster_size_dict=cluster_size_dict
        )
    else:
        for clust in arg_list:
            cluster_list.append(compute_subclusters(clust, cluster_size_dict))
    logger.debug(timer.elapsed("concatenating/writing clusters"))
    out_frame = pd.concat(cluster_list)
    out_frame.sort_values(["hom.cluster", "sub"], inplace=True)
    out_frame.index = list(range(len(out_frame)))
    for column in ["sub", "sub_siz"]:
        out_frame[column] = out_frame[column].astype(int)
    out_frame["link"] = out_frame["link"].map(
        lambda x: "" if pd.isnull(x) else f"{x:.0f}"
    )
    out_frame.to_csv(
        "combined.tsv",
        sep="\t",
        columns=[
            "hom.cluster",
            "siz",
            "sub",
            "sub_siz",
            "cont",
            "norm",
            "std",
            "len",
            "link",
            "id",
        ],
        float_format="%.3f",
        index=False,
    )
    logger.debug(timer.elapsed("computing stats"))
    n_fully_contained = len(
        set(out_frame[out_frame["cont"] == 1]["hom.cluster"])
    )
    contained_pct = n_fully_contained * 100.0 / cluster_count
    logger.info(
        f"{n_fully_contained} of {cluster_count}"
        + f" clusters are fully contained ({contained_pct:.1f}%.)"
    )
