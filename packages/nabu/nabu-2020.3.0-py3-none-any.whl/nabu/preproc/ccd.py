import os
from typing import Union, Any
from bisect import bisect_left
import numpy as np
from ..resources.validators import convert_to_bool_noerr
from ..io.reader import ChunkReader
from ..utils import check_supported

try:
    from scipy.ndimage.filters import median_filter

    __have_scipy__ = True
except ImportError:
    __have_scipy__ = False
    from ..utils import median2 as nabu_median_filter



class CCDProcessing(object):
    """
    A base class for processing taking place in the "radios" domain.
    This base class does not "fill" memory on its own (it merely stores references
    to arrays).
    """
    def __init__(self, radios_shape: tuple):
        """
        Initialize a CCDProcessing instance.

        Parameters
        -----------
        radios_shape: tuple
            A tuple describing the shape of the radios stack, in the form
            `(n_radios, n_z, n_x)`.
        """
        self._set_radios_shape(radios_shape)

    def _set_radios_shape(self, radios_shape):
        if len(radios_shape) == 2:
            self.radios_shape = (1, ) + radios_shape
        elif len(radios_shape) == 3:
            self.radios_shape = radios_shape
        else:
            raise ValueError("Expected radios to have 2 or 3 dimensions")
        n_radios, n_z, n_x = self.radios_shape
        self.n_radios = n_radios
        self.n_angles = n_radios
        self.shape = (n_z, n_x)


    def _take_logarithm(self, radios, clip_min=None, clip_max=None):
        if (clip_min is not None) or (clip_max is not None):
            np.clip(radios, clip_min, clip_max, out=radios)
            np.log(radios, out=radios)
        else:
            np.log(radios, out=radios)
        radios[:] *= -1;
        return radios



class FlatField(CCDProcessing):
    """
    A class for flat-field normalization
    """

    _supported_interpolations = ["linear", "nearest"]

    def __init__(
        self,
        radios_shape: tuple,
        flats: dict,
        darks: dict,
        radios_indices=None,
        interpolation: str = "linear",
        **chunk_reader_kwargs
    ):
        """
        Initialize a flat-field normalization process.

        Parameters
        ----------
        radios_shape: tuple
            A tuple describing the shape of the radios stack, in the form
            `(n_radios, n_z, n_x)`.
        flats: dict
            Dictionary where the key is the flat index, and the value is a
            silx.io.DataUrl pointing to the flat.
        darks: dict
            Dictionary where the key is the dark index, and the value is a
            silx.io.DataUrl pointing to the dark.
        radios_indices: array, optional
            Array containing the radios indices. `radios_indices[0]` is the index
            of the first radio, and so on.
        interpolation: str, optional
            Interpolation method for flat-field. See below for more details.

        Tip
        -----
        The other named parameters are passed to ChunkReader(). Please read its
        documentation for more information.

        Notes
        ------
        Usually, when doing a scan, only one or a few darks/flats are acquired.
        However, the flat-field normalization has to be performed on each radio,
        although incoming beam can fluctuate between projections.
        The usual way to overcome this is to interpolate between flats.
        If interpolation="nearest", the first flat is used for the first
        radios subset, the second flat is used for the second radios subset,
        and so on.
        If interpolation="linear", the normalization is done as a linear
        function of the radio index.
        """
        self._set_parameters(radios_shape, flats, darks, radios_indices, interpolation)
        self._init_readers(chunk_reader_kwargs)
        self._load_flats()
        self._load_darks()


    def _check_frames(self, frames, frames_type, min_frames_required, max_frames_supported):
        if len(frames) < min_frames_required:
            raise ValueError("Need at least %d %s" % (min_frames_required, frames_type))
        if len(frames) > max_frames_supported:
            raise ValueError(
                "Flat-fielding with more than %d %s is not supported"
                % (max_frames_supported, frames_type)
            )

    def _set_parameters(self, radios_shape, flats, darks, radios_indices, interpolation):
        self._set_radios_shape(radios_shape)
        self._check_frames(flats, "flats", 1, 9999)
        self._check_frames(darks, "darks", 1, 1)
        self.flats = flats
        self.darks = darks
        if radios_indices is None:
            radios_indices = np.arange(0, self.n_radios, dtype=np.int32)
        else:
            radios_indices = np.array(radios_indices, dtype=np.int32)
            assert radios_indices.size == self.n_radios
        self.radios_indices = radios_indices
        self.interpolation = interpolation
        check_supported(
            interpolation, self._supported_interpolations, "Interpolation mode"
        )


    def _init_readers(self, chunk_reader_kwargs):
        """
        Initialize file readers for flat/darks
        """
        self.flats_reader = ChunkReader(self.flats, **chunk_reader_kwargs)
        self.darks_reader = ChunkReader(self.darks, **chunk_reader_kwargs)

    def _load_flats(self):
        self.n_flats = len(self.flats)
        self.flats_arr = {}
        for flat_idx, flat_url in self.flats.items():
            self.flats_arr[flat_idx] = self.flats_reader.get_data(flat_url)
        self._sorted_flat_indices = sorted(self.flats.keys())
        self._flat2arrayidx = {k: v for k, v in zip(self._sorted_flat_indices, np.arange(self.n_flats))}

    def _load_darks(self):
        self.n_darks = len(self.darks)
        self.darks_arr = {}
        for dark_idx, dark_url in self.darks.items():
            self.darks_arr[dark_idx] = self.darks_reader.get_data(dark_url)
        self._sorted_dark_indices = sorted(self.darks.keys())

    @staticmethod
    def get_previous_next_indices(arr, idx):
        pos = bisect_left(arr, idx)
        if pos == len(arr): # outside range
            return (arr[-1], )
        if arr[pos] == idx:
            return (idx,)
        if pos == 0:
            return (arr[0], )
        return arr[pos - 1], arr[pos]

    @staticmethod
    def get_nearest_index(arr, idx):
        pos = bisect_left(arr, idx)
        if arr[pos] == idx:
            return idx
        return arr[pos - 1] if idx - arr[pos - 1] < arr[pos] - idx else arr[pos]

    def _get_flat_linear(self, idx, dtype=np.float32):
        prev_next = self.get_previous_next_indices(self._sorted_flat_indices, idx)
        if len(prev_next) == 1:  # current index corresponds to an acquired flat
            flat_data = self.flats_arr[prev_next[0]]
        else:  # interpolate
            prev_idx, next_idx = prev_next
            flat_data_prev = self.flats_arr[prev_idx]
            flat_data_next = self.flats_arr[next_idx]
            delta = next_idx - prev_idx
            w1 = 1 - (idx - prev_idx) / delta
            w2 = 1 - (next_idx - idx) / delta
            flat_data = w1 * flat_data_prev + w2 * flat_data_next
        if flat_data.dtype != dtype:
            flat_data = np.ascontiguousarray(flat_data, dtype=dtype)
        return flat_data

    def _get_flat_nearest(self, idx, dtype=np.float32):
        idx0 = self.get_nearest_index(self._sorted_flat_indices, idx)
        flat_arr = self.flats_arr[idx0]
        if flat_arr.dtype != dtype:
            flat_arr = np.ascontiguousarray(flat_arr, dtype=dtype)
        return flat_arr

    def get_flat(self, idx, dtype=np.float32):
        """
        Get flat file corresponding to the corresponding index.
        If no flat file was acquired at this index, an interpolated flat
        is returned.
        """
        if self.interpolation == "linear":
            return self._get_flat_linear(idx, dtype=dtype)
        if self.interpolation == "nearest":
            return self._get_flat_nearest(idx, dtype=dtype)
        return None

    def normalize_radios(self, radios):
        """
        Apply a flat-field correction, with the current parameters, to a stack
        of radios.
        The processing is done in-place, meaning that the radios content is overwritten.

        Parameters
        -----------
        radios: numpy.ndarray
            Radios chunk
        """
        first_dark_idx = self._sorted_dark_indices[0]
        dark = np.ascontiguousarray(
            self.darks_arr[first_dark_idx], dtype=np.float32
        )
        for i, idx in enumerate(self.radios_indices):
            radio_data = radios[i]
            flat = self.get_flat(idx)
            radios[i] = (radio_data - dark) / (flat - dark)
        return radios



class CCDCorrection(CCDProcessing):
    """
    A base class for processings applied on radios.
    It is designed to handle chunks of radios (see the documentation for more
    information on the radios chunk concept).
    """

    _supported_ccd_corrections = ["median_clip"]

    def __init__(
        self,
        radios_shape: tuple,
        correction_type: str="median_clip",
        median_clip_thresh: float = 0.1,
    ):
        """
        Initialize a CCDCorrection instance.

        Parameters
        -----------
        radios_shape: tuple
            A tuple describing the shape of the radios stack, in the form
            `(n_radios, n_z, n_x)`.
        correction_type: str
            Correction type for radios ("median_clip", "sigma_clip", ...)
        median_clip_thresh: float, optional
            Threshold for the median clipping method.

        Notes
        ------
        A CCD correction is a process (usually filtering) taking place in the
        radios space.
        Available filters:
           - median_clip: if the value of the current pixel exceeds the median
             of adjacent pixels (a 3x3 neighborhood) more than a threshold,
             then this pixel value is set to the median value.
        """
        super().__init__(radios_shape)
        check_supported(
            correction_type, self._supported_ccd_corrections, "CCD correction mode"
        )
        self.correction_type = correction_type
        self.median_clip_thresh = median_clip_thresh


    @staticmethod
    def median_filter(img):
        if __have_scipy__:
            return median_filter(img, (3, 3), mode="reflect")
        else:
            return nabu_median_filter(img)

    def median_clip_mask(self, img, return_medians=False):
        """
        Compute a mask indicating whether a pixel is valid or not, according to
        the median-clip method.

        Parameters
        ----------
        img: numpy.ndarray
            Input image
        return_medians: bool, optional
            Whether to return the median values additionally to the mask.
        """
        median_values = self.median_filter(img)
        invalid_mask = img >= median_values + self.median_clip_thresh
        if return_medians:
            return invalid_mask, median_values
        else:
            return invalid_mask

    def median_clip_correction(self, radio, output=None):
        """
        Compute the median clip correction on one image.

        Parameters
        ----------
        radios: numpy.ndarray, optional
            A radio image.
        output: numpy.ndarray, optional
            Output array
        """
        assert radio.shape == self.shape
        if output is None:
            output = np.copy(radio)
        else:
            output[:] = radio[:]
        invalid_mask, medians = self.median_clip_mask(radio, return_medians=True)
        output[invalid_mask] = medians[invalid_mask]
        return output



class Log(CCDProcessing):
    """
    Helper class to take -log(radios)
    """
    def __init__(self, radios_shape, clip_min=None, clip_max=None):
        super().__init__(radios_shape)
        self.clip_min = clip_min
        self.clip_max = clip_max


    def take_logarithm(self, radios):
        """
        Take the negative logarithm of a radios chunk.

        Parameters
        -----------
        radios: `pycuda.gpuarray.GPUArray`
            Radios chunk
            If not provided, a new GPU array is created.
        clip_min: float, optional
            Before taking the logarithm, the values are clipped to this minimum.
        clip_max: float, optional
            Before taking the logarithm, the values are clipped to this maximum.
        """
        self._take_logarithm(radios, clip_min=self.clip_min, clip_max=self.clip_max)
        return radios

