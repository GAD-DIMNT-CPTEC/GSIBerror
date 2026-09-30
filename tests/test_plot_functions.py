from types import SimpleNamespace

import numpy as np
import pytest
import xarray as xr

from gsiberror.plot_functions import global_minmax, var_name


def matrix(values):
    array = xr.DataArray(np.asarray(values))
    return SimpleNamespace(
        amplitudes={"q": array},
        balprojs={"wgvin": array},
        hscales={"sf": array},
        vscales={"sf": array},
    )


def test_var_name_rejects_unknown_variable():
    with pytest.raises(ValueError, match="Unknown variable"):
        var_name("invalid")


def test_global_minmax_applies_plot_unit_conversion():
    matrices = [matrix([1, 2]), matrix([-3, 4])]

    assert global_minmax(matrices, "amplitudes", "q", scale=100) == (-300, 400)
    assert global_minmax(matrices, "hscales", "sf", scale=0.001) == (-0.003, 0.004)


def test_global_minmax_validates_inputs():
    with pytest.raises(ValueError, match="At least one"):
        global_minmax([], "amplitudes", "q")
    with pytest.raises(ValueError, match="Unknown data collection"):
        global_minmax([matrix([1])], "invalid", "q")
