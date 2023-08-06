import numpy as np
from silx.io import get_data
from ..preproc.ccd import FlatField
from ..preproc.alignment import CenterOfRotation

class CORFinder:
    """
    An application-type class for finding the Center Of Rotation (COR).
    """
    def __init__(self, dataset_info, angles=None, halftomo=False):
        """
        Initialize a CORFinder object.

        Parameters
        ----------
        dataset_info: `nabu.resources.dataset_analyzer.DatasetAnalyzer`
            Dataset information structure
        angles: array, optional
            Information on rotation angles. If provided, it overwrites
            the rotation angles available in `dataset_info`, if any.
        halftomo: bool, optional
            Whether the scan was performed in "half tomography" acquisition.
        """
        self.halftomo = halftomo
        self.dataset_info = dataset_info
        self.shape = dataset_info._radio_dims_notbinned[::-1]
        self._get_angles(angles)
        self._init_radios()
        self._init_flatfield()
        self._apply_flatfield()
        self.cor = CenterOfRotation()


    def _get_angles(self, angles):
        dataset_angles = self.dataset_info.rotation_angles
        if dataset_angles is None:
            if angles is None: # should not happen with hdf5
                print("Warning: no information on angles was found for this dataset. Using default [0, 180[ range.")
                angles = np.linspace(0, np.pi, len(self.dataset_info.projections), False)
            dataset_angles = angles
        self.angles = dataset_angles


    def _init_radios(self):
        # TODO
        if self.halftomo:
            raise NotImplementedError("Automatic COR with half tomo is not supported yet")
        #
        # We take 2 radios. It could be tuned for a 360 degrees scan.
        self._n_radios = 2
        self._radios_indices = []
        radios_indices = sorted(self.dataset_info.projections.keys())

        # Take angles 0 and 180 degrees. It might not work of there is an offset
        i_0 = np.argmin(np.abs(self.angles))
        i_180 = np.argmin(np.abs(self.angles - np.pi))
        _min_indices = [i_0, i_180]
        self._radios_indices = [
            radios_indices[i_0],
            radios_indices[i_180]
        ]
        self.radios = np.zeros((self._n_radios, ) + self.shape, "f")
        for i in range(self._n_radios):
            radio_idx = self._radios_indices[i]
            self.radios[i] = get_data(self.dataset_info.projections[radio_idx]).astype("f")


    def _init_flatfield(self):
        self.flatfield = FlatField(
            self.radios.shape,
            flats=self.dataset_info.flats,
            darks=self.dataset_info.darks,
            radios_indices=self._radios_indices,
            interpolation="linear",
            convert_float=True
        )


    def _apply_flatfield(self):
        self.flatfield.normalize_radios(self.radios)


    def find_cor(self, **cor_kwargs):
        """
        Find the center of rotation.

        Parameters
        ----------
        This function passes the named parameters to nabu.preproc.alignment.CenterOfRotation.find_shift.

        Returns
        -------
        cor: float
            The estimated center of rotation for the current dataset.
        """
        shift = self.cor.find_shift(
            self.radios[0],
            np.fliplr(self.radios[1]),
            **cor_kwargs
        )
        # find_shift returned a single scalar in 2020.1
        # This should be the default after 2020.2 release
        if hasattr(shift, "__iter__"):
            shift = shift[0]
        #
        return self.shape[1]/2 + shift

