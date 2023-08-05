import pandas

from tank_forecaster import decomp


def test_decomp_tank(tank_full_data):
    x = decomp.decompose_tank(tank_full_data)
    assert type(x) is pandas.core.frame.DataFrame
