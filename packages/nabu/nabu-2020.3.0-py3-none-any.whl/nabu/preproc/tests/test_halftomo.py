import os
import numpy as np
import pytest
import h5py
from nabu.testutils import compare_arrays, utilstest
from nabu.preproc.sinogram import SinoProcessing, convert_halftomo
from nabu.cuda.utils import __has_pycuda__
if __has_pycuda__:
    import pycuda.gpuarray as garray
    from nabu.preproc.sinogram_cuda import CudaSinoProcessing


@pytest.fixture(scope='class')
def bootstrap(request):
    cls = request.cls
    radio, sino_ref, cor = get_data_h5("halftomo.h5")
    cls.radio = radio
    cls.radios = np.moveaxis(np.tile(cls.radio, (1, 1, 1)), 1, 0)
    cls.sino_ref = sino_ref
    cls.rot_center = cor
    cls.tol = 5e-3
    if __has_pycuda__:
        import pycuda.autoinit


def get_data_h5(*dataset_path):
    dataset_relpath = os.path.join(*dataset_path)
    dataset_path = utilstest.getfile(dataset_relpath)
    with h5py.File(dataset_path, 'r') as hf:
        radio = hf["entry/radio/results/data"][()]
        sino = hf["entry/sino/results/data"][()]
        cor = hf["entry/sino/configuration/configuration/rotation_axis_position"][()]
    return radio, sino, cor



@pytest.mark.usefixtures('bootstrap')
class TestHalftomo:

    def test_halftomo(self):
        sino_processing = SinoProcessing(
            radios_shape=self.radios.shape,
            rot_center=self.rot_center,
            halftomo=True
        )
        sinos_halftomo = sino_processing.radios_to_sinos(self.radios)
        _, err = compare_arrays(sinos_halftomo[0], self.sino_ref, self.tol, return_residual=True)
        assert err < self.tol, "Something wrong with SinoProcessing.radios_to_sino, halftomo=True"

    @pytest.mark.skipif(not(__has_pycuda__), reason="Need pycuda for this test")
    def test_cuda_halftomo(self):
        sino_processing = CudaSinoProcessing(
            radios_shape=self.radios.shape,
            rot_center=self.rot_center,
            halftomo=True
        )
        d_radios = garray.to_gpu(self.radios)
        d_sinos = garray.zeros(sino_processing.sinos_halftomo_shape, "f")
        sino_processing.radios_to_sinos(d_radios, output=d_sinos)
        sino_halftomo = d_sinos.get()[0]
        _, err = compare_arrays(sino_halftomo, self.sino_ref, self.tol, return_residual=True)
        assert err < self.tol, "Something wrong with SinoProcessing.radios_to_sino, halftomo=True"
