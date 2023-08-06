import numpy as np
from ..utils import get_2D_3D_shape

class SinoProcessing(object):
    """
    A base class for processing sinograms.
    """

    def __init__(self, sinos_shape=None, radios_shape=None, rot_center=None, halftomo=False):
        """
        Initialize a SinoProcessing instance.

        Parameters
        ----------
        sinos_shape: tuple of int
            Shape of the stack of sinograms, in the form `(n_z, n_angles, n_x)`.
            If not provided, it is derived from `radios_shape`.
        radios_shape: tuple of int
            Shape of the chunk of radios, in the form `(n_angles, n_z, n_x)`.
            If not provided, it is derived from `sinos_shape`.
        rot_center: int or array
            Rotation axis position. A scalar indicates the same rotation axis position
            for all the projections.
        halftomo: bool
            Whether "half tomography" is enabled. Default is False.
        """
        self._get_shapes(sinos_shape, radios_shape)
        self.set_rot_center(rot_center)
        self._set_halftomo(halftomo)


    def _get_shapes(self, sinos_shape, radios_shape):
        if (sinos_shape is None) and (radios_shape is None):
            raise ValueError("Need to provide sinos_shape and/or radios_shape")
        if sinos_shape is None:
            n_a, n_z, n_x = get_2D_3D_shape(radios_shape)
            sinos_shape = (n_z, n_a, n_x)
        elif len(sinos_shape) == 2:
            sinos_shape = (1, ) + sinos_shape
        if radios_shape is None:
            n_z, n_a, n_x = get_2D_3D_shape(sinos_shape)
            radios_shape = (n_a, n_z, n_x)
        elif len(radios_shape) == 2:
            radios_shape = (1, ) + radios_shape

        self.sinos_shape = sinos_shape
        self.radios_shape = radios_shape
        n_a, n_z, n_x = radios_shape
        self.n_angles = n_a
        self.n_z = n_z
        self.n_x = n_x


    def set_rot_center(self, rot_center):
        """
        Set the rotation axis position for the current radios/sinos stack.

        rot_center: int or array
            Rotation axis position. A scalar indicates the same rotation axis position
            for all the projections.
        """
        if rot_center is None:
            rot_center = (self.n_x - 1) / 2.
        if not(np.isscalar(rot_center)):
            rot_center = np.array(rot_center)
            if rot_center.size != self.n_angles:
                raise ValueError(
                    "Expected rot_center to have %d elements but got %d"
                    % (self.n_angles, rot_center.size)
                )
        self.rot_center = rot_center
        self._rot_center_int = int(round(self.rot_center))


    def _set_halftomo(self, halftomo):
        self.halftomo = halftomo
        if not(halftomo):
            return
        assert (self.n_angles % 2) == 0, "Half tomography: expected an even number of angles (got %d)" % self.n_angles
        if abs(self.rot_center - ((self.n_x - 1) / 2.)) < 1: # which tol ?
            raise ValueError(
                "Half tomography: incompatible rotation axis position: %.2f"
                % self.rot_center
            )
        self.sinos_halftomo_shape = (self.n_z, self.n_angles // 2, 2 * self._rot_center_int)


    def _check_array_shape(self, array, kind="radio"):
        expected_shape = self.radios_shape if "radio" in kind else self.sinos_shape
        assert array.shape == expected_shape, "Expected radios shape %s, but got %s" % (expected_shape, array.shape)


    def _radios_to_sinos_simple(self, radios, output, copy=False):
        sinos = np.rollaxis(radios, 1, 0)  # view
        if not(copy) and output is None:
            return sinos
        if output is None: # copy and output is None
            return np.ascontiguousarray(sinos)  # copy
        # not(copy) and output is not None
        for i in range(output.shape[0]):
            output[i] = sinos[i]
        return output


    def _radios_to_sinos_halftomo(self, radios, sinos):
        # TODO
        if not(np.isscalar(self.rot_center)):
            raise NotImplementedError("Half tomo with varying rotation axis position is not implemented yet")
        #

        n_a, n_z, n_x = radios.shape
        n_a2 = n_a // 2
        out_dwidth = 2 * self._rot_center_int
        if sinos is not None:
            if sinos.shape[-1] != out_dwidth:
                raise ValueError(
                    "Expected sinos sinogram last dimension to have %d elements"
                    % out_dwidth
                )
            if sinos.shape[-2] != n_a2:
                raise ValueError("Expected sinograms to have %d angles" % n_a2)
        else:
            sinos = np.zeros(self.sinos_halftomo_shape, dtype=np.float32)
        for i in range(n_z):
            sinos[i][:] = convert_halftomo(radios[:, i, :], self._rot_center_int)
        return sinos


    @property
    def output_shape(self):
        """
        Get the output sinograms shape.
        """
        if self.halftomo:
            return self.sinos_halftomo_shape
        return self.sinos_shape


    def radios_to_sinos(self, radios, output=None, copy=False):
        """
        Convert a chunk of radios to a stack of sinograms.

        Parameters
        -----------
        radios: array
            Radios to convert
        output: array, optional
            Output sinograms array, pre-allocated
        """
        self._check_array_shape(radios, kind="radio")
        if self.halftomo:
            return self._radios_to_sinos_halftomo(radios, output)
        return self._radios_to_sinos_simple(radios, output, copy=copy)



def convert_halftomo(sino, rotation_axis_position):
    """
    Converts a sinogram into a sinogram with extended FOV with the "half tomography"
    setting.
    """
    assert sino.ndim == 2
    assert (sino.shape[0] % 2) == 0
    na, nx = sino.shape
    na2 = na // 2
    r = rotation_axis_position
    d = nx - r
    res = np.zeros((na2, 2 * r), dtype="f")

    sino1 = sino[:na2, :]
    sino2 = sino[na2:, ::-1]
    res[:, : nx - d] = sino1[:, : nx - d]
    #
    w1 = np.linspace(0, 1, d, endpoint=True)
    res[:, nx - d : nx] = (1 - w1) * sino1[:, nx - d :] + w1 * sino2[:, d : 2 * d]
    #
    res[:, nx:] = sino2[:, 2 * d :]

    return res

