import numpy as np
from .sinogram import SinoProcessing
from ..thirdparty.pore3d_deringer_munch import munchetal_filter
from ..utils import check_supported

class Deringer(SinoProcessing):
    """
    Class aimed at wrapping several sinogram-based rings correction methods.
    """

    _available_methods = {
        "munch": munchetal_filter
    }

    def __init__(self, sinos_shape=None, radios_shape=None, method="munch", deringer_args=None, deringer_kwargs=None):
        """
        Parameters
        -----------
        method: str
            Sinogram rings correction method.
        deringer_args: list or tuple
            List of options to pass (additionally to the current sinogram) to
            the sinogram de-striping function.
        deringer_kwargs: dict
            Dictionary of named options to pass to the sinogram de-striping function.

        Please see the SinoProcessing documentation for other parameters
        """
        super().__init__(sinos_shape=sinos_shape, radios_shape=radios_shape)
        self._init_destriping_function(method, deringer_args, deringer_kwargs)


    def _init_destriping_function(self, method, deringer_args, deringer_kwargs):
        check_supported(method, list(self._available_methods.keys()), "method")
        self.method = method
        self._destriping_func = self._available_methods[method]
        self.deringer_args = []
        if deringer_args is not None:
            self.deringer_args = deringer_args
        self.deringer_kwargs = {}
        if deringer_kwargs is not None:
            self.deringer_kwargs = deringer_kwargs

    def _destripe_sinogram(self, sinogram):
        return self._destriping_func(
            sinogram,
            *self.deringer_args,
            **self.deringer_kwargs
        )


    def correct_rings(self, sinos, output=None):
        """
        Correct the rings in sinogram.
        Defaults to in-place processing !

        Parameters
        -----------
        sino: numpy.ndarray, optional
            Sinogram or stack of sinograms.
        output: numpy.ndarray, optional
            Stack of sinograms. If not provided, the correction will overwrite
            the sinogram passed as input.
        """
        if output is None:
            output = sinos
        # TODO more elegant
        if sinos.ndim == 2:
            output[:] = self._destripe_sinogram(sinos)
            return output
        n_sinos = sinos.shape[0]
        for i in range(n_sinos):
            output[i] = self._destripe_sinogram(sinos[i])
        return output
