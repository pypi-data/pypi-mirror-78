import pytest
import numpy as np
import os
import h5py

try:
    import scipy.ndimage
    __has_scipy__ = True
except ImportError:
    __has_scipy__ = False

from nabu.preproc import alignment
from nabu.testutils import utilstest, __do_long_tests__

@pytest.fixture(scope="class")
def bootstrap_base(request):
    cls = request.cls
    cls.abs_tol = 2.5e-2


@pytest.fixture(scope="class")
def bootstrap_cor(request):
    cls = request.cls
    cls.abs_tol = 0.2

    cls.data, calib_data = get_cor_data_h5("test_alignment_cor.h5")
    cls.cor_gl_pix, cls.cor_hl_pix, cls.tilt_deg = calib_data


@pytest.fixture(scope="class")
def bootstrap_dtr(request):
    cls = request.cls
    cls.abs_tol = 1e-1

    cls.data, cls.img_pos, calib_data = get_alignxc_data("test_alignment_alignxc.h5")
    cls.expected_shifts_vh, cls.all_shifts_vh = calib_data


@pytest.fixture(scope="class")
def bootstrap_fcs(request):
    cls = request.cls
    cls.abs_tol_dist = 1e-2
    cls.abs_tol_tilt = 2.5e-4

    cls.data, cls.img_pos, cls.pixel_size, (calib_data_std, calib_data_angle) = get_focus_data("test_alignment_focus.h5")
    cls.angle_best_ind, cls.angle_best_pos, cls.angle_tilt_v, cls.angle_tilt_h = calib_data_angle
    cls.std_best_ind, cls.std_best_pos = calib_data_std


def get_cor_data_h5(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    with h5py.File(dataset_downloaded_path, "r") as hf:
        data = hf["/entry/instrument/detector/data"][()]

        cor_global_pix = hf['/calibration/alignment/global/x_rotation_axis_pixel_position'][()]

        cor_highlow_pix = hf['/calibration/alignment/highlow/x_rotation_axis_pixel_position'][()]
        tilt_deg = hf['/calibration/alignment/highlow/z_camera_tilt'][()]

    return data, (cor_global_pix, cor_highlow_pix, tilt_deg)


def get_alignxc_data(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    with h5py.File(dataset_downloaded_path, "r") as hf:
        data = hf["/entry/instrument/detector/data"][()]
        img_pos = hf["/entry/instrument/detector/distance"][()]

        unit_length_shifts_vh = [
            hf['/calibration/alignxc/y_pixel_shift_unit'][()],
            hf['/calibration/alignxc/x_pixel_shift_unit'][()]
        ]
        all_shifts_vh = hf['/calibration/alignxc/yx_pixel_offsets'][()]

    return data, img_pos, (unit_length_shifts_vh, all_shifts_vh)


def get_focus_data(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    with h5py.File(dataset_downloaded_path, "r") as hf:
        data = hf["/entry/instrument/detector/data"][()]
        img_pos = hf["/entry/instrument/detector/distance"][()]

        pixel_size = np.mean([
            hf['/entry/instrument/detector/x_pixel_size'][()],
            hf['/entry/instrument/detector/y_pixel_size'][()]
        ])

        angle_best_ind = hf['/calibration/focus/angle/best_img'][()]
        angle_best_pos = hf['/calibration/focus/angle/best_pos'][()]
        angle_tilt_v = hf['/calibration/focus/angle/tilt_v_rad'][()]
        angle_tilt_h = hf['/calibration/focus/angle/tilt_h_rad'][()]

        std_best_ind = hf['/calibration/focus/std/best_img'][()]
        std_best_pos = hf['/calibration/focus/std/best_pos'][()]

    calib_data_angle = (angle_best_ind, angle_best_pos, angle_tilt_v, angle_tilt_h)
    calib_data_std = (std_best_ind, std_best_pos)
    return data, img_pos, pixel_size, (calib_data_std, calib_data_angle)


@pytest.mark.usefixtures("bootstrap_base")
class TestAlignmentBase(object):
    def test_peak_fitting_2d_3x3(self):
        # Fit a 3 x 3 grid
        fy = np.linspace(-1, 1, 3)
        fx = np.linspace(-1, 1, 3)
        yy, xx = np.meshgrid(fy, fx, indexing="ij")

        peak_pos_yx = np.random.rand(2) * 1.6 - 0.8
        f_vals = np.exp(-((yy - peak_pos_yx[0]) ** 2 + (xx - peak_pos_yx[1]) ** 2) / 100)

        fitted_peak_pos_yx = alignment.AlignmentBase.refine_max_position_2d(f_vals, fy, fx)

        message = (
            "Computed peak position: (%f, %f) " % (*fitted_peak_pos_yx,)
            + " and real peak position (%f, %f) do not coincide." % (*peak_pos_yx,)
            + " Difference: (%f, %f)," % (*(fitted_peak_pos_yx - peak_pos_yx),)
            + " tolerance: %f" % self.abs_tol
        )
        assert np.all(np.isclose(peak_pos_yx, fitted_peak_pos_yx, atol=self.abs_tol)), message

    def test_peak_fitting_2d_error_checking(self):
        # Fit a 3 x 3 grid
        fy = np.linspace(-1, 1, 3)
        fx = np.linspace(-1, 1, 3)
        yy, xx = np.meshgrid(fy, fx, indexing="ij")

        peak_pos_yx = np.random.rand(2) + 1.5
        f_vals = np.exp(-((yy - peak_pos_yx[0]) ** 2 + (xx - peak_pos_yx[1]) ** 2) / 100)

        with pytest.raises(ValueError) as ex:
            alignment.AlignmentBase.refine_max_position_2d(f_vals, fy, fx)

        message = (
            "Error should have been raised about the peak being fitted outside margins, "
            + "other error raised instead:\n%s" % str(ex.value)
        )
        assert "positions are outide the input margins" in str(ex.value), message

    def test_extract_peak_regions_1d(self):
        img = np.random.randint(0, 10, size=(8, 8))

        peaks_pos = np.argmax(img, axis=-1)
        peaks_val = np.max(img, axis=-1)

        cc_coords = np.arange(0, 8)

        (found_peaks_val, found_peaks_pos) = alignment.AlignmentBase.extract_peak_regions_1d(img, axis=-1, cc_coords=cc_coords)
        message = "The found peak positions do not correspond to the expected peak positions:\n  Expected: %s\n  Found: %s" % (
            peaks_pos,
            found_peaks_pos[1, :],
        )
        assert np.all(peaks_val == found_peaks_val[1, :]), message


@pytest.mark.usefixtures("bootstrap_cor")
class TestCor(object):
    def test_cor_posx(self):
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        CoR_calc = alignment.CenterOfRotation()
        cor_position = CoR_calc.find_shift(radio1, radio2)

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_gl_pix
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message

    def test_noisy_cor_posx(self):
        radio1 = np.fmax(self.data[0, :, :], 0)
        radio2 = np.fmax(self.data[1, :, :], 0)

        radio1 = np.random.poisson(radio1 * 400)
        radio2 = np.random.poisson(np.fliplr(radio2) * 400)

        CoR_calc = alignment.CenterOfRotation()
        cor_position = CoR_calc.find_shift(radio1, radio2, median_filt_shape=(3, 3))

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_gl_pix
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message

    @pytest.mark.skipif(not(__has_scipy__), reason="need scipy for this test")
    def test_noisyHF_cor_posx(self):
        """  test with noise at high frequencies
        """
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        noise_level = radio1.max() / 16.0
        noise_ima1 = np.random.normal(0.0, size=radio1.shape) * noise_level
        noise_ima2 = np.random.normal(0.0, size=radio2.shape) * noise_level

        noise_ima1 = noise_ima1 - scipy.ndimage.filters.gaussian_filter(noise_ima1, 2.0)
        noise_ima2 = noise_ima2 - scipy.ndimage.filters.gaussian_filter(noise_ima2, 2.0)

        radio1 = radio1 + noise_ima1
        radio2 = radio2 + noise_ima2

        CoR_calc = alignment.CenterOfRotation()

        # cor_position = CoR_calc.find_shift(radio1, radio2)
        cor_position = CoR_calc.find_shift(radio1, radio2, low_pass=(6.0, 0.3))

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_gl_pix
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message

    def test_cor_posx_linear(self):
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        CoR_calc = alignment.CenterOfRotation()
        cor_position = CoR_calc.find_shift(radio1, radio2, padding_mode="edge")

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_gl_pix
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message

    def test_error_checking_001(self):
        CoR_calc = alignment.CenterOfRotation()

        radio1 = self.data[0, :, :1:]
        radio2 = self.data[1, :, :]

        with pytest.raises(ValueError) as ex:
            CoR_calc.find_shift(radio1, radio2)

        message = "Error should have been raised about img #1 shape, other error raised instead:\n%s" % str(ex.value)
        assert "Images need to be 2-dimensional. Shape of image #1" in str(ex.value), message

    def test_error_checking_002(self):
        CoR_calc = alignment.CenterOfRotation()

        radio1 = self.data[0, :, :]
        radio2 = self.data

        with pytest.raises(ValueError) as ex:
            CoR_calc.find_shift(radio1, radio2)

        message = "Error should have been raised about img #2 shape, other error raised instead:\n%s" % str(ex.value)
        assert "Images need to be 2-dimensional. Shape of image #2" in str(ex.value), message

    def test_error_checking_003(self):
        CoR_calc = alignment.CenterOfRotation()

        radio1 = self.data[0, :, :]
        radio2 = self.data[1, :, 0:10]

        with pytest.raises(ValueError) as ex:
            CoR_calc.find_shift(radio1, radio2)

        message = "Error should have been raised about different image shapes, " + "other error raised instead:\n%s" % str(
            ex.value
        )
        assert "Images need to be of the same shape" in str(ex.value), message

    def test_camera_tilt(self):
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        tilt_calc = alignment.CameraTilt()
        cor_position, camera_tilt = tilt_calc.compute_angle(radio1, radio2)

        message = "Computed tilt %f " % camera_tilt + " and real tilt %f do not coincide" % self.tilt_deg
        assert np.isclose(self.tilt_deg, camera_tilt, atol=self.abs_tol), message

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_hl_pix
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message


@pytest.mark.usefixtures("bootstrap_dtr")
class TestDetectorTranslation(object):
    def test_alignxc(self):
        T_calc = alignment.DetectorTranslationAlongBeam()

        shifts_v, shifts_h, found_shifts_list = T_calc.find_shift(self.data, self.img_pos, return_shifts=True)

        message = "Computed shifts coefficients %s and expected %s do not coincide" % (
            (shifts_v, shifts_h),
            self.expected_shifts_vh,
        )
        assert np.all(np.isclose(self.expected_shifts_vh, [shifts_v, shifts_h], atol=self.abs_tol)), message

        message = "Computed shifts %s and expected %s do not coincide" % (found_shifts_list, self.all_shifts_vh)
        assert np.all(np.isclose(found_shifts_list, self.all_shifts_vh, atol=self.abs_tol)), message

    @pytest.mark.skipif(not(__has_scipy__), reason="need scipy for this test")
    def test_alignxc_synth(self):
        T_calc = alignment.DetectorTranslationAlongBeam()

        stack = np.zeros([4, 512, 512], "d")
        for i in range(4):
            stack[i, 200 - i * 10, 200 - i * 10] = 1
        stack = scipy.ndimage.filters.gaussian_filter(stack, [0, 10, 10.0]) * 100
        x, y = np.meshgrid(np.arange(stack.shape[-1]), np.arange(stack.shape[-2]))
        for i in range(4):
            xc = x - (250 + i * 1.234)
            yc = y - (250 + i * 1.234 * 2)
            stack[i] += np.exp(-(xc * xc + yc * yc) * 0.5)
        shifts_v, shifts_h, found_shifts_list = T_calc.find_shift(
            stack, np.array([0.0, 1, 2, 3]), high_pass=1.0, return_shifts=True
        )

        message = "Found shifts per units %s and reference %s do not coincide" % ((shifts_v, shifts_h), (-1.234 * 2, -1.234))
        assert np.all(np.isclose((shifts_v, shifts_h), (-1.234 * 2, -1.234), atol=self.abs_tol)), message


@pytest.mark.skipif(not(__do_long_tests__), reason="need environment variable NABU_LONG_TESTS=1")
@pytest.mark.usefixtures("bootstrap_fcs")
class TestFocus(object):
    def test_find_distance(self):
        focus_calc = alignment.CameraFocus()
        focus_pos, focus_ind = focus_calc.find_distance(self.data, self.img_pos)

        message = "Computed focus motor position %f " % focus_pos + " and expected %f do not coincide" % self.std_best_pos
        assert np.isclose(self.std_best_pos, focus_pos, atol=self.abs_tol_dist), message

        message = "Computed focus image index %f " % focus_ind + " and expected %f do not coincide" % self.std_best_ind
        assert np.isclose(self.std_best_ind, focus_ind, atol=self.abs_tol_dist), message

    def test_find_scintillator_tilt(self):
        focus_calc = alignment.CameraFocus()
        focus_pos, focus_ind, tilts_vh = focus_calc.find_scintillator_tilt(self.data, self.img_pos)

        message = "Computed focus motor position %f " % focus_pos + " and expected %f do not coincide" % self.angle_best_pos
        assert np.isclose(self.angle_best_pos, focus_pos, atol=self.abs_tol_dist), message

        message = "Computed focus image index %f " % focus_ind + " and expected %f do not coincide" % self.angle_best_ind
        assert np.isclose(self.angle_best_ind, focus_ind, atol=self.abs_tol_dist), message

        expected_tilts_vh = np.squeeze(np.array([self.angle_tilt_v, self.angle_tilt_h]))
        computed_tilts_vh = - tilts_vh / (self.pixel_size / 1000)
        message = "Computed tilts %s and expected %s do not coincide" % (computed_tilts_vh, expected_tilts_vh)
        assert np.all(np.isclose(computed_tilts_vh, expected_tilts_vh, atol=self.abs_tol_tilt)), message

    def test_size_determination(self):
        inp_shape = [2162, 2560]
        exp_shape = np.array([2160, 2160])
        new_shape = alignment.CameraFocus._check_img_block_size(inp_shape, 4, suggest_new_shape=True)

        message = "New suggested shape: %s and expected: %s do not coincide" % (new_shape, exp_shape)
        assert np.all(new_shape == exp_shape), message
