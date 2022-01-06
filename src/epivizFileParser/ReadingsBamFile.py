# import pysam
# import numpy
from .BamFile import BamFile
from .utils import toDataFrame

__author__ = "Jayaram Kancherla, Victor Alexandru"
__copyright__ = "jkanche"
__license__ = "mit"


class ReadingsBamFile(BamFile):
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
            self.columns = ["chr", "name", "start", "length"]
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

        reads = []

        try:
            for read in self.file.fetch(chr, start, end):
                # for future ref
                # .get_blocks()  # the actual broken segments seen in ivg
                # .reference_start - .reference_end

                reads.append((
                    read.reference_name,  # chr
                    read.query_name,  # read name
                    read.reference_start,
                    read.reference_length  # actual length with gaps
                ))

            self.get_col_names()

            if respType == "DataFrame":
                result = toDataFrame(reads, self.columns)

        except ValueError as e:
            result = toDataFrame(reads, self.get_col_names())
            return result, "Invalid input. (chr, start, end)"
        except Exception as e:
            result = toDataFrame(reads, self.get_col_names())
            return result, str(e)

        return result, None
