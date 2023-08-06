from os import path, mkdir
import numpy as np
from ..resources.logger import LoggerOrPrint
from .utils import use_options, pipeline_step, WriterConfigurator
from ..utils import check_supported
from ..io.reader import ChunkReader
from ..preproc.ccd import FlatField, Log, CCDCorrection
from ..preproc.shift import VerticalShift
from ..preproc.double_flatfield import DoubleFlatField
from ..preproc.phase import PaganinPhaseRetrieval
from ..preproc.sinogram import SinoProcessing
from ..misc.unsharp import UnsharpMask
from ..resources.utils import is_hdf5_extension
# ~ from ..io.writer import Writers

class FullFieldPipeline:
    """
    Pipeline for "regular" full-field tomography.
    Data is processed by chunks. A chunk consists in K contiguous lines of all the radios.
    In parallel geometry, a chunk of K radios lines gives K sinograms,
    and equivalently K reconstructed slices.
    """

    FlatFieldClass = FlatField
    DoubleFlatFieldClass = DoubleFlatField
    CCDCorrectionClass = CCDCorrection
    PaganinPhaseRetrievalClass = PaganinPhaseRetrieval
    UnsharpMaskClass = UnsharpMask
    VerticalShiftClass = VerticalShift
    SinoProcessingClass = SinoProcessing
    MLogClass = Log
    FBPClass = None # For now we don't have a plain python/numpy backend for reconstruction

    def __init__(self, process_config, sub_region, logger=None, extra_options=None, phase_margin=None):
        """
        Initialize a Full-Field pipeline.

        Parameters
        ----------
        processing_config: `nabu.resources.processcinfig.ProcessConfig`
            Process configuration.
        sub_region: tuple
            Sub-region to process in the volume for this worker, in the format
            `(start_x, end_x, start_z, end_z)`.
        logger: `nabu.app.logger.Logger`, optional
            Logger class
        extra_options: dict, optional
            Advanced extra options.
        phase_margin: tuple, optional
            Margin to use when performing phase retrieval, in the form ((up, down), (left, right)).
            See also the documentation of PaganinPhaseRetrieval.
            If not provided, no margin is applied.


        Notes
        ------
        Using a `phase_margin` results in a lesser number of reconstructed slices.
        More specifically, if `phase_margin = (V, H)`, then there will be `delta_z - 2*V`
        reconstructed slices (if the sub-region is in the middle of the volume)
        or `delta_z - V` reconstructed slices (if the sub-region is on top or bottom
        of the volume).
        """
        self.logger = LoggerOrPrint(logger)
        self._set_params(process_config, sub_region, extra_options, phase_margin)
        self.set_subregion(sub_region)
        self._init_pipeline()


    def _set_params(self, process_config, sub_region, extra_options, phase_margin):
        self.process_config = process_config
        self.dataset_infos = self.process_config.dataset_infos
        self.processing_steps = self.process_config.processing_steps.copy()
        self.processing_options = self.process_config.processing_options
        self.sub_region = self._check_subregion(sub_region)
        self.delta_z = sub_region[-1] - sub_region[-2]
        self.chunk_size = self.delta_z
        self._set_phase_margin(phase_margin)
        self._set_extra_options(extra_options)
        self._orig_file_prefix = None
        self._callbacks = {}
        self._steps_name2component = {}
        self._steps_component2name = {}


    @staticmethod
    def _check_subregion(sub_region):
        if len(sub_region) < 4:
            assert len(sub_region) == 2
            sub_region = (None, None) + sub_region
        if None in sub_region[-2:]:
            raise ValueError("Cannot set z_min or z_max to None")
        return sub_region


    def _set_extra_options(self, extra_options):
        if extra_options is None:
            extra_options = {}
        advanced_options = {}
        advanced_options.update(extra_options)
        self.extra_options = advanced_options


    def _set_phase_margin(self, phase_margin):
        if phase_margin is None:
            phase_margin = ((0, 0), (0, 0))
        self._phase_margin_up = phase_margin[0][0]
        self._phase_margin_down = phase_margin[0][1]
        self._phase_margin_left = phase_margin[1][0]
        self._phase_margin_right = phase_margin[1][1]


    def set_subregion(self, sub_region):
        """
        Set a sub-region to process.

        Parameters
        ----------
        sub_region: tuple
            Sub-region to process in the volume, in the format
            `(start_x, end_x, start_z, end_z)` or `(start_z, end_z)`.
        """
        sub_region = self._check_subregion(sub_region)
        dz = sub_region[-1] - sub_region[-2]
        if dz != self.delta_z:
            raise ValueError(
                "Class was initialized for delta_z = %d but provided sub_region has delta_z = %d"
                % (self.delta_z, dz)
            )
        self.sub_region = sub_region
        self.z_min = sub_region[-2]
        self.z_max = sub_region[-1]


    def _compute_phase_kernel_margin(self):
        """
        Get the "margin" to pass to classes like PaganinPhaseRetrieval.
        In order to have a good accuracy for filter-based phase retrieval methods,
        we need to load extra data around the edges of each image. Otherwise,
        a default padding type is applied.
        """
        if "phase" not in self.processing_steps:
            self._phase_margin = None
            return
        up_margin = self._phase_margin_up
        down_margin = self._phase_margin_down
        # Horizontal margin is not implemented
        left_margin, right_margin = (0, 0)
        self._phase_margin = ((up_margin, down_margin), (left_margin, right_margin))


    def _get_phase_margin(self):
        if "phase" not in self.processing_steps:
            return ((0, 0), (0, 0))
        return self._phase_margin


    def _get_cropped_radios(self):
        ((up_margin, down_margin), (left_margin, right_margin)) = self._phase_margin
        zslice = slice(up_margin or None, -down_margin or None)
        xslice = slice(left_margin or None, -right_margin or None)
        self._radios_cropped = self.radios[:, zslice, xslice]
        return self._radios_cropped


    @property
    def phase_margin(self):
        """
        Return the margin for phase retrieval in the form ((up, down), (left, right))
        """
        return self._get_phase_margin()


    @property
    def n_recs(self):
        """
        Return the final number of reconstructed slices.
        """
        n_recs = self.delta_z
        n_recs -= sum(self._get_phase_margin()[0])
        return n_recs


    def _get_process_name(self):
        # TODO support "incomplete" processing pipeline
        return "reconstruction"


    def register_callback(self, step_name, callback):
        """
        Register a callback for a pipeline processing step.

        Parameters
        ----------
        step_name: str
            processing step name
        callback: callable
            A function. It will be executed once the processing step `step_name`
            is finished. The function takes only one argument: the class instance.
        """
        if step_name not in self.processing_steps:
            raise ValueError(
                "'%s' is not in processing steps %s"
                % (step_name, self.processing_steps)
            )
        if step_name in self._callbacks:
            self.logger.warning("Overwriting existing callback for %s" % step_name)
        self._callbacks[step_name] = callback


    def _reshape_radios_after_phase(self):
        """
        Callback executed after phase retrieval, if margin != (0, 0).
        It modifies self.radios so that further processing will be done
        on the "inner part".
        """
        if sum(self._get_phase_margin()[0]) <= 0:
            return
        self._orig_radios = self.radios
        self.logger.debug(
            "Reshaping radios from %s to %s"
            % (str(self.radios.shape), str(self._radios_cropped.shape))
        )
        self.radios = self._radios_cropped

    #
    # Likely overwritten in inheriting classes
    #

    def _get_shape(self, step_name):
        """
        Get the shape to provide to the class corresponding to step_name.
        """
        if step_name == "flatfield":
            shape = self.radios.shape
        elif step_name == "double_flatfield":
            shape = self.radios.shape
        elif step_name == "phase":
            shape = self.radios.shape[1:]
        elif step_name == "ccd_correction":
            shape = self.radios.shape[1:]
        elif step_name == "unsharp_mask":
            shape = self.radios.shape[1:]
        elif step_name == "take_log":
            shape = self._radios_cropped_shape
        elif step_name == "radios_movements":
            shape = self._radios_cropped_shape
        elif step_name == "build_sino":
            shape = self._radios_cropped_shape
        elif step_name == "reconstruction":
            shape = self.sino_builder.output_shape[1:]
        else:
            raise ValueError("Unknown processing step %s" % step_name)
        self.logger.debug("Data shape for %s is %s" % (step_name, str(shape)))
        return shape

    def _get_phase_output_shape(self):
        if "phase" not in self.processing_steps:
            self._radios_cropped_shape = self.radios.shape
            return
        ((up_margin, down_margin), (left_margin, right_margin)) = self._phase_margin
        self._radios_cropped_shape = (
            self.radios.shape[0],
            self.radios.shape[1] - (up_margin + down_margin),
            self.radios.shape[2] - (left_margin + right_margin)
        )

    def _allocate_array(self, shape, dtype, name=None):
        return np.zeros(shape, dtype=dtype)

    def _allocate_sinobuilder_output(self):
        return self._allocate_array(self.sino_builder.output_shape, "f", name="sinos")

    def _allocate_recs(self, ny, nx):
        self.n_slices = self.radios.shape[1]  # TODO modify with vertical shifts
        if "phase" in self.processing_steps:
            self.n_slices -= sum(self.phase_margin[0])
        self.recs = self._allocate_array((self.n_slices, ny, nx), "f", name="recs")

    def _reset_memory(self):
        pass

    def _init_reader_finalize(self):
        """
        Method called after _init_reader
        """
        self.radios = self.chunk_reader.files_data
        self._compute_phase_kernel_margin()
        self._get_phase_output_shape()


    def _process_finalize(self):
        """
        Method called once the pipeline has been executed
        """
        pass

    #
    # Pipeline initialization
    #

    def _init_pipeline(self):
        self._init_reader()
        self._init_flatfield()
        self._init_double_flatfield()
        self._init_ccd_corrections()
        self._init_phase()
        self._init_unsharp()
        self._init_radios_movements()
        self._init_mlog()
        self._init_sino_builder()
        self._prepare_reconstruction()
        self._init_reconstruction()
        self._init_writer()

    @use_options("read_chunk", "chunk_reader")
    def _init_reader(self):
        if "read_chunk" not in self.processing_steps:
            raise ValueError("Cannot proceed without reading data")
        options = self.processing_options["read_chunk"]
        # ChunkReader always take a non-subsampled dictionary "files"
        self.chunk_reader = ChunkReader(
            options["files"],
            sub_region=self.sub_region,
            convert_float=True,
            binning=options["binning"],
            dataset_subsampling=options["dataset_subsampling"]
        )
        self._init_reader_finalize()

    @use_options("flatfield", "flatfield")
    def _init_flatfield(self, shape=None):
        if shape is None:
            shape = self._get_shape("flatfield")
        options = self.processing_options["flatfield"]
        # FlatField parameter "radios_indices" must account for subsampling
        self.flatfield = self.FlatFieldClass(
            shape,
            flats=self.dataset_infos.flats,
            darks=self.dataset_infos.darks,
            radios_indices=options["projs_indices"],
            interpolation="linear",
            sub_region=self.sub_region,
            binning=options["binning"],
            convert_float=True
        )

    @use_options("double_flatfield", "double_flatfield")
    def _init_double_flatfield(self):
        options = self.processing_options["double_flatfield"]
        self.double_flatfield = self.DoubleFlatFieldClass(
            self._get_shape("double_flatfield"),
            result_url=None,
            input_is_mlog=False,
            output_is_mlog=False,
            average_is_on_log=False,
            sigma_filter=options["sigma"]
        )

    @use_options("ccd_correction", "ccd_correction")
    def _init_ccd_corrections(self):
        options = self.processing_options["ccd_correction"]
        self.ccd_correction = self.CCDCorrectionClass(
            self._get_shape("ccd_correction"),
            median_clip_thresh=options["median_clip_thresh"]
        )

    @use_options("phase", "phase_retrieval")
    def _init_phase(self):
        options = self.processing_options["phase"]
        # If unsharp mask follows phase retrieval, then it should be done
        # before cropping to the "inner part".
        # Otherwise, crop the data just after phase retrieval.
        if "unsharp_mask" in self.processing_steps:
            margin = None
        else:
            margin=self._phase_margin
        self.phase_retrieval = self.PaganinPhaseRetrievalClass(
            self._get_shape("phase"),
            distance=options["distance_cm"],
            energy=options["energy_kev"],
            delta_beta=options["delta_beta"],
            pixel_size=options["pixel_size_microns"],
            padding=options["padding_type"],
            margin=margin,
        )
        if "unsharp_mask" not in self.processing_steps:
            self.register_callback("phase", self._reshape_radios_after_phase)

    @use_options("unsharp_mask", "unsharp_mask")
    def _init_unsharp(self):
        options = self.processing_options["unsharp_mask"]
        self.unsharp_mask = self.UnsharpMaskClass(
            self._get_shape("unsharp_mask"),
            options["unsharp_sigma"], options["unsharp_coeff"],
            mode="reflect", method="gaussian"
        )
        self.register_callback("unsharp_mask", self._reshape_radios_after_phase)

    @use_options("take_log", "mlog")
    def _init_mlog(self):
        options = self.processing_options["take_log"]
        self.mlog = self.MLogClass(
            self._get_shape("take_log"),
            clip_min=options["log_min_clip"],
            clip_max=options["log_max_clip"]
        )

    @use_options("radios_movements", "radios_movements")
    def _init_radios_movements(self):
        options = self.processing_options["radios_movements"]
        self._vertical_shifts = options["translation_movements"][:, 1]
        self.radios_movements = self.VerticalShiftClass(
            self._get_shape("radios_movements"),
            self._vertical_shifts
        )

    @use_options("build_sino", "sino_builder")
    def _init_sino_builder(self):
        options = self.processing_options["build_sino"]
        self.sino_builder = self.SinoProcessingClass(
            radios_shape=self._get_shape("build_sino"),
            rot_center=options["rotation_axis_position"],
            halftomo=options["enable_halftomo"],
        )
        if not(options["enable_halftomo"]):
            self._sinobuilder_copy = False
            self._sinobuilder_output = None
            self.sinos = None
        else:
            self._sinobuilder_copy = True
            self.sinos = self._allocate_sinobuilder_output()
            self._sinobuilder_output = self.sinos

    @use_options("reconstruction", "reconstruction")
    def _prepare_reconstruction(self):
        options = self.processing_options["reconstruction"]
        x_s, x_e = options["start_x"], options["end_x"]+1
        y_s, y_e = options["start_y"], options["end_y"]+1
        self._rec_roi = (x_s, x_e, y_s, y_e)
        self._allocate_recs(y_e - y_s, x_e - x_s)

    @use_options("reconstruction", "reconstruction")
    def _init_reconstruction(self):
        options = self.processing_options["reconstruction"]
        # TODO account for reconstruction from already formed sinograms
        if self.sino_builder is None:
            raise ValueError("Reconstruction cannot be done without build_sino")

        if options["enable_halftomo"]:
            rot_center = options["rotation_axis_position_halftomo"]
        else:
            rot_center = options["rotation_axis_position"]
        if options.get("cor_estimated_auto", False):
            self.logger.info("Estimated center of rotation: %.2f" % rot_center)

        self.reconstruction = self.FBPClass(
            self._get_shape("reconstruction"),
            angles=options["angles"],
            rot_center=rot_center,
            filter_name=options["fbp_filter_type"],
            slice_roi=self._rec_roi,
            scale_factor=1./options["pixel_size_cm"],
            extra_options={
                "padding_mode": options["padding_type"],
                "axis_correction": options["axis_correction"],
            }
        )
        if options["fbp_filter_type"] == "none":
            self.reconstruction.fbp = self.reconstruction.backproj

    @use_options("save", "writer")
    def _init_writer(self):
        options = self.processing_options["save"]
        # Set file prefix for current chunk
        if self._orig_file_prefix is None:
            self._orig_file_prefix = options["file_prefix"]
        output_dir = path.join(
            options["location"],
            self._orig_file_prefix
        )

        nx_info = None
        if is_hdf5_extension(options["file_format"]):
            fname_start_index = None
            options["file_prefix"] = self._orig_file_prefix + str(
                "_%04d" % (self.z_min + self._phase_margin_up)
            )
            entry = getattr(self.dataset_infos.dataset_scanner, "entry", None)
            nx_info = {
                "process_name": self._get_process_name(),
                "processing_index": 0,
                "config": {
                    "processing_options": self.processing_options,
                    "nabu_config": self.process_config.nabu_config
                },
                "entry": entry,
            }
        else:
            fname_start_index = self.z_min + self._phase_margin_up

        self._writer_configurator = WriterConfigurator(
            options, output_dir=output_dir, start_index=fname_start_index,
            logger=self.logger, nx_info=nx_info
        )
        self.writer = self._writer_configurator.writer
        self._writer_exec_args = self._writer_configurator._writer_exec_args
        self._writer_exec_kwargs = self._writer_configurator._writer_exec_kwargs

    #
    # Pipeline re-initialization
    #

    def _reset_sub_region(self, sub_region):
        self.set_subregion(sub_region)
        # Reader
        self.chunk_reader._set_subregion(self.sub_region)
        self.chunk_reader._init_reader()
        self.chunk_reader._loaded = False
        # Flat-field
        self._reset_flatfield()

    def _reset_flatfield(self):
        self._init_flatfield()

    #
    # Pipeline execution
    #

    @pipeline_step("chunk_reader", "Reading data")
    def _read_data(self):
        self.logger.debug("Region = %s" % str(self.sub_region))
        self.chunk_reader.load_files()

    @pipeline_step("flatfield", "Applying flat-field")
    def _flatfield(self):
        self.flatfield.normalize_radios(self.radios)

    @pipeline_step("double_flatfield", "Applying double flat-field")
    def _double_flatfield(self, radios=None):
        if radios is None:
            radios = self.radios
        self.double_flatfield.apply_double_flatfield(radios)

    @pipeline_step("ccd_correction", "Applying double CCD corrections")
    def _ccd_corrections(self, radios=None):
        if radios is None:
            radios = self.radios
        _tmp_radio = self._allocate_array(radios.shape[1:], "f", name="tmp_ccdcorr_radio")
        for i in range(radios.shape[0]):
            self.ccd_correction.median_clip_correction(
                radios[i], output=_tmp_radio
            )
            radios[i][:] = _tmp_radio[:]

    @pipeline_step("phase_retrieval", "Performing phase retrieval")
    def _retrieve_phase(self):
        if "unsharp_mask" in self.processing_steps:
            output = self.radios
        else:
            self._get_cropped_radios()
            output = self._radios_cropped
        for i in range(self.radios.shape[0]):
            self.phase_retrieval.apply_filter(
                self.radios[i], output=output[i]
            )

    @pipeline_step("unsharp_mask", "Performing unsharp mask")
    def _apply_unsharp(self):
        for i in range(self.radios.shape[0]):
            self.radios[i] = self.unsharp_mask.unsharp(self.radios[i])
        self._get_cropped_radios()

    @pipeline_step("mlog", "Taking logarithm")
    def _take_log(self):
        self.mlog.take_logarithm(self.radios)


    @pipeline_step("radios_movements", "Applying radios movements")
    def _radios_movements(self, radios=None):
        if radios is None:
            radios = self.radios
        self.radios_movements.apply_vertical_shifts(
            radios, list(range(radios.shape[0]))
        )

    @pipeline_step("sino_builder", "Building sinograms")
    def _build_sino(self, radios=None):
        if radios is None:
            radios = self.radios
        # Either a new array (previously allocated in "_sinobuilder_output"),
        # or a view of "radios"
        self.sinos = self.sino_builder.radios_to_sinos(
            radios,
            output=self._sinobuilder_output,
            copy=self._sinobuilder_copy
        )

    @pipeline_step("reconstruction", "Reconstruction")
    def _reconstruct(self, sinos=None):
        if sinos is None:
            sinos = self.sinos
        for i in range(sinos.shape[0]):
            self.reconstruction.fbp(
                sinos[i], output=self.recs[i]
            )

    @pipeline_step("writer", "Saving data")
    def _write_data(self, data=None):
        if data is None:
            data = self.recs
        self.writer.write(data, *self._writer_exec_args, **self._writer_exec_kwargs)
        self.logger.info("Wrote %s" % self.writer.get_filename())
        self.processing_options["save"]["file_prefix"] = self._orig_file_prefix


    def _process_chunk(self):
        self._flatfield()
        self._double_flatfield()
        self._ccd_corrections()
        self._retrieve_phase()
        self._apply_unsharp()
        self._take_log()
        self._radios_movements()
        self._build_sino()
        self._reconstruct()
        self._write_data()
        self._process_finalize()


    def process_chunk(self, sub_region=None):
        if sub_region is not None:
            self._reset_sub_region(sub_region)
            self._reset_memory()
            self._init_writer()
            self._init_double_flatfield()
        self._read_data()
        self._process_chunk()

