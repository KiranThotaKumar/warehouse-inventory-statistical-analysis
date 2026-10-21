
import pytest

from src.estimation import estimate_value_per_sqft


def test_value_per_sqft_calculation():
    result = {
        "estimated_total_value": 100000.0,
        "total_ci_lower": 90000.0,
        "total_ci_upper": 110000.0,
    }

    output = estimate_value_per_sqft(result, 10000)

    assert output["estimated_inventory_value_per_sqft"] == 10.0
    assert output["ci_lower_per_sqft"] == 9.0
    assert output["ci_upper_per_sqft"] == 11.0


def test_floor_area_must_be_positive():
    result = {
        "estimated_total_value": 100000.0,
        "total_ci_lower": 90000.0,
        "total_ci_upper": 110000.0,
    }

    with pytest.raises(ValueError):
        estimate_value_per_sqft(result, 0)


def test_floor_area_must_be_numeric():
    result = {
        "estimated_total_value": 100000.0,
        "total_ci_lower": 90000.0,
        "total_ci_upper": 110000.0,
    }

    with pytest.raises(TypeError):
        estimate_value_per_sqft(result, "10000")


def test_missing_estimation_fields():
    with pytest.raises(ValueError):
        estimate_value_per_sqft({}, 10000)

