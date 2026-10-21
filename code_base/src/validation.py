
"""
Repeated-sampling validation for warehouse inventory estimation.
"""

import numpy as np
import pandas as pd

from src.sampling import draw_random_sample
from src.estimation import estimate_mean


def validate_coverage(
    population: pd.DataFrame,
    sample_size: int = 100,
    repetitions: int = 1000,
    confidence_level: float = 0.90,
    random_seed: int = 2026,
) -> dict:
    """
    Evaluate confidence interval coverage using repeated samples
    from a fixed, fully known synthetic population.
    """
    if population.empty:
        raise ValueError("Population must not be empty.")

    if not population["box_id"].is_unique:
        raise ValueError("Population box IDs must be unique.")

    if (
        isinstance(sample_size, (bool, np.bool_))
        or not isinstance(sample_size, (int, np.integer))
    ):
        raise TypeError("sample_size must be an integer.")

    if sample_size < 2 or sample_size > len(population):
        raise ValueError(
            "sample_size must be between 2 and population size."
        )

    if (
        isinstance(repetitions, (bool, np.bool_))
        or not isinstance(repetitions, (int, np.integer))
    ):
        raise TypeError("repetitions must be an integer.")

    if repetitions <= 0:
        raise ValueError("repetitions must be positive.")

    if not 0 < confidence_level < 1:
        raise ValueError(
            "confidence_level must be between 0 and 1."
        )

    true_mean = float(population["retail_value_usd"].mean())
    population_size = len(population)

    covered = 0
    relative_errors = []
    interval_widths = []

    # Use a reproducible sequence of distinct random seeds.
    seed_sequence = np.random.SeedSequence(random_seed)
    child_sequences = seed_sequence.spawn(repetitions)

    for child_sequence in child_sequences:
        sample_seed = int(
            child_sequence.generate_state(1)[0]
        )

        sample = draw_random_sample(
            population,
            sample_size=sample_size,
            random_seed=sample_seed,
        )

        result = estimate_mean(
            sample,
            population_size=population_size,
            confidence_level=confidence_level,
        )

        if (
            result["ci_lower"] <= true_mean
            <= result["ci_upper"]
        ):
            covered += 1

        relative_errors.append(
            result["relative_margin_error"]
        )

        interval_widths.append(
            result["ci_upper"] - result["ci_lower"]
        )

    coverage_rate = covered / repetitions

    return {
        "population_size": population_size,
        "sample_size": sample_size,
        "repetitions": repetitions,
        "confidence_level": confidence_level,
        "true_population_mean": true_mean,
        "covered_intervals": covered,
        "coverage_rate": coverage_rate,
        "mean_relative_margin_error": float(
            np.mean(relative_errors)
        ),
        "median_relative_margin_error": float(
            np.median(relative_errors)
        ),
        "proportion_meeting_25_percent_error": float(
            np.mean(np.asarray(relative_errors) <= 0.25)
        ),
        "mean_interval_width": float(
            np.mean(interval_widths)
        ),
    }

