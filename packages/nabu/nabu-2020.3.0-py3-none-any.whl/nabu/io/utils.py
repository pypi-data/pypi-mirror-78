import numpy as np
from silx.io.url import DataUrl


def get_compacted_dataslices(urls, subsampling=None):
    """
    Regroup urls to get the data more efficiently.
    Build a structure mapping files indices to information on
    how to load the data: `{indices_set: data_location}`
    where `data_location` contains contiguous indices.

    Parameters
    -----------
    urls: dict
        Dictionary where the key is an integer and the value is a silx `DataUrl`.
    subsampling: int, optional
        Subsampling factor when reading the frames. If an integer `n` is provided,
        then one frame out of `n` will be read.

    Returns
    --------
    merged_urls: dict
        Dictionary with the same keys as the `urls` parameter, and where the
        values are the corresponding `silx.io.url.DataUrl` with merged data_slice.
    """
    def _convert_to_slice(idx):
        if np.isscalar(idx):
            return slice(idx, idx+1)
        # otherwise, assume already slice object
        return idx

    def is_contiguous_slice(slice1, slice2):
        if np.isscalar(slice1):
            slice1 = slice(slice1, slice1+1)
        if np.isscalar(slice2):
            slice2 = slice(slice2, slice2+1)
        return slice2.start == slice1.stop

    def merge_slices(slice1, slice2):
        return slice(slice1.start, slice2.stop)

    sorted_files_indices = sorted(urls.keys())
    idx0 = sorted_files_indices[0]
    first_url = urls[idx0]

    merged_indices = [
        [idx0]
    ]
    data_location = [
        [
            first_url.file_path(),
            first_url.data_path(),
            _convert_to_slice(first_url.data_slice())
        ]
    ]
    pos = 0
    curr_fp, curr_dp, curr_slice = data_location[pos]
    for idx in sorted_files_indices[1:]:
        url = urls[idx]
        next_slice = _convert_to_slice(url.data_slice())
        if (url.file_path() == curr_fp) and (url.data_path() == curr_dp) and is_contiguous_slice(curr_slice, next_slice):
            merged_indices[pos].append(idx)
            merged_slices = merge_slices(curr_slice, next_slice)
            data_location[pos][-1] = merged_slices
            curr_slice = merged_slices
        else: # "jump"
            pos += 1
            merged_indices.append([idx])
            data_location.append([
                url.file_path(), url.data_path(), _convert_to_slice(url.data_slice())
            ])
            curr_fp, curr_dp, curr_slice = data_location[pos]

    # Format result
    res = {}
    for ind, dl in zip(merged_indices, data_location):
        # res[tuple(ind)] = DataUrl(file_path=dl[0], data_path=dl[1], data_slice=dl[2])
        res.update(
            dict.fromkeys(ind, DataUrl(file_path=dl[0], data_path=dl[1], data_slice=dl[2]))
        )

    if subsampling is None or subsampling <= 1:
        return res

    # Subsample
    next_pos = 0
    for idx in sorted_files_indices:
        url = res[idx]
        url_str = str(url)
        ds = url.data_slice()
        res[idx] = DataUrl(
            file_path=url.file_path(), data_path=url.data_path(),
            data_slice=slice(next_pos + ds.start, ds.stop, subsampling)
        )
        n_imgs = ds.stop - (ds.start + next_pos)
        next_pos = abs(-n_imgs % subsampling)

    return res
