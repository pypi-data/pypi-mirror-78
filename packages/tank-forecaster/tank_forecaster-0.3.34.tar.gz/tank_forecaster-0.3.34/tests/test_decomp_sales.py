from tank_forecaster import decomp


def test_decompose_sales_none_returns_none():
    x = decomp.decompose_sales(None)
    assert x is None


def test_decompose_sales_little_data_returns_lists(sales_little_data):
    x = decomp.decompose_sales(sales_little_data)
    assert len(x[0]) != 0
    assert len(x[1]) != 0
