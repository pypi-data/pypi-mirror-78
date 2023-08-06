from silx.opencl.backprojection import Backprojection

# Compatibility layer Nabu/silx
def Backprojector(
    sino_shape,
    slice_shape=None,
    angles=None,
    rot_center=None,
    filter_name=None,
    slice_roi=None,
    scale_factor=None,
    ctx=None,
    devicetype="all",
    platformid=None,
    deviceid=None,
    profile=False,
    extra_options=None,
):
    if slice_roi:
        raise ValueError("Not implemented yet in the OpenCL back-end")
    B = Backprojection(
        sino_shape,
        slice_shape=slice_shape,
        axis_position=rot_center, #
        angles=angles,
        filter_name=filter_name,
        ctx=ctx,
        devicetype=devicetype,
        platformid=platformid,
        deviceid=deviceid,
        profile=profile,
        extra_options=extra_options,
    )
    # Temporary patch ! The scale factor should be implemented in the opencl code
    if scale_factor is not none:
        B._old_fbp = B.filtered_backprojection
        def fbp_with_scale_factor(sino, output=None):
            return B._old_fbp(sino * scale_factor, output=output)
        B.filtered_backprojection = fbp_with_scale_factor
    #

    # Alias
    B.fbp = B.filtered_backprojection
    return B
