import numpy as np
import pytest
from nabu.utils import clip_circle
from nabu.testutils import get_data, compare_arrays
from nabu.cuda.utils import __has_pycuda__, __has_cufft__
if __has_pycuda__:
    from nabu.reconstruction.fbp import Backprojector
try:
    from scipy.ndimage import shift
    __have_scipy__= True
except ImportError:
    __have_scipy__= False


@pytest.fixture(scope='class')
def bootstrap(request):
    cls = request.cls
    cls.sino_512 = get_data("mri_sino500.npz")["data"]
    cls.ref_512 = get_data("mri_rec_astra.npz")["data"]
    cls.sino_511 = cls.sino_512[:, :-1]
    cls.tol = 5e-2

@pytest.mark.skipif(not(__has_pycuda__ and __has_cufft__), reason="Need pycuda and scikit-cuda for this test")
@pytest.mark.usefixtures('bootstrap')
class TestFBP:

    @staticmethod
    def clip_to_inner_circle(img):
        radius = int(0.99*max(img.shape)/2)
        return clip_circle(img, radius=radius)

    def test_fbp_512(self):
        """
        Simple test of a FBP on a 512x512 slice
        """
        B = Backprojector((500, 512))
        res = B.fbp(self.sino_512)

        delta_clipped = self.clip_to_inner_circle(res - self.ref_512)
        err_max = np.max(np.abs(delta_clipped))

        assert err_max < self.tol, "Max error is too high"


    def test_fbp_511(self):
        """
        Test FBP of a 511x511 slice where the rotation axis is at (512-1)/2.0
        """
        B = Backprojector((500, 511), rot_center=255.5)
        res = B.fbp(self.sino_511)
        ref = self.ref_512[:-1, :-1]

        delta_clipped = self.clip_to_inner_circle(res - ref)
        err_max = np.max(np.abs(delta_clipped))

        assert err_max < self.tol, "Max error is too high"


    def test_multi_fbp(self):
        """
        Test FBP of a 3D sinogram
        """
        multi_sino = np.tile(self.sino_511, (4, 1, 1))
        B = Backprojector(multi_sino.shape, rot_center=255.5)
        res = B.fbp(multi_sino)

        err_max = np.max(np.abs(np.std(res, axis=0)))
        assert err_max < 1e-5, "Something wrong with multi-FBP"

        ref = self.ref_512[:-1, :-1]
        delta_clipped = self.clip_to_inner_circle(res[0] - ref)
        err_max = np.max(np.abs(delta_clipped))

        assert err_max < self.tol, "Max error is too high"


    def test_fbp_roi(self):
        """
        Test FBP in region of interest
        """
        sino = self.sino_511
        B0 = Backprojector(sino.shape, rot_center=255.5)
        ref = B0.fbp(sino)

        def backproject_roi(roi, reference):
            B = Backprojector(sino.shape, rot_center=255.5, slice_roi=roi)
            res = B.fbp(sino)
            err_max = np.max(np.abs(res - ref))
            return err_max

        cases = {
            # Test 1: use slice_roi=(0, -1, 0, -1), i.e plain FBP of whole slice
            1: [(0, None, 0, None), ref],
            # Test 2: horizontal strip
            2: [(0, None, 50, 100), ref[50:100, :]],
            # Test 3: vertical strip
            3: [(60, 65, 0, None), ref[:, 60:65]],
            # Test 4: rectangular inner ROI
            4: [(157, 162, 260, -10), ref[260:-10, 157:162]],
        }
        for roi, ref in cases.values():
            err_max = backproject_roi(roi, ref)
            assert err_max < self.tol, str("backproject_roi: max error is too high for ROI=%s" % str(roi))


    @pytest.mark.skipif(not(__have_scipy__), reason="Need scipy for this test")
    def test_fbp_axis_corr(self):
        """
        Test the "axis correction" feature
        """
        sino = self.sino_512
        # Create a sinogram with a drift in the rotation axis
        def create_drifted_sino(sino, drifts):
            out = np.zeros_like(sino)
            for i in range(sino.shape[0]):
                out[i] = shift(sino[i], drifts[i])
            return out
        drifts = np.linspace(0, 20, sino.shape[0])
        sino = create_drifted_sino(sino, drifts)
        B = Backprojector(sino.shape, extra_options={"axis_correction": drifts})
        res = B.fbp(sino)

        delta_clipped = clip_circle(res - self.ref_512, radius=200)
        err_max = np.max(np.abs(delta_clipped))
        # Max error is relatively high, migh be due to interpolation of scipy shift in sinogram
        assert err_max < 10., "Max error is too high"

