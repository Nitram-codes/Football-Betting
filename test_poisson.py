from poisson import poisson_calc
import pytest


def test_poisson_calc():

    """Tests that the function returns the expected result for valid input"""

    actual_result = poisson_calc(2, 1.6)
    expected_result = 0.25842754303316

    assert expected_result == pytest.approx(actual_result)