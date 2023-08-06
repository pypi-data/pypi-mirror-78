from silx.utils.enum import Enum

"""
The following structure define the allowed values for certain parameters.
There are two structures:
  - One mapping between "user parameters" and canonical name
  - One Enum for canonical names
"""

phase_retrieval_methods = {
    "": None,
    "none": None,
    "paganin": "paganin",
    "tie": "paganin",
    "ctr": "CTR",
}

class PhaseRetrievalMethod(Enum):
    PAGANIN = "paganin"
    CTR = "CTR"
    NONE = None

padding_modes = {
    "edges": "edge",
    "edge": "edge",
    "mirror": "mirror",
    "zeros": "zeros",
    "zero": "zeros",
}

class PaddingMode(Enum):
    EDGE = "edge"
    MIRROR = "mirror"
    ZEROS = "zeros"

reconstruction_methods = {
    "fbp": "FBP",
    "none": None,
    "": None
}

class ReconstructionMethod(Enum):
    FBP = "FBP"
    NONE = None

fbp_filters = {
    "ramlak": "ramlak",
    "ram-lak": "ramlak",
    "none": None,
    "": None,
}

class FBPFilter(Enum):
    RAMLAK = "ramlak"
    NONE = None


iterative_methods = {
    "tv": "TV",
    "wavelets": "wavelets",
    "l2": "L2",
    "ls": "L2",
    "sirt": "SIRT",
    "em": "EM",
}
class IterativeMethod(Enum):
    TV = "TV"
    WAVELETS = "wavelets"
    SIRT = "SIRT"
    L2 = "L2"
    EM = "EM"

optim_algorithms = {
    "chambolle": "chambolle-pock",
    "chambollepock": "chambolle-pock",
    "fista": "fista",
}
class OptimAlgorithm(Enum):
    CHAMBOLLEPOCK = "chambolle-pock"
    FISTA = "fista"

files_formats = {
    "h5": "hdf5",
    "hdf5": "hdf5",
    "nexus": "hdf5",
    "nx": "hdf5",
    "npy": "npy",
    "npz": "npz",
    "tif": "tiff",
    "tiff": "tiff",
    "jp2": "jp2",
    "jp2k": "jp2",
    "j2k": "jp2",
    "jpeg2000": "jp2",
}
class FileFormat(Enum):
    EDF = "edf"
    HDF5 = "hdf5"
    NPY = "npy"
    NPZ = "npz"
    TIFF = "tiff"
    JP2 = "jp2"


distribution_methods = {
    "local": "local",
    "slurm": "slurm",
    "": "local",
    "preview": "preview",
}
class DistributionMethod(Enum):
    LOCAL = "local"
    SLURM = "slurm"
    PREVIEW = "preview"

log_levels = {
    "0": "error",
    "1": "warning",
    "2": "info",
    "3": "debug",
}
class LogLevel(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
