import os
from contextlib import contextmanager
import numpy as np
from time import time
from itertools import product
from silx.utils.enum import Enum as _Enum


def nextpow2(N, dtype=np.int):
    return 2 ** np.ceil(np.log2(N)).astype(dtype)


def previouspow2(N, dtype=np.int):
    return 2 ** np.floor(np.log2(N)).astype(dtype)


def updiv(a, b):
    return (a + (b - 1)) // b


def convert_index(idx, idx_max, default_val):
    """
    Convert an index (possibly negative or None) to a non-negative integer.

    Parameters
    ----------
    idx: int or None
        Index
    idx_max: int
        Maximum value (upper bound) for the index.
    default_val: int
        Default value if idx is None

    Examples
    ---------
    Given an integer `M`, `J = convert_index(i, M, XX)` returns an integer in the
    mathematical range [0, M] (or Python `range(0, M)`). `J` can then be used
    to define an upper bound of a range.
    """
    if idx is None:
        return default_val
    if idx > idx_max:
        return idx_max
    if idx < 0:
        return idx % idx_max
    return idx


def get_folder_path(foldername=""):
    _file_dir = os.path.dirname(os.path.realpath(__file__))
    package_dir = _file_dir
    return os.path.join(package_dir, foldername)


def get_cuda_srcfile(filename):
    src_relpath = os.path.join("cuda", "src")
    cuda_src_folder = get_folder_path(foldername=src_relpath)
    return os.path.join(cuda_src_folder, filename)


def get_resource_file(filename, subfolder=None):
    subfolder = subfolder or []
    relpath = os.path.join("resources", *subfolder)
    abspath = get_folder_path(foldername=relpath)
    return os.path.join(abspath, filename)


def _sizeof(Type):
    """
    return the size (in bytes) of a scalar type, like the C behavior
    """
    return np.dtype(Type).itemsize


def get_ftype(url):
    """
    return supposed filetype of an url
    """
    if hasattr(url, "file_path"):
        return os.path.splitext(url.file_path())[-1].replace(".", "")
    else:
        return os.path.splitext(url)[-1].replace(".", "")


def get_2D_3D_shape(shape):
    if len(shape) == 2:
        return (1, ) + shape
    return shape


def is_device_backend(backend):
    return backend.lower() in ["cuda", "opencl"]


def get_decay(curve, cutoff=1e3, vmax=None):
    """
    Assuming a decreasing curve, get the first point below a certain threshold.

    Parameters
    ----------
    curve: numpy.ndarray
        A 1D array
    cutoff: float, optional
        Threshold. Default is 1000.
    vmax: float, optional
        Curve maximum value
    """
    if vmax is None:
        vmax = curve.max()
    return np.argmax(np.abs(curve) < vmax / cutoff)


def generate_powers():
    """
    Generate a list of powers of [2, 3, 5, 7],
    up to (2**15)*(3**9)*(5**6)*(7**5).
    """
    primes = [2, 3, 5, 7]
    maxpow = {2: 15, 3: 9, 5: 6, 7: 5}
    valuations = []
    for prime in primes:
        # disallow any odd number (for R2C transform), and any number
        # not multiple of 4 (Ram-Lak filter behaves strangely when
        # dwidth_padded/2 is not even)
        minval = 2 if prime == 2 else 0
        valuations.append(range(minval, maxpow[prime]+1))
    powers = product(*valuations)
    res = []
    for pw in powers:
        res.append(np.prod(list(map(lambda x: x[0] ** x[1], zip(primes, pw)))))
    return np.unique(res)


def calc_padding_lengths1D(length, length_padded):
    """
    Compute the padding lengths at both side along one dimension.

    Parameters
    ----------
    length: int
        Number of elements along one dimension of the original array
    length_padded: tuple
        Number of elements along one dimension of the padded array

    Returns
    -------
    pad_lengths: tuple
        A tuple under the form (padding_left, padding_right). These are the
        lengths needed to pad the original array.
    """
    pad_left = (length_padded - length)//2
    pad_right = length_padded - length - pad_left
    return (pad_left, pad_right)


def calc_padding_lengths(shape, shape_padded):
    """
    Multi-dimensional version of calc_padding_lengths1D.
    Please refer to the documentation of calc_padding_lengths1D.
    """
    assert len(shape) == len(shape_padded)
    padding_lengths = []
    for dim_len, dim_len_padded in zip(shape, shape_padded):
        pad0, pad1 = calc_padding_lengths1D(dim_len, dim_len_padded)
        padding_lengths.append((pad0, pad1))
    return tuple(padding_lengths)


# TODO merge with resources.params
class PaddingMode(_Enum):
    ZEROS = 'zeros'
    MEAN = 'mean'
    EDGE = 'edge'
    SYMMETRIC = 'symmetric'
    REFLECT = 'reflect'


def partition_dict(dict_, n_partitions):
    keys = np.sort(list(dict_.keys()))
    res = []
    for keys_arr in np.array_split(keys, n_partitions):
        d = {}
        for key in keys_arr:
            d[key] = dict_[key]
        res.append(d)
    return res


def subsample_dict(dic, subsampling_factor):
    """
    Subsample a dict where keys are integers.
    """
    res = {}
    indices = sorted(dic.keys())
    for i in indices[::subsampling_factor]:
        res[i] = dic[i]
    return res


def check_supported(param_value, available, param_desc):
    if param_value not in available:
        raise ValueError("Unsupported %s '%s'. Available are: %s" % (param_desc, param_value, str(available)))


def check_supported_enum(param_value, enum_cls, param_desc):
    available = enum_cls.values()
    return check_supported(param_value, available, param_desc)


def check_shape(shape, expected_shape, name):
    if shape != expected_shape:
        raise ValueError(
            "Expected %s shape %s but got %s"
            % (name, str(expected_shape), str(shape))
        )


def copy_dict_items(dict_, keys):
    """
    Perform a shallow copy of a subset of a dictionary.
    The subset if done by a list of keys.
    """
    res = {
        key: dict_[key]
        for key in keys
    }
    return res


class PlaceHolder:
    """
    Base class for place holders.
    """

    def __init__(self):
        pass


class DataPlaceHolder(PlaceHolder):
    """
    Placeholder for data-like objects
    """

    def __init__(self):
        super().__init__()


class ArrayPlaceHolder(PlaceHolder):
    """
    Placeholder for array-like objects
    """

    def __init__(self, shape, dtype, name=None):
        self.shape = shape
        self.dtype = np.dtype(dtype)
        self.data = None
        self.name = name

    @property
    def size(self):
        return np.prod(self.shape)

    @property
    def nbytes(self):
        return self.size * self.dtype.itemsize

    def __repr__(self):
        return "ArrayPlaceHolder(shape=%s, dtype=%s)" % (self.shape, self.dtype)


def array_tostring(arr, show_dtype=False):
    """
    Displays an array without displaying its content.
    """
    if isinstance(arr, ArrayPlaceHolder):
        return arr.__repr__()
    attrs = "shape=%s" % (str(arr.shape))
    if show_dtype:
        attrs += ", dtype=%s" % (str(arr.dtype))
    if hasattr(arr, "gpudata"):  # pycuda.gpuarray
        name = "CudaArray"
        attrs += ", data=%s" % str(arr.gpudata)
        if arr.base is not None:
            attrs += ", base=%s" % arr.base.gpudata
    elif hasattr(arr, "queue"):  # pyopencl.array
        name = "OpenclArray"
        attrs += ", data=%s" % str(arr.data)
    else:  # assuming numpy
        name = "NumpyArray"
        attrs += ", data=%s" % hex(arr.ctypes.data)
    return "%s(%s)" % (name, attrs)


# ------------------------------------------------------------------------------
# ------------------------ Image (move elsewhere ?) ----------------------------
# ------------------------------------------------------------------------------


def generate_coords(img_shp, center=None):
    l_r, l_c = float(img_shp[0]), float(img_shp[1])
    R, C = np.mgrid[:l_r, :l_c]  # np.indices is faster
    if center is None:
        center0, center1 = l_r / 2., l_c / 2.
    else:
        center0, center1 = center
    R += 0.5 - center0
    C += 0.5 - center1
    return R, C


def clip_circle(img, center=None, radius=None):
    R, C = generate_coords(img.shape, center)
    M = R**2+C**2
    res = np.zeros_like(img)
    res[M < radius ** 2] = img[M < radius ** 2]
    return res


def extend_image_onepixel(img):
    # extend of one pixel
    img2 = np.zeros((img.shape[0]+2, img.shape[1]+2), dtype=img.dtype)
    img2[0, 1:-1] = img[0]
    img2[-1, 1:-1] = img[-1]
    img2[1:-1, 0] = img[:, 0]
    img2[1:-1, -1] = img[:, -1]
    # middle
    img2[1: -1, 1:-1] = img
    # corners
    img2[0, 0] = img[0, 0]
    img2[-1, 0] = img[-1, 0]
    img2[0, -1] = img[0, -1]
    img2[-1, -1] = img[-1, -1]
    return img2


def median2(img):
    """
    3x3 median filter for 2D arrays, with "reflect" boundary mode.
    Roughly same speed as scipy median filter, but more memory demanding.
    """
    img2 = extend_image_onepixel(img)
    I = np.array([
        img2[0:-2, 0:-2],
        img2[0:-2, 1:-1],
        img2[0:-2, 2:],
        img2[1:-1, 0:-2],
        img2[1:-1, 1:-1],
        img2[1:-1, 2:],
        img2[2:, 0:-2],
        img2[2:, 1:-1],
        img2[2:, 2:]
    ])
    return np.median(I, axis=0)


# ------------------------------------------------------------------------------
# ---------------------------- Decorators --------------------------------------
# ------------------------------------------------------------------------------

_warnings = {}


def measure_time(func):
    def wrapper(*args, **kwargs):
        t0 = time()
        res = func(*args, **kwargs)
        el = time() - t0
        return el, res
    return wrapper


def wip(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        if func_name not in _warnings:
            _warnings[func_name] = 1
            print("Warning: function %s is a work in progress, it is likely to change in the future")
        return func(*args, **kwargs)
    return wrapper


def warning(msg):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            if func_name not in _warnings:
                _warnings[func_name] = 1
                print(msg)
                res = func(*args, **kwargs)
                return res
        return wrapper
    return decorator


#
# Context manager for temporary OS environment
# Found on https://github.com/laurent-laporte-pro/stackoverflow-q2059482
# with the following license:
#
# The MIT License (MIT)

# Copyright (c) 2018 Laurent LAPORTE

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

@contextmanager
def modified_environ(*remove, **update):
    """
    Temporarily updates the ``os.environ`` dictionary in-place.
    The ``os.environ`` dictionary is updated in-place so that the modification
    is sure to work in all situations.
    :param remove: Environment variables to remove.
    :param update: Dictionary of environment variables and values to add/update.
    """
    env = os.environ
    update = update or {}
    remove = remove or []

    # List of environment variables being updated or removed.
    stomped = (set(update.keys()) | set(remove)) & set(env.keys())
    # Environment variables and values to restore on exit.
    update_after = {k: env[k] for k in stomped}
    # Environment variables and values to remove on exit.
    remove_after = frozenset(k for k in update if k not in env)

    try:
        env.update(update)
        [env.pop(k, None) for k in remove]
        yield
    finally:
        env.update(update_after)
        [env.pop(k) for k in remove_after]

