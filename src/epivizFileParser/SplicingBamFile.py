# import pysam
# import numpy
from .BamFile import BamFile
from .utils import toDataFrame

__author__ = "Jayaram Kancherla, Victor Alexandru"
__copyright__ = "jkanche"
__license__ = "mit"


class SplicingBamFile(BamFile):
    """
    Class to parse bam files 

    Args:
        file (str): file location can be local (full path) or hosted publicly
        columns ([str]) : names of columns in the bam file

    Attributes:
        file: a pysam file object
        fileSrc: location of the file
        cacheData: cache of accessed data in memory
        columns: column names
    """

    def __init__(self, file, columns=None):
        super().__init__(file, columns)

    def get_col_names(self):
        """
        Columns of a bam file
        """
        if self.columns is None:
            self.columns = ["chr", "region1_start", "region2_start",
                            "region1_end", "region2_end", "value"]
        return self.columns

    def _get_junctions(self, chr, start, end):
        # iter = self.file.fetch(chr, start, end)
        iter = self.file.pileup(
            chr,
            start,
            end,
            truncate=True,
        )

        reads_set = set()
        reads_refs = []

        for pileupcolumn in iter:
            for pileupread in pileupcolumn.pileups:
                _name = pileupread.alignment.query_name

                if _name in reads_set:
                    pass
                else:
                    reads_set.add(_name)
                    reads_refs.append(pileupread.alignment)

        junctions = {}

        for read in reads_refs:
            # print(read.query_name)

            if read.cigartuples is None:
                # Skipping read with no CIGAR string
                continue

            cigar_string = read.cigarstring
            cigar = read.cigartuples

            if ("N" in cigar_string) and (cigar_string.count("N") > 1):
                # Skipping read with multiple junctions crossed
                continue

            # Check if the read contains an insertion (I)
            # or deletion (D) -- if so, skip it
            skip = False
            for cigar_tuple in cigar:
                if cigar_tuple[0] == 1 or cigar_tuple[1] == 2:
                    # skip = True # possible typo by yarden
                    break
            if skip:
                continue

            aligned_positions = read.get_reference_positions()

            for i, value in enumerate(aligned_positions):
                if value < start or value > end:
                    continue

                try:
                    # if there is a junction coming up
                    if aligned_positions[i+1] > value + 1:
                        leftss = value+1
                        rightss = aligned_positions[i+1]+1

                        if leftss > start and leftss < end and \
                                rightss > start and rightss < end:
                            jxn = ":".join(map(str, [leftss, rightss]))

                            try:
                                junctions[jxn] += 1
                            except:
                                junctions[jxn] = 1
                except:
                    pass

        # convert to proper format
        junction_list = []
        for key, value in junctions.items():
            _start, _end = key.split(":")
            _start = int(_start)
            _end = int(_end)
            junction_list.append((chr, _start-1, _end, _start, _end+1, value))

        return junction_list

    def getRange(self, chr, start, end, bins=2000, zoomlvl=-1, metric="AVG", respType="DataFrame"):
        """
        Get data for a genomic location

        Args:
            chr (str): chromosome 
            start (int): genomic start
            end (int): genomic end
            respType (str): result format type, default is "DataFrame

        Returns:
            a tuple of 
            result
                a DataFrame with matched regions from the input genomic location if respType is DataFrame else result is an array
            error 
                if there was any error during the process
        """
        coverage = []
        junctions = []

        if "chr" in chr:
            alternate_chr = chr.split('chr')[1]
            index_statistics = self.file.get_index_statistics()

            for record in index_statistics:
                if record.contig == alternate_chr:
                    chr = alternate_chr

        try:
            # coverage columns
            self.columns = None
            self.columns = super().get_col_names()
            coverage = super().getRange(chr, start, end)[0]

            _junctions = self._get_junctions(chr, start, end)

            self.columns = None
            self.get_col_names()

            if respType == "DataFrame":
                junctions = toDataFrame(_junctions, self.columns)
        except Exception as e:
            self.columns = None
            coverage = toDataFrame(coverage, super().get_col_names())
            self.columns = None
            junctions = toDataFrame(junctions, self.get_col_names())
            return (coverage, junctions), str(e)

        return (coverage, junctions), None
