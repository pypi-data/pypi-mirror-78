import re

# Parser functions


def parse_starlog(path_to_log):
    """Parse star logfile into a dict.
    Args:
        path_to_log: filepath containing the star run log
    Returns:
        dict that contains metrics from star log
    """
    qc_dict = {}
    with open(path_to_log) as f:
        for line in f:
            if "|" in line:
                tokens = line.split("|")
                qc_dict[tokens[0].strip()] = tokens[1].strip()
    return qc_dict


# format pergentage points


def percentage_to_float(line):
    return float(line.strip("%"))


def convert_string_with_commas_to_int(number_string):
    """Convert string of format xyz,tuv representing an int into an int.
    Args:
        number_string: str representing an int
    Returns:
        int represented by the number_string
    """
    return int(re.sub(",", "", number_string))


def try_converting_to_numeric(value):
    """Try converting to numeric.
    Attempts to convert to int, and if that fails, to float
    and as a last resort keep as str.
    Args:
        value: str input value from qc
    Returns:
        value converted to numeric if applicable.
    """
    assert type(value) == str
    try:
        converted_value = int(value)
    except ValueError:
        try:
            converted_value = float(value)
        except ValueError:
            converted_value = value
    return converted_value


def parse_flagstats(filePath):
    """Parse samtools flagstat file into a dict
    Args:
        filePath: path to samtools flagstat file
    Returns:
        dict that contains metrics from flagstats
    """
    pairs = {}
    numbers_type = int
    with open(filePath, "r") as fh:
        while True:
            line = fh.readline()
            if line is None:
                break
            line.strip()
            if line == "":
                continue
            # 2826233 + 0 in total (QC-passed reads + QC-failed reads)
            if line.find("QC-passed reads") > 0:
                # 2826233 + 0 in total (QC-passed reads + QC-failed reads)
                parts = line.split()
                pairs["total"] = numbers_type(parts[0])
                pairs["total_qc_failed"] = numbers_type(parts[2])
            # 0 + 0 duplicates
            elif line.find("duplicates") > 0:
                parts = line.split()
                pairs["duplicates"] = numbers_type(parts[0])
                pairs["duplicates_qc_failed"] = numbers_type(parts[2])
            # 2826233 + 0 mapped (100.00%:-nan%)
            elif "mapped" not in pairs and line.find("mapped") > 0:
                parts = line.split()
                pairs["mapped"] = numbers_type(parts[0])
                pairs["mapped_qc_failed"] = numbers_type(parts[2])
                val = parts[4][1:].split(":")[0]
                pairs["mapped_pct"] = percentage_to_float(val)
            # 2142 + 0 paired in sequencing
            elif line.find("paired in sequencing") > 0:
                parts = line.split()
                if int(parts[0]) <= 0:  # Not paired-end, so nothing more needed
                    break
                pairs["paired"] = numbers_type(parts[0])
                pairs["paired_qc_failed"] = numbers_type(parts[2])
            # 107149 + 0 read1
            elif line.find("read1") > 0:
                parts = line.split()
                pairs["read1"] = numbers_type(parts[0])
                pairs["read1_qc_failed"] = numbers_type(parts[2])
            # 107149 + 0 read2
            elif line.find("read2") > 0:
                parts = line.split()
                pairs["read2"] = numbers_type(parts[0])
                pairs["read2_qc_failed"] = numbers_type(parts[2])
            # 2046 + 0 properly paired (95.48%:-nan%)
            elif line.find("properly paired") > 0:
                parts = line.split()
                pairs["paired_properly"] = numbers_type(parts[0])
                pairs["paired_properly_qc_failed"] = numbers_type(parts[2])
                val = parts[5][1:].split(":")[0]
                pairs["paired_properly_pct"] = percentage_to_float(val)
            # 0 + 0      singletons (0.00%:-nan%)
            elif line.find("singletons") > 0:
                parts = line.split()
                pairs["singletons"] = numbers_type(parts[0])
                pairs["singletons_qc_failed"] = numbers_type(parts[2])
                val = parts[4][1:].split(":")[0]
                pairs["singletons_pct"] = percentage_to_float(val)
            # 2046212 + 0 with itself and mate mapped
            elif line.find("with itself and mate mapped") > 0:
                parts = line.split()
                pairs["with_itself"] = numbers_type(parts[0])
                pairs["with_itself_qc_failed"] = numbers_type(parts[2])
            # 0 + 0 with mate mapped to a different chr (mapQ>=5)
            elif line.find("with mate mapped to a different chr") > 0:
                parts = line.split()
                pairs["diff_chroms"] = numbers_type(parts[0])
                pairs["diff_chroms_qc_failed"] = numbers_type(parts[2])
                break
    return pairs


def parse_key_value_tsv(path_to_tsv, sep=None):
    """Parse 2-column tsv file with string key, valuetype value into a dict.
    Args:
        path_to_tsv: path to file containing the tsv
        sep: column separator String, default: None (will split on any whitespace)
    Raises:
        AssertionError if a row that splits into number of tokens other than 2
    """
    qc_dict = {}
    with open(path_to_tsv) as f:
        for line in f:
            tokens = line.split(sep)
            assert len(tokens) == 2
            qc_dict[tokens[0]] = try_converting_to_numeric(tokens[1])
    return qc_dict


def parse_illumina_trimstats(path_to_trimstats):
    """Parse illumina trimstats into a dict.
    Args:
        path_to_trimstats: path to file that contains illumina trimstats
    Returns:
        dict with trimstats qc metrics
    Raises:
        AssertionError if a row that splits into number of tokens other than 2
        ValueError if some value is not suitable for converting into int
    """
    qc_dict = {}
    with open(path_to_trimstats) as f:
        rawstats = f.readline()
    tokens = rawstats.split(";")
    qc_dict["Total read-pairs processed"] = int(tokens[0].split()[-1])
    qc_dict["Total read-pairs trimmed"] = int(tokens[1].split()[-1])
    return qc_dict


def parse_bamcounts(path_to_bamcounts):
    """Parse bamcounts into a dict.
    Args:
        path_to_bamcounts: path to file that contains bamcounts/tagcounts
    Returns:
        dict with bamcounts qc metrics
    Raises:
        AssertionError if a row that splits into number of tokens other than 2
    """
    return parse_key_value_tsv(path_to_bamcounts)


def parse_preseq_targets(path_to_preseq_targets):
    """Parse preseq targets into a dict.
    Args:
        path_to_preseq_targets: path to file that contains preeq targets
    Returns:
        dict with preseq targets qc metrics
    Raises:
        AssertionError if a row that splits into number of tokens other than 2
    """
    return parse_key_value_tsv(path_to_preseq_targets)


def parse_hotspot1_spot_score(path_to_hotspot1_spot_score):
    """Parse hotspot1 spot score into a dict.
    Args:
        path_to_hotspot1_spot_score: path to file that contains hotspot1 spot score
    Returns:
        dict with hotspot1 spot score qc metrics
    """
    qc_dict = {}
    with open(path_to_hotspot1_spot_score) as f:
        next(f)
        raw_values = f.readline()
    values = raw_values.strip().split()
    qc_dict["# of read tags provided"] = try_converting_to_numeric(values[0])
    qc_dict["# of read tags that were in hotspots"] = try_converting_to_numeric(
        values[1]
    )
    qc_dict["SPOT1 score"] = try_converting_to_numeric(values[2])
    return qc_dict


def parse_picard_metrics(path_to_metrics):
    """Parse picard metrics into a dict.
    Args:
        path_to_metrics: path to a file that contains picard etrics
    Returns:
        dict with picard metrics
    """
    qc_dict = {}
    with open(path_to_metrics) as f:
        lines = []
        for _ in range(8):
            lines.append(f.readline())
    keys = lines[6].split("\t")
    values = lines[7].split("\t")
    keys = [key.strip() for key in keys]
    values = [value.strip() for value in values]
    for key, value in zip(keys, values):
        qc_dict[key] = try_converting_to_numeric(value)
    return qc_dict


def parse_picard_duplication_metrics(path_to_duplication_metrics):
    """Parse picard duplication metrics into a dict.
    Args:
        path_to_duplication_metrics: path to a file that contains picard duplication metrics
    Returns:
        dict with picard duplication metrics
    """
    raw_metrics = parse_picard_metrics(path_to_duplication_metrics)
    encode_formatted_metrics = {}
    encode_formatted_metrics["Estimated Library Size"] = raw_metrics.get(
        "ESTIMATED_LIBRARY_SIZE"
    )
    encode_formatted_metrics["Percent duplication"] = raw_metrics.get(
        "PERCENT_DUPLICATION"
    )
    encode_formatted_metrics["Read Pair Duplicates"] = raw_metrics.get(
        "READ_PAIR_DUPLICATES"
    )
    encode_formatted_metrics["Read Pair Optical Duplicates"] = raw_metrics.get(
        "READ_PAIR_OPTICAL_DUPLICATES"
    )
    encode_formatted_metrics["Read Pairs Examined"] = raw_metrics.get(
        "READ_PAIRS_EXAMINED"
    )
    encode_formatted_metrics["Unpaired Reads Examined"] = raw_metrics.get(
        "UNPAIRED_READS_EXAMINED"
    )
    encode_formatted_metrics["Reads examined"] = (
        encode_formatted_metrics["Read Pairs Examined"]
        + encode_formatted_metrics["Unpaired Reads Examined"]
    )
    encode_formatted_metrics["Unmapped Reads"] = raw_metrics.get("UNMAPPED_READS")
    encode_formatted_metrics["Unpaired Read Duplicates"] = raw_metrics.get(
        "UNPAIRED_READ_DUPLICATES"
    )
    encode_formatted_metrics["Read duplicates"] = (
        encode_formatted_metrics["Read Pair Duplicates"]
        + encode_formatted_metrics["Unpaired Read Duplicates"]
    )

    return encode_formatted_metrics


def parse_picard_insert_size_metrics(path_to_insert_size_metrics):
    """Parse picard insert size metrics into a dict.
    Args:
        path_to_insert_size_metrics: path to a file that contains picard insert size metrics
    Returns:
        dict with picard insert size metrics
    """
    return parse_picard_metrics(path_to_insert_size_metrics)


def parse_insert_size_info(path_to_insert_size_info):
    return parse_key_value_tsv(path_to_insert_size_info)


def parse_samtools_stats(path_to_samtools_stats):
    """Parse samtools stats metrics into a dict.
    Args:
        path_to_samtools_stats: path to a file that contains samtools stats metrics
    Returns:
        dict with samtools stats metrics
    """
    with open(path_to_samtools_stats) as f:
        stats_lines = [
            line.split("\t") for line in f.readlines() if line.startswith("SN")
        ]
    raw_stats = {
        line[1].strip(":"): try_converting_to_numeric(line[2]) for line in stats_lines
    }
    encode_formatted_stats = {}
    encode_formatted_stats["1st fragments"] = raw_stats.get("1st fragments")
    encode_formatted_stats["Average length"] = raw_stats.get("average length")
    encode_formatted_stats["Average quality"] = raw_stats.get("average quality")
    encode_formatted_stats["# of bases duplicated"] = raw_stats.get("bases duplicated")
    encode_formatted_stats["# of bases mapped"] = raw_stats.get("bases mapped")
    encode_formatted_stats["# of bases mapped (cigar)"] = raw_stats.get(
        "bases mapped (cigar)"
    )
    encode_formatted_stats["# of bases trimmed"] = raw_stats.get("bases trimmed")
    encode_formatted_stats["Error rate"] = raw_stats.get("error rate")
    encode_formatted_stats["# of filtered sequences"] = raw_stats.get(
        "filtered sequences"
    )
    encode_formatted_stats["Average insert size"] = raw_stats.get("insert size average")
    encode_formatted_stats["SD of insert size"] = raw_stats.get(
        "insert size standard deviation"
    )
    encode_formatted_stats["# of inward oriented pairs"] = raw_stats.get(
        "inward oriented pairs"
    )
    encode_formatted_stats["Is sorted flag"] = raw_stats.get("is sorted")
    encode_formatted_stats["Last fragments"] = raw_stats.get("last fragments")
    encode_formatted_stats["Maximum length"] = raw_stats.get("maximum length")
    encode_formatted_stats["# of mismatches"] = raw_stats.get("mismatches")
    encode_formatted_stats["# of non-primary alignments"] = raw_stats.get(
        "non-primary alignments"
    )
    encode_formatted_stats["# of outward oriented pairs"] = raw_stats.get(
        "outward oriented pairs"
    )
    encode_formatted_stats["# of pairs on diff chr"] = raw_stats.get(
        "pairs on different chromosomes"
    )
    encode_formatted_stats["# pairs with other orientation"] = raw_stats.get(
        "pairs with other orientation"
    )
    encode_formatted_stats["# of total raw sequences"] = raw_stats.get(
        "raw total sequences"
    )
    encode_formatted_stats["# of reads MQ0"] = raw_stats.get("reads MQ0")
    encode_formatted_stats["# of reads failing QC"] = raw_stats.get("reads QC failed")
    encode_formatted_stats["# of duplicated reads"] = raw_stats.get("reads duplicated")
    encode_formatted_stats["# of reads mapped"] = raw_stats.get("reads mapped")
    encode_formatted_stats["# of reads mapped and paired"] = raw_stats.get(
        "reads mapped and paired"
    )
    encode_formatted_stats["# reads paired"] = raw_stats.get("reads paired")
    encode_formatted_stats["# of properly paired reads"] = raw_stats.get(
        "reads properly paired"
    )
    encode_formatted_stats["# of unmapped reads"] = raw_stats.get("reads unmapped")
    encode_formatted_stats["# of sequences"] = raw_stats.get("sequences")
    encode_formatted_stats["Total length"] = raw_stats.get("total length")

    return encode_formatted_stats


def parse_cutadapt_trimstats(path_to_cutadapt_trimstats):
    """Parse cutadapt trimstats metrics into a dict.
    Args:
        path_to_cutadapt_trimstats: path to a file that contains cutadapt trimstats metrics
    Returns:
        dict with cutadapts trimstats metrics
    """
    qc_dict = {}
    with open(path_to_cutadapt_trimstats) as f:
        trimstats_lines = f.readlines()
    qc_dict["Total read pairs processed"] = convert_string_with_commas_to_int(
        trimstats_lines[7].split()[-1]
    )
    qc_dict["Read 1 with adapter"] = convert_string_with_commas_to_int(
        trimstats_lines[8].split()[-2]
    )
    qc_dict["Read 2 with adapter"] = convert_string_with_commas_to_int(
        trimstats_lines[9].split()[-2]
    )
    return qc_dict
