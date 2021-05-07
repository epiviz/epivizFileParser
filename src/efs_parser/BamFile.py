import pysam
from .SamFile import SamFile
from .utils import toDataFrame

__author__ = "Jayaram Kancherla"
__copyright__ = "jkanche"
__license__ = "mit"

class BamFile(SamFile):
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
            self.result.append((self.chr_temp, self.start_temp, self.end_temp, self.value_temp))
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
            self.columns = ["chr", "start", "end", "number of sequence aligned"]
        return self.columns

    def getRange(self, chr, start, end, bins=2000, zoomlvl=-1, metric="AVG", respType = "DataFrame"):
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
            iter = self.file.pileup(chr, start, end)
            self.result = []
            # (result, _) = get_range_helper(self.to_DF, self.get_bin, self.get_col_names, chr, start, end, iter, self.columns, respType)
            result = []
            chrTemp = startTemp = endTemp = valueTemp = None
            for x in iter:
                if valueTemp is None:
                    chrTemp = x.reference_name
                    startTemp = x.reference_pos
                    valueTemp = x.get_num_aligned()
                elif valueTemp is not x.get_num_aligned():
                    result.append((chrTemp, startTemp, endTemp, valueTemp))
                    chrTemp = x.reference_name
                    startTemp = x.reference_pos
                    valueTemp = x.get_num_aligned()

                endTemp = x.reference_pos+1

            columns = self.get_col_names(result[0])

            if respType == "DataFrame":
                result = toDataFrame(result, self.columns)
            return result, None
        except ValueError as e:
            raise Exception("didn't find chromId with the given name")