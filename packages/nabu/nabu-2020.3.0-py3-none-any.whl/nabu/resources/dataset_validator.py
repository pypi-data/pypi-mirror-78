import os
import numpy as np
from silx.io import get_data
from ..utils import subsample_dict
from .validators import validator, directory_writeable_validator
from .utils import get_values_from_file


"""
The NabuValidator class is a "second-stage validation".
The first stage was:
  - Validate individual entries of the nabu config file / config dict
  - Analyze the dataset and extract information (radios, flats, darks, energy, ...)
Now we couple these two (nabu config and dataset) together in order to cross check.
"""


class NabuValidator(object):
    def __init__(self, nabu_config, dataset_infos):
        """
        Perform a cross-validation of nabu configuration against dataset informations.
        Check the consistency of these two structures, and possibly modify them in-place.

        Parameters
        ----------
        nabu_config: dict
            Dictionary containing the nabu configuration, usually got from
            `nabu.io.config.validate_nabu_config()`
            It will possibly be modified !
        dataset_infos: `DatasetAnalyzer`
            Structure containing information on the dataset to process.
            It will possibly be modified !
        """
        self.nabu_config = nabu_config
        self.dataset_infos = dataset_infos
        self.check_not_empty() # has to be done first
        self.convert_negative_indices()
        self.get_angles()
        self._get_rotation_axis()
        self._get_translation_file()
        self._get_resources()
        self._get_output_filename()


    @staticmethod
    def _convert_negative_idx(idx, last_idx):
        res = idx
        if idx < 0:
            res = last_idx + idx
        return res


    def convert_negative_indices(self):
        """
        Convert any negative index to the corresponding positive index.
        """
        nx, nz = self.dataset_infos.radio_dims
        ny = nx
        if self.nabu_config["reconstruction"]["enable_halftomo"]:
            if self.dataset_infos.axis_position is None:
                raise ValueError("rotation_axis_position should be either a number or 'auto' for half tomo")
            cor = int(round(self.dataset_infos.axis_position))
            ny = nx = 2*cor
        what = (
            ("reconstruction", "start_x", nx),
            ("reconstruction", "end_x", nx),
            ("reconstruction", "start_y", ny),
            ("reconstruction", "end_y", ny),
            ("reconstruction", "start_z", nz),
            ("reconstruction", "end_z", nz),
        )
        for section, key, upper_bound in what:
            self.nabu_config[section][key] = self._convert_negative_idx(
                self.nabu_config[section][key], upper_bound
            )


    def check_not_empty(self):
        assert len(self.dataset_infos.projections) > 0, "Dataset seems to be empty (no projections)"
        assert self.dataset_infos.n_angles is not None, "Could not determine the number of projections. Please check the .info or HDF5 file"
        for dim_name, n in zip(["dim_1", "dim_2"], self.dataset_infos.radio_dims):
            assert n is not None, "Could not determine %s. Please check the .info file or HDF5 file" % dim_name
        self._projs_indices = sorted(self.dataset_infos.projections.keys())


    def get_angles(self):
        rec_params = self.nabu_config["reconstruction"]
        n_angles = self.dataset_infos.n_angles
        angles_file = rec_params["angles_file"]
        if angles_file is not None:
            try:
                angles = get_values_from_file(angles_file, n_values=n_angles)
            except ValueError:
                print("Something wrong with angle file %s" % angles_file)
                raise
        else:
            angles = self.dataset_infos.rotation_angles
            if angles is None:
                if rec_params["enable_halftomo"]:
                    angles = np.linspace(0, 2*np.pi, n_angles, True)
                else:
                    angles = np.linspace(0, np.pi, n_angles, False)
        angles += np.deg2rad(rec_params["angle_offset"])
        self.dataset_infos.reconstruction_angles = angles


    def _get_rotation_axis(self):
        rec_params = self.nabu_config["reconstruction"]
        axis_correction_file = rec_params["axis_correction_file"]
        axis_correction = None
        if axis_correction_file is not None:
            try:
                axis_correction = get_values_from_file(
                    axis_correction_file, n_values=self.dataset_infos.n_angles
                ).astype(np.flooat32)
            except ValueError:
                print("Something wrong with axis correction file %s" % axis_correction_file)
                raise
        self.dataset_infos.axis_correction = axis_correction


    def _get_translation_file(self):
        rec_params = self.nabu_config["reconstruction"]
        transl_file = rec_params["translation_movements_file"]
        if transl_file in (None, ''):
            return
        translations = None
        if transl_file is not None and "://" not in transl_file:
            try:
                translations = get_values_from_file(
                    transl_file, shape=(self.dataset_infos.n_angles, 2)
                ).astype(np.float32)
            except ValueError:
                print("Something wrong with translation_movements_file %s" % transl_file)
                raise
        else:
            try:
                translations = get_data(transl_file)
            except:
                print("Something wrong with translation_movements_file %s" % transl_file)
                raise
        self.dataset_infos.translations = translations


    def _get_resources(self):
        opts = self.nabu_config["resources"]
        if opts["gpu_id"] != []:
            opts["gpus"] = len(opts["gpu_id"])
        if opts["gpus"] == 0:
            opts["gpu_id"] = []


    def _get_output_filename(self):
        opts = self.nabu_config["output"]
        dataset_path = self.nabu_config["dataset"]["location"]
        if opts["location"] == "" or opts["location"] is None:
            opts["location"] = os.path.dirname(dataset_path)
        if opts["file_prefix"] == "" or opts["file_prefix"] is None:
            if os.path.isfile(dataset_path): # hdf5
                file_prefix = os.path.basename(dataset_path).split(".")[0]
            elif os.path.isdir(dataset_path):
                file_prefix = os.path.basename(dataset_path)
            else:
                raise ValueError(
                    "dataset location %s is neither a file or directory"
                    % dataset_path
                )
            file_prefix += "_rec" # avoid overwriting dataset
            opts["file_prefix"] = file_prefix


    #
    # User-triggered checks
    #
    def check_first_last_radios(self):
        first_idx = self._projs_indices[0]
        last_idx = self._projs_indices[-1]


    def check_can_do_flatfield(self):
        if self.nabu_config["preproc"]["flatfield_enabled"]:
            darks = self.dataset_infos.darks
            assert len(darks) > 0, "Need at least one dark to perform flat-field correction"
            for dark_id, dark_url in darks.items():
                assert os.path.isfile(dark_url.file_path()), "Dark file %s not found" % dark_url.file_path()
            flats = self.dataset_infos.flats
            assert len(flats) > 0, "Need at least one flat to perform flat-field correction"
            for flat_id, flat_url in flats.items():
                assert os.path.isfile(flat_url.file_path()), "Flat file %s not found" % flat_url.file_path()


    @staticmethod
    def _check_start_end_idx(start, end, n_elements, start_name="start_x", end_name="end_x"):
        assert (start >= 0 and start < n_elements), "Invalid value for %s, must be >= 0 and < %d" % (start_name, n_elements)
        assert (end >= 0 and end < n_elements), "Invalid value for %s, must be >= 0 and < %d" % (end_name, n_elements)


    def check_slice_indexes(self):
        nx, nz = self.dataset_infos.radio_dims
        rec_params = self.nabu_config["reconstruction"]
        if rec_params["enable_halftomo"]:
            cor = int(round(rec_params["rotation_axis_position"]))
            ny = nx = 2*cor
        what = (
            ("start_x", "end_x", nx),
            ("start_y", "end_y", nx),
            ("start_z", "end_z", nz)
        )
        for (start_name, end_name, numels) in what:
            self._check_start_end_idx(
                rec_params[start_name],
                rec_params[end_name],
                numels,
                start_name=start_name,
                end_name=end_name
            )


    def perform_all_checks(self, remove_unused_radios=True):
        """
        Do the final stage of validation: check the nabu configuration against
        the analyzed dataset.
        """
        self.check_first_last_radios()
        self.check_can_do_flatfield()
        self.check_slice_indexes()
        if remove_unused_radios:
            self.remove_unused_radios()
        self.handle_processing_mode()
        self.handle_binning()
        self.check_output_file()


    #
    # Dataset modifications
    #
    def remove_unused_radios(self):
        unused_radios = self.dataset_infos.remove_unused_radios()
        # update
        self._projs_indices = sorted(self.dataset_infos.projections.keys())


    def handle_binning(self):
        """
        Modify the dataset description and nabu config to handle binning and
        projections subsampling.
        """
        self.dataset_infos._radio_dims_notbinned = self.dataset_infos.radio_dims
        dataset_cfg = self.nabu_config["dataset"]
        self.binning = (dataset_cfg["binning"], dataset_cfg["binning_z"])
        self.dataset_infos._binning = self.binning
        subsampling_factor = dataset_cfg["projections_subsampling"]
        self.projections_subsampling = subsampling_factor
        self.dataset_infos._projections_subsampled = self.dataset_infos.projections
        self.dataset_infos._projs_indices_subsampled = self._projs_indices
        if subsampling_factor > 1:
            self.dataset_infos._projections_subsampled = subsample_dict(self.dataset_infos.projections, subsampling_factor)
            self.dataset_infos._projs_indices_subsampled = sorted(self.dataset_infos._projections_subsampled.keys())
            self.dataset_infos.reconstruction_angles = self.dataset_infos.reconstruction_angles[::subsampling_factor]
            self.dataset_infos.n_angles //= subsampling_factor
        if self.binning != (1, 1):
            bin_x, bin_z = self.binning
            nx, nz = self.dataset_infos.radio_dims
            nx //= bin_x
            ny = nx # square slices
            nz //= bin_z
            self.dataset_infos.radio_dims = (nx, nz)
            rec_cfg = self.nabu_config["reconstruction"]
            end_x = rec_cfg["end_x"]
            end_y = rec_cfg["end_y"]
            end_z = rec_cfg["end_z"]
            bin_y = bin_x # square slices
            rec_cfg["end_x"] = (end_x // bin_x) - ((nx % bin_x) != 0)
            rec_cfg["end_y"] = (end_y // bin_y) - ((ny % bin_y) != 0)
            rec_cfg["end_z"] = (end_z // bin_z) - ((nz % bin_z) != 0)
            rec_cfg["start_x"] = (rec_cfg["start_x"] // bin_x)
            rec_cfg["start_y"] = (rec_cfg["start_y"] // bin_y)
            rec_cfg["start_z"] = (rec_cfg["start_z"] // bin_z)
            # Update the Rotation center
            # TODO axis_corrections
            rot_c = self.dataset_infos.axis_position
            nx0, nz0 = self.dataset_infos._radio_dims_notbinned
            bin_fact = nx0 / nx
            if rot_c is not None: # user-specified
                rot_c /= bin_fact # float
            else:
                rot_c = (nx - 1)/2.
            self.dataset_infos.axis_position = rot_c
            self.nabu_config["reconstruction"]["rotation_axis_position"] = rot_c


    def check_output_file(self):
        out_cfg = self.nabu_config["output"]
        out_fname = os.path.join(out_cfg["location"], out_cfg["file_prefix"] + out_cfg["file_format"])
        if os.path.exists(out_fname):
            raise ValueError("File %s already exists" % out_fname)


    def handle_processing_mode(self):
        mode = self.nabu_config["resources"]["method"]
        if mode == "preview":
            print("Warning: the method 'preview' was selected. This means that the data volume will be binned so that everything fits in memory.")
            # TODO automatically compute binning/subsampling factors as a function of lowest memory (GPU)
            self.nabu_config["dataset"]["binning"] = 2
            self.nabu_config["dataset"]["binning_z"] = 2
            self.nabu_config["dataset"]["projections_subsampling"] = 2
        # TODO handle other modes


