import numpy as np
import pycuda.gpuarray as garray
from .sinogram_cuda import CudaSinoProcessing
from ..utils import get_cuda_srcfile, updiv
from ..cuda.kernel import CudaKernel
try:
    from pypwt import Wavelets
    __have_pypwt__ = True
except ImportError:
    __have_pypwt__ = False
try:
    from skcuda.fft import Plan
    from skcuda.fft import fft as cufft
    from skcuda.fft import ifft as cuifft
    __have_skcuda__ = True
except ImportError:
    __have_skcuda__ = False


def get_minor_version(semver_version):
    return float(".".join(semver_version.split(".")[:2]))

# "Get memory pointer" only available from pypwt 0.9
if __have_pypwt__:
    __pypwt_version__ = get_minor_version(Wavelets.version())
    if __pypwt_version__ < 0.9:
        __have_pypwt__ = False


class CudaMunchDeringer(CudaSinoProcessing):

    def __init__(self, levels, sigma, wname="db15", sinos_shape=None, radios_shape=None, cuda_options=None):
        """
        Cuda implementation of Fourier-Wavelets de-striping method [1].
        Please see the documentation of nabu.preproc.sinogram.SinoProcessing.

        Parameters
        -----------
        levels: int
            Number of Wavelets decomposition levels.
        sigma: float
            Damping factor in the Wavelets domain.
        wname: str, optional
            Wavelets name

        """
        if not(__have_pypwt__ and __have_skcuda__):
            raise ValueError("Needs pypwt and scikit-cuda to use this class")
        super().__init__(sinos_shape=sinos_shape, radios_shape=radios_shape, cuda_options=cuda_options)
        self._init_wavelets(levels, sigma, wname)
        self._init_fft()
        self._setup_fw_kernel()

    def _init_fft(self):
        self._fft_plans = {}
        for level, d_vcoeff in self._d_vertical_coeffs.items():
            n_angles, dwidth = d_vcoeff.shape
            # Batched vertical 1D FFT - need advanced data layout
            # http://docs.nvidia.com/cuda/cufft/#advanced-data-layout
            p_f = Plan(
                (n_angles,),
                np.float32, np.complex64,
                batch=dwidth,
                inembed=np.int32([0]),
                istride=dwidth,
                idist=1,
                onembed=np.int32([0]),
                ostride=dwidth,
                odist=1
            )
            p_i = Plan(
                (n_angles,),
                np.complex64, np.float32,
                batch=dwidth,
                inembed=np.int32([0]),
                istride=dwidth,
                idist=1,
                onembed=np.int32([0]),
                ostride=dwidth,
                odist=1
            )
            self._fft_plans[level] = {"forward": p_f, "inverse": p_i}

    def _init_wavelets(self, levels, sigma, wname):
        self.sigma = float(sigma)
        self.sino_shape = self.sinos_shape[1:]
        self.cudwt = Wavelets(np.zeros(self.sino_shape, "f"), wname, levels)
        # Access memory allocated by "pypwt" from pycuda
        self._d_sino = garray.empty(self.sino_shape, np.float32, gpudata=self.cudwt.image_int_ptr())
        self._get_vertical_coeffs()

    def _get_vertical_coeffs(self):
        self._d_vertical_coeffs = {}
        self._d_sino_f = {}
        # Transfer the (0-memset) coefficients in order to get all the shapes
        coeffs = self.cudwt.coeffs
        for i in range(self.cudwt.levels):
            shape = coeffs[i+1][1].shape
            self._d_vertical_coeffs[i+1] = garray.empty(
                shape,
                np.float32,
                gpudata=self.cudwt.coeff_int_ptr(3*i+2)
            )
            self._d_sino_f[i+1] = garray.zeros(
                (shape[0]//2+1, shape[1]),
                dtype=np.complex64
            )


    def _setup_fw_kernel(self):
        self._fw_kernel = CudaKernel(
            "kern_fourierwavelets",
            filename=get_cuda_srcfile("fourier_wavelets.cu"),
            signature="Piif",
        )


    def destripe_munch(self, d_sino, output=None):
        # set the "image" for DWT (memcpy D2D)
        self._d_sino.set(d_sino)
        # perform forward DWT
        self.cudwt.forward()
        for i in range(self.cudwt.levels):
            level = i + 1
            d_coeffs = self._d_vertical_coeffs[level]
            d_sino_f = self._d_sino_f[level]
            Ny, Nx = d_coeffs.shape
            # Batched FFT along axis 0
            cufft(
                d_coeffs,
                d_sino_f,
                self._fft_plans[level]["forward"]
            )
            # Dampen the wavelets coefficients
            self._fw_kernel(d_sino_f, Nx, Ny, self.sigma)
            # IFFT
            cuifft(
                d_sino_f,
                d_coeffs,
                self._fft_plans[level]["inverse"]
            )
        # Finally, inverse DWT
        self.cudwt.inverse()
        if output is None:
            output = d_sino
        output.set(self._d_sino)
        return output

