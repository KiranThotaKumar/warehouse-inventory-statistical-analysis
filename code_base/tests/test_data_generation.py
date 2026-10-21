
import numpy as np
import pandas as pd
import pytest

from src.data_generation import generate_population
from src.sampling import draw_random_sample
from src.estimation import estimate_mean


def test_population_size_and_columns():
    population = generate_population(population_size=100)

    assert len(population) == 100
    assert list(population.columns) == [
        "box_id",
        "retail_value_usd",
    ]


def test_box_ids_are_unique():
    population = generate_population(population_size=100)

    assert population["box_id"].is_unique


def test_retail_values_are_positive_and_finite():
    population = generate_population(population_size=100)

    values = population["retail_value_usd"].to_numpy()

    assert np.all(np.isfinite(values))
    assert np.all(values > 0)


def test_same_seed_reproduces_population():
    population_1 = generate_population(
        population_size=100,
        random_seed=123,
    )
    population_2 = generate_population(
        population_size=100,
        random_seed=123,
    )

    pd.testing.assert_frame_equal(population_1, population_2)


def test_different_seeds_produce_different_values():
    population_1 = generate_population(
        population_size=100,
        random_seed=123,
    )
    population_2 = generate_population(
        population_size=100,
        random_seed=456,
    )

    assert not np.array_equal(
        population_1["retail_value_usd"].to_numpy(),
        population_2["retail_value_usd"].to_numpy(),
    )


def test_invalid_population_size():
    with pytest.raises(ValueError):
        generate_population(population_size=0)


def test_invalid_sigma():
    with pytest.raises(ValueError):
        generate_population(sigma_log=0)


def test_non_integer_population_size():
    with pytest.raises(TypeError):
        generate_population(population_size=10.5)

def test_sample_size():
    population = generate_population(population_size=1000)
    sample = draw_random_sample(population, sample_size=100)

    assert len(sample) == 100


def test_no_duplicate_boxes():
    population = generate_population(population_size=1000)
    sample = draw_random_sample(population, sample_size=100)

    assert sample["box_id"].is_unique


def test_sample_contains_only_population_boxes():
    population = generate_population(population_size=1000)
    sample = draw_random_sample(population, sample_size=100)

    assert set(sample["box_id"]).issubset(
        set(population["box_id"])
    )


def test_reproducible_sampling():
    population = generate_population(population_size=1000)

    sample_1 = draw_random_sample(
        population, sample_size=100, random_seed=42
    )
    sample_2 = draw_random_sample(
        population, sample_size=100, random_seed=42
    )

    pd.testing.assert_frame_equal(sample_1, sample_2)


def test_different_seeds_can_produce_different_samples():
    population = generate_population(population_size=1000)

    sample_1 = draw_random_sample(
        population, sample_size=100, random_seed=42
    )
    sample_2 = draw_random_sample(
        population, sample_size=100, random_seed=99
    )

    assert set(sample_1["box_id"]) != set(sample_2["box_id"])


def test_sample_size_cannot_exceed_population():
    population = generate_population(population_size=10)

    with pytest.raises(ValueError):
        draw_random_sample(population, sample_size=11)


def test_sample_size_must_be_positive():
    population = generate_population(population_size=100)

    with pytest.raises(ValueError):
        draw_random_sample(population, sample_size=0)


def test_sample_size_must_be_integer():
    population = generate_population(population_size=100)

    with pytest.raises(TypeError):
        draw_random_sample(population, sample_size=10.5)

def test_estimation_returns_expected_fields():
    population = generate_population(population_size=1000)
    sample = draw_random_sample(population, sample_size=100)

    result = estimate_mean(sample, population_size=1000)

    expected_fields = {
        "population_size",
        "sample_size",
        "confidence_level",
        "sample_mean",
        "sample_std",
        "sample_variance",
        "standard_error",
        "margin_of_error",
        "ci_lower",
        "ci_upper",
        "relative_margin_error",
    }

    assert expected_fields.issubset(result.keys())


def test_confidence_interval_contains_sample_mean():
    population = generate_population(population_size=1000)
    sample = draw_random_sample(population, sample_size=100)

    result = estimate_mean(sample, population_size=1000)

    assert result["ci_lower"] <= result["sample_mean"]
    assert result["sample_mean"] <= result["ci_upper"]


def test_standard_error_and_margin_are_nonnegative():
    population = generate_population(population_size=1000)
    sample = draw_random_sample(population, sample_size=100)

    result = estimate_mean(sample, population_size=1000)

    assert result["standard_error"] >= 0
    assert result["margin_of_error"] >= 0


def test_relative_margin_error():
    population = generate_population(population_size=1000)
    sample = draw_random_sample(population, sample_size=100)

    result = estimate_mean(sample, population_size=1000)

    expected = (
        result["margin_of_error"] / result["sample_mean"]
    )

    assert np.isclose(
        result["relative_margin_error"], expected
    )


def test_sample_must_have_at_least_two_rows():
    population = generate_population(population_size=10)
    sample = population.iloc[:1]

    with pytest.raises(ValueError):
        estimate_mean(sample, population_size=10)


def test_sample_cannot_exceed_population():
    population = generate_population(population_size=10)

    with pytest.raises(ValueError):
        estimate_mean(population, population_size=5)

p = generate_population()
print(p.head())
print('\nPopulation size:', len(p))
print('Mean value: $', round(p['retail_value_usd'].mean(), 2))
print('Total value: $', round(p['retail_value_usd'].sum(), 2))

s = draw_random_sample(p, 100)
r = estimate_mean(s, len(p))
[print(f'{k}: {v}') for k, v in r.items()]
