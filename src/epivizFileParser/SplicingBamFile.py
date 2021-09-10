import pysam
import numpy
from .SamFile import SamFile
from .utils import toDataFrame

__author__ = "Jayaram Kancherla"
__copyright__ = "jkanche"
__license__ = "mit"


class SplicingBamFile(SamFile):
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
        self.file = pysam.AlignmentFile(file, "rb")
        self.fileSrc = file
        self.cacheData = {}
        self.columns = columns

    def get_bin(self, x):
        if self.value_temp is not x.get_num_aligned() and self.value_temp is not None:
            self.result.append(
                (self.chr_temp, self.start_temp, self.end_temp, self.value_temp))
            self.value_temp = None

        if self.value_temp is None:
            self.chr_temp = x.reference_name
            self.start_temp = x.reference_pos
            self.value_temp = x.get_num_aligned()

        return (x.reference_name, x.reference_start, x.reference_end, x.query_alignment_sequence, x.query_sequence)

    def to_DF(self, result):
        """
        Transform result into a pandas dataframe
        """
        return toDataFrame(result, self.columns)

    def get_col_names(self, result):
        """
        Columns of a bam file
        """
        if self.columns is None:
            self.columns = ["chr", "region1_start", "region2_start",
                            "region1_end", "region2_end", "value"]
        return self.columns

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
        try:
            iter = self.file.fetch(chr, start, end)

            wiggle = numpy.zeros(end - start + 1)
            junctions = {}

            for read in iter:
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

                    wiggle_index = value - start
                    wiggle[wiggle_index] += 1./read.query_alignment_length

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
                junction_list.append((chr, 0, _end, _start, 0, value))

            self.get_col_names(junction_list[0])

            result = junction_list
            if respType == "DataFrame":
                result = toDataFrame(junction_list, self.columns)
            return result, None
        except ValueError as e:
            return None, "Didn't find chromId with the given name"
        except IndexError as e:
            return None, "No data in given range."
