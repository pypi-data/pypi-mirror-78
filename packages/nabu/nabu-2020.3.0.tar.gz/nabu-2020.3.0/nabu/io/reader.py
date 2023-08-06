import os
from typing import Union, Any
import numpy as np
from tomoscan.io import HDF5File
from .utils import get_compacted_dataslices
from ..misc.binning import get_binning_function
from ..utils import subsample_dict

try:
    from silx.third_party.EdfFile import EdfFile
except ImportError:
    EdfFile = None


class Reader(object):
    """
    Abstract class for various file readers.
    """

    def __init__(self, sub_region=None):
        """
        Parameters
        ----------
        sub_region: tuple, optional
            Coordinates in the form (start_x, end_x, start_y, end_y), to read
            a subset of each frame. It can be used for Regions of Interest (ROI).
            Indices start at zero !
        """
        self._set_default_parameters(sub_region)

    def _set_default_parameters(self, sub_region):
        self._set_subregion(sub_region)

    def _set_subregion(self, sub_region):
        self.sub_region = sub_region
        if sub_region is not None:
            start_x, end_x, start_y, end_y = sub_region
            self.start_x = start_x
            self.end_x = end_x
            self.start_y = start_y
            self.end_y = end_y
        else:
            self.start_x = 0
            self.end_x = None
            self.start_y = 0
            self.end_y = None


    def get_data(self, data_url):
        """
        Get data from a silx.io.url.DataUrl
        """
        raise ValueError("This should be implemented by inheriting class")


    def release(self):
        """
        Release the file if needed.
        """
        pass





class NPReader(Reader):

    multi_load = True

    def __init__(self, sub_region=None, mmap=True):
        """
        Reader for NPY/NPZ files. Mostly used for internal development.
        Please refer to the documentation of nabu.io.reader.Reader
        """
        super().__init__(sub_region=sub_region)
        self._file_desc = {}
        self._set_mmap(mmap)

    def _set_mmap(self, mmap):
        self.mmap_mode = "r" if mmap else None

    def _open(self, data_url):
        file_path = data_url.file_path()
        file_ext = self._get_file_type(file_path)
        if file_ext == "npz":
            if file_path not in self._file_desc:
                self._file_desc[file_path] = np.load(file_path, mmap_mode=self.mmap_mode)
            data_ref = self._file_desc[file_path][data_url.data_path()]
        else:
            data_ref = np.load(file_path, mmap_mode=self.mmap_mode)
        return data_ref

    @staticmethod
    def _get_file_type(fname):
        if fname.endswith(".npy"):
            return "npy"
        elif fname.endswith(".npz"):
            return "npz"
        else:
            raise ValueError("Not a numpy file: %s" % fname)

    def get_data(self, data_url):
        data_ref = self._open(data_url)
        data_slice = data_url.data_slice()
        if data_slice is None:
            res = data_ref[self.start_y:self.end_y, self.start_x:self.end_x]
        else:
            res = data_ref[data_slice, self.start_y:self.end_y, self.start_x:self.end_x]
        return res

    def release(self):
        for fname, fdesc in self._file_desc.items():
            if fdesc is not None:
                fdesc.close()
                self._file_desc[fname] = None

    def __del__(self):
        self.release()


class EDFReader(Reader):

    multi_load = False # not implemented

    def __init__(self, sub_region=None):
        """
        A class for reading series of EDF Files.
        Multi-frames EDF are not supported.
        """
        if EdfFile is None:
            raise ImportError("Need EdfFile to use this reader")
        super().__init__(sub_region=sub_region)

    def read(self, fname):
        E = EdfFile(fname, "r")
        if self.sub_region is not None:
            data = E.GetData(
                0,
                Pos=(self.start_x, self.start_y),
                Size=(self.end_x - self.start_x, self.end_y - self.start_y),
            )
        else:
            data = E.GetData(0)
        E.File.close()
        return data

    def get_data(self, data_url):
        return self.read(data_url.file_path())



class HDF5Reader(Reader):

    multi_load = True

    def __init__(self, sub_region=None):
        """
        A class for reading a HDF5 File.
        """
        super().__init__(sub_region=sub_region)
        self._file_desc = {}


    def _open(self, file_path):
        if file_path not in self._file_desc:
            self._file_desc[file_path] = HDF5File(file_path, "r", swmr=True)


    def get_data(self, data_url):
        file_path = data_url.file_path()
        self._open(file_path)
        h5dataset = self._file_desc[file_path][data_url.data_path()]
        data_slice = data_url.data_slice()
        if data_slice is None:
            res = h5dataset[self.start_y:self.end_y, self.start_x:self.end_x]
        else:
            res = h5dataset[data_slice, self.start_y:self.end_y, self.start_x:self.end_x]
        return res

    def release(self):
        for fname, fdesc in self._file_desc.items():
            if fdesc is not None:
                try:
                    fdesc.close()
                    self._file_desc[fname] = None
                except Exception as exc:
                    print("Error while closing %s: %s" % (fname, str(exc)))

    def __del__(self):
        self.release()



Readers = {
    "edf": EDFReader,
    "hdf5": HDF5Reader,
    "h5": HDF5Reader,
    "nx": HDF5Reader,
    "npz": NPReader,
    "npy": NPReader,
}



class ChunkReader(object):
    """
    A reader of chunk of images.
    """

    def __init__(
        self,
        files,
        sub_region: Union[tuple, None] = None,
        pre_allocate=True,
        data_buffer=None,
        convert_float=False,
        shape=None,
        dtype=None,
        binning=None,
        dataset_subsampling=None
    ):
        """
        Initialize a "ChunkReader". A chunk is a stack of images.

        Parameters
        ----------
        files: dict
            Dictionary where the key is the file/data index, and the value is a
            silx.io.url.DataUrl pointing to the data.
            The dict must contain only the files which shall be used !
            Note: the shape and data type is infered from the first data file.
        sub_region: tuple, optional
            If provided, this must be a tuple in the form
            (start_x, end_x, start_y, end_y). Each image will be cropped to this
            region. This is used to specify a chunk of files.
            Each of the parameters can be None, in this case the default start
            and end are taken in each dimension.
        pre_allocate: bool
            Whether to pre-allocate data before reading.
        data_buffer: array-like, optional
            If `pre_allocate` is set to False, this parameter has to be provided.
            It is an array-like object which will hold the data.
        convert_float: bool
            Whether to convert data to float32, regardless of the input data type.
        shape: tuple, optional
            Shape of each image. If not provided, it is inferred from the first image
            in the collection.
        dtype: `numpy.dtype`, optional
            Data type of each image. If not provided, it is inferred from the first image
            in the collection.
        binning: int or tuple of int, optional
            Whether to bin the data. If multi-dimensional binning is done,
            the parameter must be in the form (binning_x, binning_y).
            Each image will be binned by these factors.
        dataset_subsampling: int, optional
            Whether to subsample the dataset. If an integer `n` is provided,
            then one image out of `n` will be read.

        Notes
        ------
        The files are provided as a collection of `silx.io.DataURL`. The file type
        is inferred from the extension.

        Binning is different from subsampling. Using binning will not speed up
        the data retrieval (quite the opposite), since the whole (subregion of) data
        is read and then binning is performed.
        """
        self._set_files(files)
        self._get_reader_class()
        self._get_shape_and_dtype(shape, dtype, binning, dataset_subsampling)
        self._set_subregion(sub_region)
        self._init_reader()
        self._loaded = False
        self.convert_float = convert_float
        if convert_float:
            self.out_dtype = np.float32
        else:
            self.out_dtype = self.dtype
        if not((data_buffer is not None) ^ (pre_allocate is True)):
            raise ValueError("Please provide either 'data_buffer' or 'pre_allocate'")
        self.files_data = data_buffer
        if data_buffer is not None:
            # overwrite out_dtype
            self.out_dtype = data_buffer.dtype
            if data_buffer.shape != self.shape:
                raise ValueError("Expected shape %s but got %s" % (self.shape, data_buffer.shape))
        if pre_allocate:
            self.files_data = np.zeros(self.chunk_shape, dtype=self.out_dtype)
        if (self.binning is not None) and (np.dtype(self.out_dtype).kind in ["u", "i"]):
            raise ValueError("Output datatype cannot be integer when using binning. Please set the 'convert_float' parameter to True or specify a 'data_buffer'.")


    def _set_files(self, files):
        if len(files) == 0:
            raise ValueError("Expected at least one data file")
        self.n_files = len(files)
        self.files = files
        self._sorted_files_indices = sorted(files.keys())
        self._fileindex_to_idx = dict.fromkeys(self._sorted_files_indices)


    def _infer_file_type(self):
        fname = self.files[self._sorted_files_indices[0]].file_path()
        ext = os.path.splitext(fname)[-1].replace(".", "")
        if ext not in Readers:
            raise ValueError(
                "Unknown file format %s. Supported formats are: %s"
                % (ext, str(Readers.keys()))
            )
        return ext

    def _get_reader_class(self):
        ext = self._infer_file_type()
        reader_class = Readers[ext]
        self._reader_class = reader_class


    def _get_shape_and_dtype(self, shape, dtype, binning, dataset_subsampling):
        if shape is None or dtype is None:
            shape, dtype = self._infer_shape_and_dtype()
        assert len(shape) == 2, "Expected the shape of an image (2-tuple)"
        self.shape_total = shape
        self.dtype = dtype
        self._set_binning(binning)
        self.dataset_subsampling = dataset_subsampling
        if dataset_subsampling is not None and dataset_subsampling > 1:
            self.n_files //= dataset_subsampling
            if not(self._reader_class.multi_load):
                # 3D loading not supported for this reader.
                # Data is loaded frames by frame, so subsample directly self.files
                self.files = subsample_dict(self.files, dataset_subsampling)
                self._sorted_files_indices = sorted(self.files.keys())
                self._fileindex_to_idx = dict.fromkeys(self._sorted_files_indices)

    def _infer_shape_and_dtype(self):
        self._reader_entire_image = self._reader_class()
        first_file_dataurl = self.files[self._sorted_files_indices[0]]
        first_file_data = self._reader_entire_image.get_data(first_file_dataurl)
        return first_file_data.shape, first_file_data.dtype

    def _set_subregion(self, sub_region):
        sub_region = sub_region or (None, None, None, None)
        start_x, end_x, start_y, end_y = sub_region
        if start_x is None:
            start_x = 0
        if start_y is None:
            start_y = 0
        if end_x is None:
            end_x = self.shape_total[1]
        if end_y is None:
            end_y = self.shape_total[0]
        self.sub_region = (start_x, end_x, start_y, end_y)
        self.shape = (end_y - start_y, end_x - start_x)
        if self.binning is not None:
            self.shape = (self.shape[0] // self.binning[1], self.shape[1] // self.binning[0])
        self.chunk_shape = (self.n_files,) + self.shape

    def _init_reader(self):
        # instantiate reader with user params
        self.file_reader = self._reader_class(
            sub_region=self.sub_region
        )


    def _set_binning(self, binning):
        if binning is None:
            self.binning = None
            return
        if np.isscalar(binning):
            binning = (binning, binning)
        else:
            assert len(binning) == 2, "Expected binning in the form (binning_x, binning_y)"
        if binning[0] == 1 and binning[1] == 1:
            self.binning = None
            return
        for b in binning:
            if int(b) != b:
                raise ValueError("Expected an integer number for binning values, but got %s" % binning)
            # Current limitation
            if b not in [1, 2, 3]:
                raise NotImplementedError("Currently, binning can only be 2 or 3 in each dimension")
            #
        self.binning = binning
        binning_function = get_binning_function(binning[::-1]) # user provides (binning_x, binning_y)
        if binning_function is None:
            raise NotImplementedError("Binning factor %s is not implemented yet" % str(binning))
        self.binning_function = binning_function


    def get_data(self, file_url):
        """
        Get the data associated to a file url.
        """
        arr = self.file_reader.get_data(file_url)
        if self.binning is not None:
            if arr.ndim == 2:
                arr = self.binning_function(arr)
            else:
                nz = arr.shape[0]
                res = np.zeros((nz, ) + self.binning_function(arr[0]).shape, dtype="f")
                for i in range(nz):
                    res[i] = self.binning_function(arr[i])
                arr = res
        return arr


    def _load_single(self):
        for i, fileidx in enumerate(self._sorted_files_indices):
            file_url = self.files[fileidx]
            self.files_data[i] = self.get_data(file_url)
            self._fileindex_to_idx[fileidx] = i


    def _load_multi(self):
        urls_compacted = get_compacted_dataslices(self.files, subsampling=self.dataset_subsampling)
        loaded = {}
        data = []
        start_idx = 0
        for idx in self._sorted_files_indices:
            url = urls_compacted[idx]
            url_str = str(url)
            is_loaded = loaded.get(url_str, False)
            if is_loaded:
                continue
            ds = url.data_slice()
            delta_z = ds.stop - ds.start
            if ds.step is not None and ds.step > 1:
                delta_z //= ds.step
            end_idx = start_idx + delta_z
            self.files_data[start_idx:end_idx] = self.get_data(url)
            start_idx += delta_z
            loaded[url_str] = True


    def load_files(self, overwrite: bool=False):
        """
        Load the files whose links was provided at class instantiation.

        Parameters
        -----------
        overwrite: bool, optional
            Whether to force reloading the files if already loaded.
        """
        if self._loaded and not(overwrite):
            raise ValueError("Radios were already loaded. Call load_files(overwrite=True) to force reloading")
        if self.file_reader.multi_load:
            self._load_multi()
        else:
            self._load_single()
        self._loaded = True



