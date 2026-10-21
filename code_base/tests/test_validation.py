
import pytest

from src.data_generation import generate_population
from src.validation import validate_coverage


def test_validation_returns_expected_fields():
    population = generate_population(population_size=100)

    result = validate_coverage(
        population,
        sample_size=30,
        repetitions=20,
    )

    expected_fields = {
        "population_size",
        "sample_size",
        "repetitions",
        "confidence_level",
        "true_population_mean",
        "covered_intervals",
        "coverage_rate",
        "mean_relative_margin_error",
        "median_relative_margin_error",
        "proportion_meeting_25_percent_error",
        "mean_interval_width",
    }

    assert expected_fields.issubset(result.keys())


def test_coverage_rate_is_between_zero_and_one():
    population = generate_population(population_size=100)

    result = validate_coverage(
        population,
        sample_size=30,
        repetitions=20,
    )

    assert 0 <= result["coverage_rate"] <= 1


def test_covered_intervals_count_is_valid():
    population = generate_population(population_size=100)

    result = validate_coverage(
        population,
        sample_size=30,
        repetitions=20,
    )

    assert 0 <= result["covered_intervals"] <= 20


def test_reproducible_validation():
    population = generate_population(population_size=100)

    result_1 = validate_coverage(
        population,
        sample_size=30,
        repetitions=20,
        random_seed=123,
    )

    result_2 = validate_coverage(
        population,
        sample_size=30,
        repetitions=20,
        random_seed=123,
    )

    assert result_1 == result_2


def test_invalid_sample_size():
    population = generate_population(population_size=100)

    with pytest.raises(ValueError):
        validate_coverage(
            population,
            sample_size=1,
            repetitions=20,
        )


def test_invalid_repetitions():
    population = generate_population(population_size=100)

    with pytest.raises(ValueError):
        validate_coverage(
            population,
            sample_size=30,
            repetitions=0,
        )

