import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .BigWig import BigWig
from .BigBed import BigBed
from .GtfParsedFile import GtfParsedFile
from .GWASBigBedPIP import GWASBigBedPIP
from .GWASBigBedPval import GWASBigBedPval
from .S3HDF5File import S3HDF5File
from .TranscriptTbxFile import TranscriptTbxFile
from .SamFile import SamFile
from .BamFile import BamFile
from .TbxFile import TbxFile
from .GtfFile import GtfFile
from .InteractionBigBed import InteractionBigBed
from .TileDB import TileDB