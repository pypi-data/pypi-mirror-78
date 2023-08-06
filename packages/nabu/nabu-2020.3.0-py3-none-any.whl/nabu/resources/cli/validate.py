#!/usr/bin/env python

"""
Validate: tool for validating a configuration file.
This tool will inspect each entry of the configuration file and ensure that:

   - The dataset can be accessed (and the output location is writeable)
   - The relevant metadata can be accessed (pixel size, energy, angles, ...)
   - Each value of the configuration file is correct (eg. invalid values)
"""

import os
from .utils import parse_params_values
from .cli_configs import ValidateConfig
from ...io.config import NabuConfigParser, validate_nabu_config
from ..dataset_analyzer import analyze_dataset
from ..dataset_validator import NabuValidator


def get_config(fname):
    if not(os.path.isfile(fname)):
        print("Error: file %s not found" % fname)
        exit(-1)
    parser = NabuConfigParser(fname)
    config = parser.conf_dict
    return config


# Obsolete with ProcessConfig
def validate_conffile(fname):
    # Read the configuration file and extract the key/values
    config = get_config(fname)

    # Validation step 1: check the config file alone
    config = validate_nabu_config(config)

    # Browse the dataset
    dataset_structure = analyze_dataset(config["dataset"]["location"])

    # Validation step 2: check the consistency of dataset and config file
    validator = NabuValidator(config, dataset_structure)
    validator.perform_all_checks()

    # Remove unused radios (modifies dataset_structure)
    validator.remove_unused_radios()

    return validator


# Obsolete with ProcessConfig
def validate_conffile_noexcept(fname, print_ok=True):
    try:
        validator = validate_conffile(fname)
    except Exception as exc:
        print("Error while checking %s:" % fname)
        print(exc)
        exit(-1)
    if print_ok:
        print("Configuration file %s is valid" % fname)
    return validator


def main():
    args = parse_params_values(
        ValidateConfig,
        parser_description="Validate a Nabu configuration file."
    )
    fname = args["input_file"]
    validate_conffile_noexcept(fname)

if __name__ == "__main__":
    main()
