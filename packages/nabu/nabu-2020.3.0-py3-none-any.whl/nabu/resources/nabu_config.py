from .validators import *
from .. import __version__, __config_version__

#
# option "type":
#  - required: always visible, user must provide a valid value
#  - optional: visible, but might be left blank
#  - advanced: optional and not visible by default
#  - unsupported: hidden (not implemented yet)
_options_levels = {
    "required": 0,
    "optional": 1,
    "advanced": 2,
    "unsupported": 10,
}


nabu_config = {
    "dataset": {
        "location": {
            "default": "",
            "help": "Dataset folder location",
            "validator": dataset_location_validator,
            "type": "required",
        },
        "binning": {
            "default": "1",
            "help": "Binning factor in the horizontal dimension when reading the data.\nThe final slices dimensions will be divided by 'slices_binning'",
            "validator": binning_validator,
            "type": "advanced",
        },
        "binning_z": {
            "default": "1",
            "help": "Binning factor in the vertical dimension when reading the data.\nThis retsults in a lesser number of reconstructed slices.",
            "validator": binning_validator,
            "type": "advanced",
        },
        "projections_subsampling": {
            "default": "1",
            "help": "Projections subsampling factor: take one projection out of 'projection_subsampling'",
            "validator": binning_validator,
            "type": "advanced",
        },
    },
    "preproc": {
        "flatfield_enabled": {
            "default": "1",
            "help": "Whether to enable flat-field normalization",
            "validator": boolean_validator,
            "type": "required",
        },
        "ccd_filter_enabled": {
            "default": "0",
            "help": "Whether to enable the CCD hotspots correction.",
            "validator": boolean_validator,
            "type": "optional",
        },
        "ccd_filter_threshold": {
            "default": "0.04",
            "help": "If ccd_filter_enabled = 1, a median filter is applied on the 3X3 neighborhood\nof every pixel. If a pixel value exceeds the median value more than this parameter,\nthen the pixel value is replaced with the median value.",
            "validator": float_validator,
            "type": "optional",
        },
        "double_flatfield_enabled": {
            "default": "0",
            "help": "Whether to enable the 'double flat-field' filetering for correcting rings artefacts.",
            "validator": boolean_validator,
            "type": "optional",
        },
        "dff_sigma": {
            "default": "",
            "help": "Enable high-pass filtering on double flatfield with this value of 'sigma'",
            "validator": optional_float_validator,
            "type": "advanced",
        },
        "take_logarithm": {
            "default": "1",
            "help": "Whether to take logarithm after flat-field and phase retrieval.",
            "validator": boolean_validator,
            "type": "required",
        },
        "log_min_clip": {
            "default": "1e-6",
            "help": "After division by the FF, and before the logarithm, the is clipped to this minimum. Enabled only if take_logarithm=1",
            "validator": float_validator,
            "type": "advanced",
        },
        "log_max_clip": {
            "default": "10.0",
            "help": "After division by the FF, and before the logarithm, the is clipped to this maximum. Enabled only if take_logarithm=1",
            "validator": float_validator,
            "type": "advanced",
        },
    },
    "phase": {
        "method": {
            "default": "none",
            "help": "Phase retrieval method. Available are: Paganin, None",
            "validator": phase_method_validator,
            "type": "required",
        },
        "delta_beta": {
            "default": "100.0",
            "help": "Single-distance phase retrieval related parameters\n----------------------------\ndelta/beta ratio for the Paganin/CTR method",
            "validator": float_validator,
            "type": "required",
        },
        "margin": {
            "default": "50",
            "help": "Margin (in pixels) in the Paganin/CTR filtering.",
            "validator": integer_validator,
            "type": "advanced",
        },
        "unsharp_coeff": {
            "default": "0",
            "help": "Unsharp mask strength. The unsharped image is equal to\n  UnsharpedImage =  (1 + coeff)*originalPaganinImage - coeff * ConvolvedImage. Setting this coefficient to zero means that no unsharp mask will be applied.",
            "validator": float_validator,
            "type": "optional",
        },
        "unsharp_sigma": {
            "default": "0",
            "help": "Standard deviation of the Gaussian filter when applying an unsharp mask\nafter the Paganin filtering. Disabled if set to 0.",
            "validator": float_validator,
            "type": "optional",
        },
        "padding_type": {
            "default": "edge",
            "help": "Padding type for the filtering step in Paganin/CTR. Available are: mirror, edge, zeros",
            "validator": padding_mode_validator,
            "type": "advanced",
        },
    },
    "reconstruction": {
        "method": {
            "default": "FBP",
            "help": "Reconstruction method. Possible values: FBP, none. If value is 'none', no reconstruction will be done.",
            "validator": reconstruction_method_validator,
            "type": "required",
        },
        "angles_file": {
            "default": "",
            "help": "In the case you want to override the angles found in the files metadata",
            "validator": optional_file_location_validator,
            "type": "optional",
        },
        "rotation_axis_position": {
            "default": "",
            "help": "Rotation axis position. Default is the middle of the detector width. If set to 'auto', nabu will attempt to determine it automatically.",
            "validator": cor_validator,
            "type": "required",
        },
        "axis_correction_file": {
            "default": "",
            "help": "In the case where the axis position is specified for each slice",
            "validator": optional_values_file_validator,
            "type": "advanced",
        },
        "translation_movements_file": {
            "default": "",
            "help": "A file where each line describes the translation in X and Z of the sample (or detector).",
            "validator": optional_values_file_validator,
            "type": "advanced",
        },
        "angle_offset": {
            "default": "0",
            "help": "Use this if you want to obtain a rotated reconstructed slice. The angle is in degrees.",
            "validator": float_validator,
            "type": "advanced",
        },
        "fbp_filter_type": {
            "default": "ramlak",
            "help": "Filter type for FBP method. Available are: ramlak, none",
            "validator": fbp_filter_name_validator,
            "type": "advanced",
        },
        "padding_type": {
            "default": "zeros",
            "help": "Padding type for FBP. Available are: zeros, edges",
            "validator": padding_mode_validator,
            "type": "optional", # put "advanced" with default value "edges" ?
        },
        "enable_halftomo": {
            "default": "0",
            "help": "Whether to enable half-acquisition",
            "validator": boolean_validator,
            "type": "optional",
        },
        "start_x": {
            "default": "0",
            "help": "\nParameters for sub-volume reconstruction. Indices start at 0 !\n----------------------------------------------------------------\n(x, y) are the dimension of a slice, and (z) is the 'vertical' axis\nBy default, all the volume is reconstructed slice by slice, along the axis 'z'.",
            "validator": nonnegative_integer_validator,
            "type": "optional",
        },
        "end_x": {
            "default": "-1",
            "help": "",
            "validator": integer_validator,
            "type": "optional",
        },
        "start_y": {
            "default": "0",
            "help": "",
            "validator": nonnegative_integer_validator,
            "type": "optional",
        },
        "end_y": {
            "default": "-1",
            "help": "",
            "validator": integer_validator,
            "type": "optional",
        },
        "start_z": {
            "default": "0",
            "help": "",
            "validator": nonnegative_integer_validator,
            "type": "optional",
        },
        "end_z": {
            "default": "-1",
            "help": "",
            "validator": integer_validator,
            "type": "optional",
        },
        "iterations": {
            "default": "200",
            "help": "\nParameters for iterative algorithms\n------------------------------------\nNumber of iterations",
            "validator": nonnegative_integer_validator,
            "type": "unsupported",
        },
        "optim_algorithm": {
            "default": "chambolle-pock",
            "help": "Optimization algorithm for iterative methods",
            "validator": optimization_algorithm_name_validator,
            "type": "unsupported",
        },
        "weight_tv": {
            "default": "1.0e-2",
            "help": "Total Variation regularization parameter for iterative methods",
            "validator": float_validator,
            "type": "unsupported",
        },
        "preconditioning_filter": {
            "default": "1",
            "help": "Whether to enable 'filter preconditioning' for iterative methods",
            "validator": boolean_validator,
            "type": "unsupported",
        },
        "positivity_constraint": {
            "default": "1",
            "help": "Whether to enforce a positivity constraint in the reconstruction.",
            "validator": boolean_validator,
            "type": "unsupported",
        },
    },
    "output": {
        "location": {
            "default": "",
            "help": "Directory where the output reconstruction is stored.",
            "validator": optional_directory_location_validator,
            "type": "required",
        },
        "file_prefix": {
            "default": "",
            "help": "File prefix. Optional, by default it is inferred from the scanned dataset.",
            "validator": optional_file_name_validator,
            "type": "optional",
        },
        "file_format": {
            "default": "hdf5",
            "help": "Output file format. Available are: hdf5, tiff, jp2",
            "validator": output_file_format_validator,
            "type": "optional",
        },
        "overwrite_results": {
            "default": "0",
            "help": "What to do in the case where the output file exists.\nBy default, the output data is never overwritten and the process is interrupted if the file already exists.\nSet this option to 1 if you want to overwrite without asking.",
            "validator": boolean_validator,
            "type": "required",
        },
    },
    "resources": {
        "method": {
            "default": "local",
            "help": "Computations distribution method. It can be:\n  - local:  run the computations on the local machine\n  - slurm: run the computations through SLURM\n  - preview: reconstruct the slices/volume as quickly as possible, possibly doing some binning.",
            "validator": distribution_method_validator,
            "type": "required",
        },
        "gpus": {
            "default": "1",
            "help": "Number of GPUs to use.",
            "validator": nonnegative_integer_validator,
            "type": "unsupported",
        },
        "gpu_id": {
            "default": "",
            "help": "For method = local only. List of GPU IDs to use. This parameter overwrites 'gpus'.\nIf left blank, exactly one GPU will be used, and the best one will be picked.",
            "validator": list_of_int_validator,
            "type": "unsupported",
        },
        "cpu_workers": {
            "default": "0",
            "help": "Number of 'CPU workers' for each GPU worker. It is discouraged to set this number to more than one. A value of -1 means exactly one CPU worker.",
            "validator": integer_validator,
            "type": "unsupported",
        },
        "memory_per_node": {
            "default": "90%",
            "help": "RAM memory per computing node, either in GB or in percent of the AVAILABLE (!= total) node memory.\nIf several workers share the same node, their combined memory usage will not exceed this number.",
            "validator": resources_validator,
            "type": "unsupported",
        },
        "threads_per_node": {
            "default": "100%",
            "help": "Number of threads to allocate on each node, either a number or a percentage of the available threads",
            "validator": resources_validator,
            "type": "unsupported",
        },
        "queue": {
            "default": "gpu",
            "help": "\nParameters exclusive to the 'slurm' distribution method\n------------------------------------------------------\nName of the SLURM partition ('queue'). Full list is obtained with 'scontrol show partition'",
            "validator": nonempty_string_validator,
            "type": "unsupported",
        },
        "walltime": {
            "default": "01:00:00",
            "help": "Time limit for the SLURM resource allocation, in the format Hours:Minutes:Seconds",
            "validator": walltime_validator,
            "type": "unsupported",
        },
    },
    "about": {
        "nabu_version": {
            "default": __version__,
            "help": "Version of the nabu software",
            "validator": no_validator,
            "type": "required",
        },
        "nabu_config_version": {
            "default": __config_version__,
            "help": "Version of the nabu configuration file",
            "validator": no_validator,
            "type": "required",
        },
        "verbosity": {
            "default": "2",
            "help": "Level of verbosity of the processing. 0 = terse, 3 = much information.",
            "validator": logging_validator,
            "type": "optional",
        },
    },
}

renamed_keys = {
    "marge": {
        "section": "phase",
        "new_name": "margin",
        "since": "2020.2.0",
        "message": "Option 'marge' has been renamed to 'margin' in [phase]",
    },
    "overwrite_results": {
        "section": "about",
        "new_name": "overwrite_results",
        "new_section": "output",
        "since": "2020.3.0",
        "message": "Option 'overwrite_results' was moved from section [about] to section [output]",
    }
}


deleted_keys = {}


