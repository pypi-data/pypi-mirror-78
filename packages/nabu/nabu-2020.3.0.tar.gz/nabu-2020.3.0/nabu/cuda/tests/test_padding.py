import numpy as np
import pytest
from nabu.cuda.utils import get_cuda_context, __has_pycuda__
from nabu.utils import calc_padding_lengths, get_cuda_srcfile
from nabu.testutils import get_data
if __has_pycuda__:
    import pycuda.gpuarray as garray
    from nabu.cuda.kernel import CudaKernel

scenarios = [
    {
        "shape": (512, 501),
        "shape_padded": (1023, 1022),
        "constant_values": ((1., 2.), (3., 4.)),
    },
]

# parametrize with fixture and "params=" will launch a new class for each scenario.
# the attributes set to "cls" will remain for all the tests done in this class
# with the current scenario.
@pytest.fixture(scope='class', params=scenarios)
def bootstrap(request):
    cls = request.cls
    cls.data = get_data("mri_proj_astra.npz")["data"]
    cls.tol = 1e-7
    cls.params = request.param
    cls.ctx = get_cuda_context()
    cls._calc_pad()
    cls._init_kernels()


@pytest.mark.skipif(not(__has_pycuda__), reason="Need Cuda and pycuda for this test")
@pytest.mark.usefixtures('bootstrap')
class TestPadding:

    @classmethod
    def _calc_pad(cls):
        cls.shape = cls.params["shape"]
        cls.data = np.ascontiguousarray(cls.data[:cls.shape[0], :cls.shape[1]])
        cls.shape_padded = cls.params["shape_padded"]
        ((pt, pb), (pl, pr)) = calc_padding_lengths(cls.shape, cls.shape_padded)
        cls.pad_top_len = pt
        cls.pad_bottom_len = pb
        cls.pad_left_len = pl
        cls.pad_right_len = pr

    @classmethod
    def _init_kernels(cls):
        cls.pad_kern = CudaKernel(
            "padding_constant",
            filename=get_cuda_srcfile("padding.cu"),
            signature="Piiiiiiiiffff",
        )
        cls.pad_edge_kern = CudaKernel(
            "padding_edge",
            filename=get_cuda_srcfile("padding.cu"),
            signature="Piiiiiiii",
        )
        cls.d_data_padded = garray.zeros(cls.shape_padded, "f")

    def _init_padding(self, arr=None):
        arr = arr or self.data
        self.d_data_padded.fill(0)
        Ny, Nx = self.shape
        self.d_data_padded[:Ny, :Nx] = self.data

    def _pad_numpy(self, arr=None, **np_pad_kwargs):
        arr = arr or self.data
        data_padded_ref = np.pad(
            arr,
            ((self.pad_top_len, self.pad_bottom_len), (self.pad_left_len, self.pad_right_len)),
            **np_pad_kwargs
        )
        # Put in the FFT layout
        data_padded_ref = np.roll(
            data_padded_ref,
            (-self.pad_top_len, -self.pad_left_len),
            axis=(0, 1)
        )
        return data_padded_ref

    def test_constant_padding(self):
        self._init_padding()
        # Pad using the cuda kernel
        ((val_top, val_bottom), (val_left, val_right)) = self.params["constant_values"]
        Ny, Nx = self.shape
        Nyp, Nxp = self.shape_padded

        self.pad_kern(
            self.d_data_padded,
            Nx, Ny,
            Nxp, Nyp,
            self.pad_left_len, self.pad_right_len,
            self.pad_top_len, self.pad_bottom_len,
            val_left, val_right, val_top, val_bottom
        )
        # Pad using numpy
        data_padded_ref = self._pad_numpy(
            mode="constant",
            constant_values=self.params["constant_values"]
        )
        # Compare
        errmax = np.max(np.abs(self.d_data_padded.get() - data_padded_ref))
        assert errmax < self.tol, "Max error is too high"

    def test_edge_padding(self):
        self._init_padding()
        # Pad using the cuda kernel
        ((val_top, val_bottom), (val_left, val_right)) = self.params["constant_values"]
        Ny, Nx = self.shape
        Nyp, Nxp = self.shape_padded

        self.pad_edge_kern(
            self.d_data_padded,
            Nx, Ny,
            Nxp, Nyp,
            self.pad_left_len, self.pad_right_len,
            self.pad_top_len, self.pad_bottom_len,
        )
        # Pad using numpy
        data_padded_ref = self._pad_numpy(mode="edge")
        # Compare
        errmax = np.max(np.abs(self.d_data_padded.get() - data_padded_ref))
        assert errmax < self.tol, "Max error is too high"

