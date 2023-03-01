from .BigBed import BigBed
import struct
import zlib
import math
import pandas as pd

class GuideBigBed(BigBed):
    """
    BigBed file parser for Guide tracks

    Columns in the bed file are 

        (chr, start, end, name, score, strand,
        pamStart, pamEnd, cutSite, Spacer)
    
    Args: 
        file (str): InteractionBigBed file location
    """
    magic = "0x8789F2EB"
    def __init__(self, file, columns=["chr", "start", "end", "name", "score", "strand",
        "pamStart", "pamEnd", "cutSite", "spacer"]):
        self.colFlag = False
        print("init guide bigbed")
        super(GuideBigBed, self).__init__(file, columns=columns)
        print(self.columns)

    def getRange(self, chr, start, end, bins=2000, zoomlvl=-1, metric="AVG", respType = "DataFrame", treedisk=None):
        result, _ = super(GuideBigBed, self).getRange(chr, start, end, bins, zoomlvl = -2, metric=metric, respType=respType, treedisk=treedisk)
        print(result)
        return result, _
