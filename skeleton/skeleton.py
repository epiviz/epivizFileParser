from .utils import toDataFrame
import pandas as pd

__author__ = "Jayaram Kancherla"
__copyright__ = "jkanche"
__license__ = "mit"

# If the class is a derivative of bigbed/bigwig format, use the BaseClass 
# BaseClass also provides several convenience methods to make file requests to local
# or remote files
class NewFileParser(object):
    """
    Class to parse `NewFileParser` files 

    Args:
        file (str): file location can be local (full path) or hosted publicly (http or s3)
        columns ([str]) : names for columns in file
    """
    def __init__(self, file, columns=None):
        self.fileSrc = file
        self.columns = columns

    def getRange(self, chr, start, end, bins=2000, zoomlvl=-1, metric="AVG", respType = "DataFrame"):
        """Get data for a given genomic location

        Args:
            chr (str): chromosome 
            start (int): genomic start
            end (int): genomic end
            respType (str): result format type, default is "DataFrame

        Returns:
            result
                a DataFrame with matched regions from the input genomic location if respType is DataFrame else result is an array
            error 
                if there was any error during the process
        """
        result = None
        error = None
        # <YOUR FUNC HERE>

        return (result, error)