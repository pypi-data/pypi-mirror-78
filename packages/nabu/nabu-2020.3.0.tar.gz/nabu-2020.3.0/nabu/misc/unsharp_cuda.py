from ..cuda.utils import __has_pycuda__
from ..cuda.convolution import Convolution
from ..cuda.processing import CudaProcessing
from .unsharp import UnsharpMask
if __has_pycuda__:
    import pycuda.gpuarray as garray
    from pycuda.elementwise import ElementwiseKernel

class CudaUnsharpMask(UnsharpMask, CudaProcessing):
    def __init__(self, shape, sigma, coeff, mode="reflect", method="gaussian",
                 cuda_options=None):
        """
        Unsharp Mask, cuda backend.
        """
        cuda_options = cuda_options or {}
        CudaProcessing.__init__(self, **cuda_options)
        UnsharpMask.__init__(self, shape, sigma, coeff, mode=mode, method=method)
        self._init_convolution()
        self._init_mad_kernel()
        self._init_arrays_to_none(["_d_out"])


    def _init_convolution(self):
        self.convolution = Convolution(
            self.shape,
            self._gaussian_kernel,
            mode=self.mode,
            extra_options={ # Use the lowest amount of memory
                "allocate_input_array": False,
                "allocate_output_array": False,
                "allocate_tmp_array": True,
            }
        )

    def _init_mad_kernel(self):
        # garray.GPUArray.mul_add is out of place...
        self.mad_kernel = ElementwiseKernel(
            "float* array, float fac, float* other, float otherfac",
            "array[i] = fac * array[i] + otherfac * other[i]",
            name="mul_add"
        )

    def unsharp(self, image, output=None):
        if output is None:
            self._allocate_array("_d_out", self.shape, "f")
            output = self._d_out
        self.convolution(image, output=output)
        if self.method == "gaussian":
            self.mad_kernel(output, -self.coeff, image, 1. + self.coeff)
        else: # log
            self.mad_kernel(output, self.coeff, image, 1.)
        return output
