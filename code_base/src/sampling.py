

"""
Simple random sampling without replacement (SRSWOR).

This module selects a random sample from a synthetic
warehouse inventory population.
"""

import numpy as np
import pandas as pd


def draw_random_sample(
    population: pd.DataFrame,
    sample_size: int,
    random_seed: int = 123,
) -> pd.DataFrame:
    """
    Draw a simple random sample without replacement.

    Parameters
    ----------
    population : pd.DataFrame
        Population containing box_id and retail_value_usd.
    sample_size : int
        Number of boxes to select.
    random_seed : int
        Seed for reproducible sampling.

    Returns
    -------
    pd.DataFrame
        Random sample with the original columns.
    """
    if not isinstance(population, pd.DataFrame):
        raise TypeError("population must be a pandas DataFrame.")

    required_columns = {"box_id", "retail_value_usd"}
    if not required_columns.issubset(population.columns):
        raise ValueError(
            "Population must contain box_id and retail_value_usd."
        )

    if population.empty:
        raise ValueError("Population must not be empty.")

    if not population["box_id"].is_unique:
        raise ValueError("Population box_id values must be unique.")

    if (
        isinstance(sample_size, (bool, np.bool_))
        or not isinstance(sample_size, (int, np.integer))
    ):
        raise TypeError("sample_size must be an integer.")

    if sample_size <= 0 or sample_size > len(population):
        raise ValueError(
            "sample_size must be between 1 and population size."
        )

    if (
        isinstance(random_seed, (bool, np.bool_))
        or not isinstance(random_seed, (int, np.integer))
    ):
        raise TypeError("random_seed must be an integer.")

    rng = np.random.default_rng(random_seed)

    selected_indices = rng.choice(
        len(population),
        size=sample_size,
        replace=False,
    )

    sample = population.iloc[selected_indices].copy()
    return sample.reset_index(drop=True)
