import numpy as np
import pycuda.gpuarray as garray
from .sinogram import SinoProcessing
from ..cuda.processing import CudaProcessing
from ..cuda.kernel import CudaKernel
from ..utils import get_cuda_srcfile, updiv


class CudaSinoProcessing(SinoProcessing, CudaProcessing):
    def __init__(self, sinos_shape=None, radios_shape=None, rot_center=None, halftomo=False, cuda_options=None):
        """
        Initialize a CudaSinoProcessing instance.
        Please see the documentation of nabu.preproc.sinogram.SinoProcessing
        and nabu.cuda.processing.CudaProcessing.
        """
        SinoProcessing.__init__(
            self, sinos_shape=sinos_shape, radios_shape=radios_shape, rot_center=rot_center,
            halftomo=halftomo,
        )
        if cuda_options is None:
            cuda_options = {}
        CudaProcessing.__init__(self, **cuda_options)
        self._init_cuda_halftomo()


    def _init_cuda_halftomo(self):
        if not(self.halftomo):
            return
        self.halftomo_kernel = CudaKernel(
            "halftomo_kernel",
            get_cuda_srcfile("halftomo.cu"),
            signature="PPPiii",
        )
        rc = self._rot_center_int
        blk = (32, 32, 1) # tune ?
        self._halftomo_blksize = blk
        self._halftomo_gridsize = (
            updiv(2 * rc, blk[0]),
            updiv(self.n_angles//2, blk[1]),
            1
        )
        d = self.n_x - rc # will have to be adapted for varying axis pos
        self.halftomo_weights = np.linspace(0, 1, d, endpoint=True, dtype="f")
        self.d_halftomo_weights = garray.to_gpu(self.halftomo_weights)


    # Overwrite parent method
    def _radios_to_sinos_simple(self, radios, output, copy=False):
        if not(copy) and output is None:
            return radios.transpose(axes=(1, 0, 2)) # view
        if output is None: # copy and output is None
            na, nz, nx = radios.shape
            output = garray.zeros((nz, na, nx), "f")
        # not(copy) and output is not None
        for i in range(output.shape[0]):
            output[i, :, :] = radios[:, i, :]
        return output



    # Overwrite parent method
    def _radios_to_sinos_halftomo(self, radios, sinos):
        # TODO
        if not(np.isscalar(self.rot_center)):
            raise NotImplementedError("Half tomo with varying rotation axis position is not implemented yet")
        #

        n_a, n_z, n_x = radios.shape
        n_a2 = n_a // 2
        rc = self._rot_center_int
        out_dwidth = 2 * rc
        if sinos is not None:
            if sinos.shape[-1] != out_dwidth:
                raise ValueError(
                    "Expected sinos sinogram last dimension to have %d elements"
                    % out_dwidth
                )
            if sinos.shape[-2] != n_a2:
                raise ValueError("Expected sinograms to have %d angles" % n_a2)
        else:
            sinos = garray.zeros(self.sinos_halftomo_shape, dtype=np.float32)

        for i in range(n_z):
            self.halftomo_kernel(
                radios[:, i, :].copy(), # need to copy this 2D, array otherwise kernel does not work
                sinos[i],
                self.d_halftomo_weights,
                n_a, n_x, rc,
                grid=self._halftomo_gridsize,
                block=self._halftomo_blksize
            )
        return sinos


