import pandas

__author__ = "Jayaram Kancherla"
__copyright__ = "jkanche"
__license__ = "mit"

def create_parser_object(format, source, columns=None):
    """Create appropriate File class based on file format

    Args:
        format (str): format of file
        source (str): location of file

    Returns:
        An instance of parser class
    """  
    
    from .BigBed import BigBed
    from .BigWig import BigWig
    from .SamFile import SamFile
    from .BamFile import BamFile
    from .TbxFile import TbxFile
    from .GtfFile import GtfFile
    from .GWASBigBedPval import GWASBigBedPval
    from .GWASBigBedPIP import GWASBigBedPIP
    from .InteractionBigBed import InteractionBigBed
    from .TileDB import TileDB
    from .TranscriptTbxFile import TranscriptTbxFile

    req_manager = {
        "bigwig": BigWig,
        "bw": BigWig,
        "bigbed": BigBed,
        "bb": BigBed,
        "sam": SamFile,
        "bam": BamFile,
        "tbx": TbxFile,
        "tabix": TbxFile,
        "gtf": GtfFile,
        "gwas": GWASBigBedPval,
        "gwas_pip": GWASBigBedPIP,
        "tiledb": TileDB,
        "interaction_bigbed": InteractionBigBed,
        "transcript": TranscriptTbxFile
    }
    
    return req_manager[format.lower()](source, columns)

def toDataFrame(records, header = None):
    input = pandas.DataFrame(records, columns=header)
    return input