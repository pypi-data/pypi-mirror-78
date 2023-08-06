#!/usr/bin/env python

from ... import version
from .utils import parse_params_values
from ..utils import is_hdf5_extension
from .cli_configs import ReconstructConfig

def get_subregion(slices_indices, radio_nz):
    if len(slices_indices) == 0:
        return (0, radio_nz-1)
    if slices_indices == "all":
        return (0, radio_nz-1)
    if slices_indices == "first":
        return (0, 0)
    if slices_indices == "middle":
        return (radio_nz // 2, radio_nz // 2)
    if slices_indices == "last":
        return (radio_nz-1, radio_nz-1)
    try:
        if "-" in slices_indices:
            z_start, z_stop = slices_indices.split("-")
            z_start = int(z_start)
            z_stop = int(z_stop)
        else:
            z_idx = int(slices_indices)
            z_start = z_idx
            z_stop = z_idx
    except Exception as exc:
        print("Could not interpret slice indices: %s")
        print(exc)
        exit(1)
    return (z_start, z_stop)


def get_reconstruction_region(arg_slice, process_config, logger):
    n_z = process_config.dataset_infos._radio_dims_notbinned[-1]
    rec_opts = process_config.nabu_config["reconstruction"]

    if arg_slice == "":
        subregion = (rec_opts["start_z"], rec_opts["end_z"])
    else:
        # Overwrite config "start_z" and "end_z". Should this be deprecated ?
        subregion = get_subregion(
            arg_slice,
            process_config.dataset_infos.radio_dims[-1]
        )
        start_z, end_z = subregion
        logger.info(
            "Overwriting config file start_z to %d and end_z to %d"
            % (start_z, end_z)
        )
        process_config.nabu_config["reconstruction"]["start_z"] = start_z
        process_config.nabu_config["reconstruction"]["end_z"] = end_z

    delta_z = subregion[-1] - subregion[-2]

    _, radio_nz = process_config.dataset_infos.radio_dims
    if subregion[0] >= radio_nz or subregion[1] >= radio_nz:
        msg = str(
            "Reconstruction outside range: asked [zmin, zmax] = [%d, %d] but detector vertical dimension is %d"
            % (subregion[0], subregion[1], radio_nz)
        )
        logger.fatal(msg)
        raise ValueError(msg)

    return subregion


def get_log_file(arg_logfile, legacy_arg_logfile, forbidden=None):
    default_arg_val = "nabu.log"
    # Compat. log_file --> logfile
    if legacy_arg_logfile != default_arg_val:
        logfile = legacy_arg_logfile
    else:
        logfile = arg_logfile
    #
    if forbidden is None:
        forbidden = []
    for forbidden_val in forbidden:
        if logfile == forbidden_val:
            print("Error: --logfile argument cannot have the value %s" % forbidden_val)
            exit(1)
    return logfile


def main():
    args = parse_params_values(
        ReconstructConfig,
        parser_description="Perform a tomographic reconstruction.",
        program_version="nabu " + version
    )

    # Imports are done here, otherwise "nabu --version" takes forever
    from ...resources.processconfig import ProcessConfig
    from ...cuda.utils import __has_pycuda__
    if __has_pycuda__:
        from ...app.local_reconstruction import LocalReconstruction
    else:
        print("Error: need cuda and pycuda for reconstruction")
        exit(1)
    from ..logger import Logger
    #

    # A crash with scikit-cuda happens only on PPC64 platform if and nvidia-persistenced is running.
    # On such machines, a warm-up has to be done.
    import platform
    if platform.machine() == "ppc64le":
        from silx.math.fft.cufft import CUFFT
    #

    proc = ProcessConfig(args["input_file"])
    logfile = get_log_file(args["logfile"], args["log_file"], forbidden=[args["input_file"]])

    logger = Logger(
        "nabu",
        level=proc.nabu_config["about"]["verbosity"],
        logfile=logfile
    )

    subregion = get_reconstruction_region(args["slice"].strip(), proc, logger)
    logger.info("Going to reconstruct slices %s" % str(subregion))
    subregion = (None, None) + subregion

    # (hopefully) temporary patch
    if "phase" in proc.processing_steps:
        if args["energy"] > 0:
            logger.warning("Using user-provided energy %.2f keV" % args["energy"])
            proc.dataset_infos.dataset_scanner._energy = args["energy"]
            proc.processing_options["phase"]["energy_kev"] = args["energy"]
        if proc.dataset_infos.energy  < 1e-3 and proc.nabu_config["phase"]["method"] != None:
            msg = "No information on energy. Cannot retrieve phase. Please use the --energy option"
            logger.fatal(msg)
            raise ValueError(msg)
    #

    R = LocalReconstruction(
        proc,
        logger=logger,
        extra_options={
            "gpu_mem_fraction": args["gpu_mem_fraction"],
            "cpu_mem_fraction": args["cpu_mem_fraction"],
            "use_phase_margin": args["use_phase_margin"],
        }
    )

    R.reconstruct()
    if is_hdf5_extension(proc.nabu_config["output"]["file_format"]):
        R.merge_hdf5_reconstructions()




if __name__ == "__main__":
    main()
