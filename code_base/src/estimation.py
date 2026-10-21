
"""
Statistical estimation for warehouse inventory sampling.
"""

import numpy as np
import pandas as pd
from scipy.stats import t


def estimate_mean(
    sample: pd.DataFrame,
    population_size: int,
    confidence_level: float = 0.90,
) -> dict:
    """
    Estimate population mean and calculate a t confidence interval
    using the finite population correction.

    Parameters
    ----------
    sample : pd.DataFrame
        Sample containing retail_value_usd.
    population_size : int
        Total number of boxes in the population.
    confidence_level : float
        Two-sided confidence level, e.g. 0.90.

    Returns
    -------
    dict
        Sample mean, sample standard deviation, standard error,
        confidence interval, and relative margin of error.
    """
    if not isinstance(sample, pd.DataFrame):
        raise TypeError("sample must be a pandas DataFrame.")

    if "retail_value_usd" not in sample.columns:
        raise ValueError(
            "Sample must contain retail_value_usd."
        )

    if (
        isinstance(population_size, (bool, np.bool_))
        or not isinstance(population_size, (int, np.integer))
    ):
        raise TypeError("population_size must be an integer.")

    if population_size <= 0:
        raise ValueError("population_size must be positive.")

    if sample.empty:
        raise ValueError("Sample must not be empty.")

    if len(sample) > population_size:
        raise ValueError(
            "Sample size cannot exceed population size."
        )

    if len(sample) < 2:
        raise ValueError(
            "At least two observations are required."
        )

    if not np.isfinite(confidence_level) or not (
        0 < confidence_level < 1
    ):
        raise ValueError(
            "confidence_level must be between 0 and 1."
        )

    values = sample["retail_value_usd"].to_numpy(dtype=float)

    if not np.all(np.isfinite(values)):
        raise ValueError("Sample values must be finite.")

    if np.any(values < 0):
        raise ValueError("Retail values must be nonnegative.")

    n = len(values)
    N = population_size

    sample_mean = float(np.mean(values))
    sample_std = float(np.std(values, ddof=1))
    sample_variance = sample_std**2

    fpc = np.sqrt(1 - n / N)
    standard_error = fpc * sample_std / np.sqrt(n)

    alpha = 1 - confidence_level
    critical_value = t.ppf(
        1 - alpha / 2,
        df=n - 1,
    )

    margin_of_error = critical_value * standard_error
    lower_bound = sample_mean - margin_of_error
    upper_bound = sample_mean + margin_of_error

    if sample_mean > 0:
        relative_margin_error = (
            margin_of_error / sample_mean
        )
    else:
        relative_margin_error = np.nan

    estimated_total_value = population_size * sample_mean
    estimated_total_standard_error = population_size * standard_error
    total_ci_lower = population_size * lower_bound
    total_ci_upper = population_size * upper_bound

    return {
        "population_size": N,
        "sample_size": n,
        "confidence_level": confidence_level,
        "sample_mean": sample_mean,
        "sample_std": sample_std,
        "sample_variance": sample_variance,
        "standard_error": float(standard_error),
        "margin_of_error": float(margin_of_error),
        "ci_lower": float(lower_bound),
        "ci_upper": float(upper_bound),
        "relative_margin_error": float(
            relative_margin_error
        ),
        "estimated_total_value": float(estimated_total_value),
        "estimated_total_standard_error": float(
            estimated_total_standard_error
        ),
        "total_ci_lower": float(total_ci_lower),
        "total_ci_upper": float(total_ci_upper),
    }


def estimate_value_per_sqft(
    estimation_result: dict,
    floor_area_sqft: float,
) -> dict:
    """
    Calculate estimated retail inventory value per square foot.

    Floor area is assumed to be known and fixed.
    """
    if (
        isinstance(floor_area_sqft, (bool, np.bool_))
        or not isinstance(floor_area_sqft, (int, float, np.integer, np.floating))
    ):
        raise TypeError("floor_area_sqft must be numeric.")

    if not np.isfinite(floor_area_sqft) or floor_area_sqft <= 0:
        raise ValueError(
            "floor_area_sqft must be finite and greater than zero."
        )

    required_fields = {
        "estimated_total_value",
        "total_ci_lower",
        "total_ci_upper",
    }

    if not required_fields.issubset(estimation_result):
        raise ValueError(
            "Estimation result is missing required total-value fields."
        )

    area = float(floor_area_sqft)

    return {
        "floor_area_sqft": area,
        "estimated_inventory_value_per_sqft": (
            estimation_result["estimated_total_value"] / area
        ),
        "ci_lower_per_sqft": (
            estimation_result["total_ci_lower"] / area
        ),
        "ci_upper_per_sqft": (
            estimation_result["total_ci_upper"] / area
        ),
    }
