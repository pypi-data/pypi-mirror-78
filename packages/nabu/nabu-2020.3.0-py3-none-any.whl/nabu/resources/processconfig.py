import os
from ..utils import PlaceHolder, DataPlaceHolder, copy_dict_items
from ..io.config import NabuConfigParser, validate_nabu_config
from .dataset_analyzer import analyze_dataset, EDFDatasetAnalyzer, HDF5DatasetAnalyzer
from .dataset_validator import NabuValidator
from .cor import CORFinder


class ProcessConfig:
    """
    A class for describing the Nabu process configuration.
    """

    def __init__(
        self,
        conf_fname=None,
        conf_dict=None,
        dataset_infos=None,
        checks=True,
        remove_unused_radios=True,
    ):
        """
        Initialize a ProcessConfig class.

        Parameters
        ----------
        conf_fname: str
            Path to the nabu configuration file. If provided, the parameters
            `conf_dict` and `dataset_infos` are ignored.
        conf_dict: dict
            A dictionary describing the nabu processing steps.
            If provided, it should be provided along with `dataset_infos` ; in this
            case, the parameter `conf_fname` is ignored.
        dataset_infos: EDFDatasetAnalyzer
            A `EDFDatasetAnalyzer` class instance.
            If provided, it should be provided along with `conf_dict` ; in this
            case, the parameter `conf_fname` is ignored.
        checks: bool, optional, default is True
            Whether to perform checks on configuration and datasets (recommended !)
        remove_unused_radios: bool, optional, default is True
            Whether to remove unused radios, i.e radios present in the dataset,
            but not explicitly listed in the scan metadata.
        """
        args_error_msg = (
            "You must either provide conf_fname, or (conf_dict and dataset_infos)"
        )
        self.conf_fname = conf_fname
        if conf_fname is not None:
            if (conf_dict is not None) or (dataset_infos is not None):
                raise ValueError(args_error_msg)
            if not (os.path.isfile(conf_fname)):
                raise ValueError("No such file: %s" % conf_fname)
            conf = NabuConfigParser(conf_fname).conf_dict
            dataset_infos = analyze_dataset(conf["dataset"]["location"])
        else:
            if (conf_dict is None) or (dataset_infos is None):
                raise ValueError(args_error_msg)
            conf = conf_dict
            assert (isinstance(dataset_infos, EDFDatasetAnalyzer)) or (
                isinstance(dataset_infos, HDF5DatasetAnalyzer)
            )
        self.dataset_infos = dataset_infos
        self.nabu_config = validate_nabu_config(conf)
        self.checks = checks
        self.remove_unused_radios = remove_unused_radios
        self._get_cor()
        self.validation_stage2()
        self.build_processing_steps()


    def _get_cor(self):
        cor = self.nabu_config["reconstruction"]["rotation_axis_position"]
        if cor == "auto":
            self.corfinder = CORFinder(
                self.dataset_infos,
                halftomo=self.nabu_config["reconstruction"]["enable_halftomo"],
            )
            cor = self.corfinder.find_cor()
        self.dataset_infos.axis_position = cor


    def validation_stage2(self):
        validator = NabuValidator(self.nabu_config, self.dataset_infos)
        if self.checks:
            validator.perform_all_checks(remove_unused_radios=self.remove_unused_radios)


    def build_processing_steps(self):
        """
        Build a list of processing steps from a ProcessConfig instance.
        The returned structures are a more compact and ready-to-use representation
        of the two main fields of ProcessConfig (dataset_infos and nabu_config).
        """
        nabu_config = self.nabu_config
        dataset_infos = self.dataset_infos
        binning = (nabu_config["dataset"]["binning"], nabu_config["dataset"]["binning_z"])
        tasks = []
        options = {}

        #
        # Dataset / Get data
        #
        # First thing to do is to get the data (radios or sinograms)
        # For now data is assumed to be on disk (see issue #66).
        tasks.append("read_chunk")
        options["read_chunk"] = {
            "files": dataset_infos.projections, # TODO handle sinograms
            "sub_region": None,
            "binning": binning,
            "dataset_subsampling": nabu_config["dataset"]["projections_subsampling"]
        }
        #
        # Flat-field
        #
        if nabu_config["preproc"]["flatfield_enabled"]:
            tasks.append("flatfield")
            options["flatfield"] = {
                #  ChunkReader handles binning/subsampling by itself,
                # but FlatField needs "real" indices (after binning/subsampling)
                "projs_indices": dataset_infos._projs_indices_subsampled,
                "binning": binning,
            }
        if nabu_config["preproc"]["ccd_filter_enabled"]:
            tasks.append("ccd_correction")
            options["ccd_correction"] = {
                "type": "median_clip", # only one available for now
                "median_clip_thresh": nabu_config["preproc"]["ccd_filter_threshold"],
            }
        #
        # Double flat field
        #
        if nabu_config["preproc"]["double_flatfield_enabled"]:
            tasks.append("double_flatfield")
            options["double_flatfield"] = {
                # ~ "results_location": nabu_config["output"]["location"], # not useful (?)
                "sigma": nabu_config["preproc"]["dff_sigma"],
            }
        #
        #
        # Phase retrieval
        #
        if nabu_config["phase"]["method"] != None:
            tasks.append("phase")
            options["phase"] = copy_dict_items(
                nabu_config["phase"],
                ["delta_beta", "margin", "padding_type"]
            )
            options["phase"].update({
                "energy_kev": dataset_infos.energy,
                "distance_cm": dataset_infos.distance * 1e2,
                "pixel_size_microns": dataset_infos.pixel_size,
            })
            if binning != (1, 1):
                options["phase"]["delta_beta"] /= (binning[0] * binning[1])
        #
        # Unsharp
        #
        if nabu_config["phase"]["unsharp_coeff"] > 0:
            tasks.append("unsharp_mask")
            options["unsharp_mask"] = copy_dict_items(
                nabu_config["phase"], ["unsharp_coeff", "unsharp_sigma"]
            )
        #
        # -logarithm
        #
        if nabu_config["preproc"]["take_logarithm"]:
            tasks.append("take_log")
            options["take_log"] = copy_dict_items(nabu_config["preproc"], ["log_min_clip", "log_max_clip"])
        #
        # Translation movements
        #
        translations = dataset_infos.translations
        if translations is not None:
            tasks.append("radios_movements")
            options["radios_movements"] = {
                "translation_movements": dataset_infos.translations
            }
        #
        # Reconstruction
        #
        if nabu_config["reconstruction"]["method"] != None:
            tasks.append("build_sino")
            options["build_sino"] = copy_dict_items(
                nabu_config["reconstruction"],
                ["rotation_axis_position", "enable_halftomo", "start_x", "end_x",
                 "start_y", "end_y", "start_z", "end_z"]
            )
            options["build_sino"]["axis_correction"] = dataset_infos.axis_correction
            tasks.append("reconstruction")
            # Iterative is not supported through configuration file for now.
            options["reconstruction"] = copy_dict_items(
                nabu_config["reconstruction"],
                ["method", "rotation_axis_position", "fbp_filter_type",
                "padding_type", "enable_halftomo",
                "start_x", "end_x", "start_y", "end_y", "start_z", "end_z"]
            )
            rec_options = options["reconstruction"]
            rec_options["rotation_axis_position"] = dataset_infos.axis_position
            options["build_sino"]["rotation_axis_position"] = dataset_infos.axis_position
            rec_options["axis_correction"] = dataset_infos.axis_correction
            rec_options["angles"] = dataset_infos.reconstruction_angles
            rec_options["radio_dims_y_x"] = dataset_infos.radio_dims[::-1]
            rec_options["pixel_size_cm"] = dataset_infos.pixel_size * 1e-4 # pix size is in microns
            if rec_options["enable_halftomo"]:
                rec_options["angles"] = rec_options["angles"][:rec_options["angles"].size//2]
                cor_i = int(round(rec_options["rotation_axis_position"]))
                # New key
                rec_options["rotation_axis_position_halftomo"] = (2*cor_i-1)/2.
            # New key
            rec_options["cor_estimated_auto"] = (nabu_config["reconstruction"]["rotation_axis_position"] == "auto")


        if nabu_config["output"]["location"] is not None:
            tasks.append("save")
            options["save"] = copy_dict_items(
                nabu_config["output"], list(nabu_config["output"].keys())
            )
            options["save"]["overwrite"] = nabu_config["output"]["overwrite_results"]

        # "sub_region" is the same for all steps
        # ~ sub_region = options["read_chunk"]["sub_region"]
        # ~ for step in options.keys():
            # ~ options[step]["sub_region"] = sub_region

        self.processing_steps = tasks
        self.processing_options = options
