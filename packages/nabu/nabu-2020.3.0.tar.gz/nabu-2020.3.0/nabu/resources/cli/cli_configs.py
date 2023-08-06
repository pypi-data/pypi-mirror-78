#
# Default configuration for CLI tools
#

# Default configuration for "bootstrap" command

BootstrapConfig = {
    "bootstrap": {
        "help": "Bootstrap a configuration file from scratch.",
        "action": "store_const",
        "const": 1,
    },
    "convert": {
        "help": "Convert a PyHST configuration file to a nabu configuration file.",
        "default": "",
    },
    "output": {
        "help": "Output filename",
        "default": "nabu.conf",
    },
    "nocomments": {
        "help": "Remove the comments in the configuration file (default: False)",
        "action": "store_const",
        "const": 1,
    },
    "level": {
        "help": "Level of options to embed in the configuration file. Can be 'required', 'optional', 'advanced'.",
        "default": "optional",
    },
}


# Default configuration for "validate" command

ValidateConfig = {
    "input_file": {
        "help": "Nabu input file",
        "mandatory": True,
    },
}


# Default configuration for "reconstruct" command

ReconstructConfig = {
    "input_file": {
        "help": "Nabu input file",
        "default": "",
        "mandatory": True,
    },
    "logfile": {
        "help": "Log file. Default is nabu.log",
        "default": "nabu.log",
    },
    "log_file": {
        "help": "Same as logfile. Deprecated, use --logfile instead.",
        "default": "nabu.log",
    },
    "slice": {
        "help": "Slice(s) indice(s) to reconstruct, in the format z1-z2. Default (empty) is the whole volume. This overwrites the configuration file start_z and end_z. You can also use --slice first, --slice last, --slice middle, and --slice all",
        "default": "",
    },
    # ~ "compute": {
        # ~ "help": "Computation distribution method. Can be 'local' or 'slurm'",
        # ~ "default": "local",
    # ~ },
    # ~ "nodes": {
        # ~ "help": "Number of computing nodes to use. Ignored if --compute is set to 'local'.",
        # ~ "default": 1,
        # ~ "type": int,
    # ~ },
    "energy": {
        "help": "Beam energy in keV. DEPRECATED, was used to patch missing fields in BCU HDF5 file.",
        "default": -1,
        "type": float,
    },
    "gpu_mem_fraction": {
        "help": "Which fraction of GPU memory to use. Default is 0.9.",
        "default": 0.9,
        "type": float,
    },
    "cpu_mem_fraction": {
        "help": "Which fraction of memory to use. Default is 0.9.",
        "default": 0.9,
        "type": float,
    },
    "use_phase_margin": {
        "help": "Whether to use a margin when performing phase retrieval. Defautl is True.",
        "default": True,
        "type": bool,
    },
}

