import numpy as np
import os
from itertools import product
from .resources.validators import convert_to_bool
from silx.resources import ExternalResources


utilstest = ExternalResources(
    project="nabu",
    url_base="http://www.silx.org/pub/nabu/data/",
    env_key="NABU_DATA",
    timeout=60
)

__big_testdata_dir__ = os.environ.get("NABU_BIGDATA_DIR")
if __big_testdata_dir__ is None or not(os.path.isdir(__big_testdata_dir__)):
    __big_testdata_dir__ = None

__do_long_tests__ = os.environ.get("NABU_LONG_TESTS", False)
if __do_long_tests__:
    __do_long_tests__ = convert_to_bool(__do_long_tests__)


def generate_tests_scenarios(configurations):
    """
    Generate "scenarios" of tests.

    The parameter is a dictionary where:
      - the key is the name of a parameter
      - the value is a list of possible parameters

    This function returns a list of dictionary where:
      - the key is the name of a parameter
      - the value is one value of this parameter
    """
    scenarios = [
        {
            key: val
            for key, val in zip(configurations.keys(), p_)
        }
        for p_ in product(*configurations.values())
    ]
    return scenarios


def get_data(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    return np.load(dataset_downloaded_path)


def get_big_data(filename):
    if __big_testdata_dir__ is None:
        return None
    return np.load(os.path.join(__big_testdata_dir__, filename))


def compare_arrays(arr1, arr2, tol, diff=None, absolute_value=True, percent=None, method="max", return_residual=False):
    """
    Utility to compare two arrays.

    Parameters
    ----------
    arr1: numpy.ndarray
        First array to compare
    arr2: numpy.ndarray
        Second array to compare
    tol: float
        Tolerance indicating whether arrays are close to eachother.
    diff: numpy.ndarray, optional
        Difference `arr1 - arr2`. If provided, this array is taken instead of `arr1`
        and `arr2`.
    absolute_value: bool, optional
        Whether to take absolute value of the difference.
    percent: float
        If set, a "relative" comparison is performed instead of a subtraction:
        `red(|arr1 - arr2|) / (red(|arr1|) * percent) < tol`
        where "red" is the reduction method (mean, max or median).
    method:
        Reduction method. Can be "max", "mean", or "median".

    Returns
    --------
    (is_close, residual) if return_residual is set to True
    is_close otherwise

    Examples
    --------
    When using method="mean" and absolute_value=True, this function computes
    the Mean Absolute Difference (MAD) metric.
    When also using percent=1.0, this computes the Relative Mean Absolute Difference
    (RMD) metric.
    """
    reductions = {
        "max": np.max,
        "mean": np.mean,
        "median": np.median,
    }
    if method not in reductions:
        raise ValueError("reduction method should be in %s" % str(list(reductions.keys())))
    if diff is None:
        diff = arr1 - arr2
    if absolute_value is not None:
        diff = np.abs(diff)
    residual = reductions[method](diff)
    if percent is not None:
        a1 = np.abs(arr1) if absolute_value else arr1
        residual /= reductions[method](a1)

    res = residual < tol
    if return_residual:
        res = res, residual
    return res
