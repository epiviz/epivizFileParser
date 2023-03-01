import pandas
from scipy import sparse

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
    """

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
    from .GuideTbxFile import GuideTbxFile
    from .GuideBigBed import GuideBigBed

    req_manager = {
        "BigWig": BigWig,
        "bigwig": BigWig,
        "bigWig": BigWig,
        "bw": BigWig,
        "BigBed": BigBed,
        "bigbed": BigBed,
        "bigBed": BigBed,
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
        "transcript": TranscriptTbxFile,
        "guide_tbx": GuideTbxFile,
        "guide": GuideBigBed,
    }
    
    return req_manager[format](source, columns)

def toDataFrame(records, header = None):
    input = pandas.DataFrame(records, columns=header)
    return input

# def toMsgpack(msg):
#     return umsgpack.packb(msg)


def dense_to_sparse(numpy_array, genes):
    csr = sparse.csr_matrix(numpy_array)

    result = {
        "indices": csr.indices.tolist(),
        "indptr": csr.indptr.tolist(),
        "data": csr.data.tolist(),
    }

    return result
