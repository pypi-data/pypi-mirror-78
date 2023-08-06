#!/usr/bin/env python

"""
computations.py: determine computational needs, chunking method to be used, etc.
"""

from silx.image.tomography import get_next_power


def estimate_required_memory(process_config, chunk_size=None, radios_and_slices=True):
    """
    Estimate the memory (RAM) needed for a reconstruction.

    Parameters
    -----------
    radios_and_slices: bool
        Whether radios and slices will co-exist in memory (meaning more memory usage)
    """
    dataset = process_config.dataset_infos
    nabu_config = process_config.nabu_config
    processing_steps = process_config.processing_steps
    Nx, Ny = dataset.radio_dims
    Na = dataset.n_angles
    if chunk_size is not None:
        Ny = chunk_size

    total_memory_needed = 0

    # Read data
    # ----------
    binning_z = nabu_config["dataset"]["binning_z"]
    projections_subsampling = nabu_config["dataset"]["projections_subsampling"]
    data_volume_size = Nx * Ny * Na * 4
    data_image_size = Nx * Ny * 4
    total_memory_needed += data_volume_size

    # CCD processing
    # ---------------
    if "flatfield" in processing_steps:
        # Flat-field is done in-place, but still need to load darks/flats
        n_darks = len(dataset.darks)
        n_flats = len(dataset.flats)
        darks_size = n_darks * Nx * Ny * 2  # uint16
        flats_size = n_flats * Nx * Ny * 4  # f32
        total_memory_needed += darks_size + flats_size

    if "ccd_correction" in processing_steps:
        # CCD filter is "batched 2D"
        total_memory_needed += data_image_size

    # Phase retrieval
    # ---------------
    if "phase" in processing_steps:
        # Phase retrieval is done image-wise, so near in-place, but needs to
        # allocate some images, fft plans, and so on
        Nx_p = get_next_power(2 * Nx)
        Ny_p = get_next_power(2 * Ny)
        img_size_real = 2 * 4 * Nx_p * Ny_p
        img_size_cplx = 2 * 8 * ((Nx_p * Ny_p) // 2 + 1)
        total_memory_needed += 2 * img_size_real + 3 * img_size_cplx

    # Reconstruction
    # ---------------
    reconstructed_volume_size = 0
    if "reconstruction" in processing_steps:
        if radios_and_slices:
            total_memory_needed += data_volume_size  # radios + sinos
        rec_config = process_config.processing_options["reconstruction"]
        if "rotation_axis_position_halftomo" in rec_config:
            # Slice has a different shape in half acquisition.
            # Not sure if start_x, ..., end_y  are supported
            Nx_rec = 2 * rec_config["rotation_axis_position_halftomo"]
            Ny_rec = Nx_rec
        else:
            Nx_rec = (rec_config["end_x"] - rec_config["start_x"] + 1)
            Ny_rec = (rec_config["end_y"] - rec_config["start_y"] + 1)
        Nz_rec = (rec_config["end_z"] - rec_config["start_z"] + 1) // binning_z
        if chunk_size:
            Nz_rec = chunk_size // binning_z
        reconstructed_volume_size = Nx_rec * Ny_rec * Nz_rec * 4  # float32
        total_memory_needed += reconstructed_volume_size

    return total_memory_needed

def estimate_chunk_size(available_memory_GB, process_config, chunk_step=50):
    """
    Estimate the maximum chunk size given an avaiable amount of memory.

    Parameters
    -----------
    available_memory_GB: float
        available memory in Giga Bytes (GB - not GiB !).
    process_config: ProcessConfig
        Instance of nabu.resources.processconfig.ProcessConfig
    """
    # Deriving a closed-form formula for estimate_required_memory would be cumbersome
    # so we use this inelegant way instead
    chunk_size = chunk_step
    radios_and_slices = False
    if (
        "reconstruction" in process_config.processing_steps
        and process_config.processing_options["reconstruction"]["enable_halftomo"]
    ):
        radios_and_slices = True

    max_dz = process_config.dataset_infos.radio_dims[1]
    chunk_size = chunk_step
    last_good_chunk_size = chunk_size
    while True:
        required_mem = estimate_required_memory(
            process_config, chunk_size=chunk_size, radios_and_slices=radios_and_slices
        )
        required_mem_GB = required_mem / 1e9
        if required_mem_GB > available_memory_GB or chunk_size > max_dz:
            break
        last_good_chunk_size = chunk_size
        chunk_size += chunk_step
    return last_good_chunk_size
