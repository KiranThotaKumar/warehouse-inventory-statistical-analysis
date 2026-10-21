

"""
Synthetic warehouse inventory population generator.

This module creates hypothetical box-level retail values for
statistical sampling demonstrations. It does not use real
warehouse or client data.
"""

import numpy as np
import pandas as pd


def generate_population(
    population_size: int = 1000,
    mean_log: float = 4.5,
    sigma_log: float = 0.6,
    random_seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a synthetic warehouse inventory population.

    Parameters
    ----------
    population_size : int
        Number of boxes in the synthetic population.
    mean_log : float
        Mean of the underlying normal distribution in log space.
    sigma_log : float
        Standard deviation of the underlying normal distribution.
    random_seed : int
        Seed used to make the generated population reproducible.

    Returns
    -------
    pd.DataFrame
        Columns:
        - box_id: unique box identifier
        - retail_value_usd: synthetic retail value in USD

    Notes
    -----
    If Y ~ Normal(mean_log, sigma_log**2), then X = exp(Y)
    follows a lognormal distribution.

    The parameters describe the logarithm of the retail value,
    not the arithmetic mean and standard deviation of the values.
    """
    if not isinstance(population_size, (int, np.integer)):
        raise TypeError("population_size must be an integer.")

    if isinstance(population_size, (bool, np.bool_)):
        raise TypeError("population_size must be an integer, not a boolean.")

    if population_size <= 0:
        raise ValueError("population_size must be greater than zero.")

    if not np.isfinite(mean_log):
        raise ValueError("mean_log must be finite.")

    if not np.isfinite(sigma_log) or sigma_log <= 0:
        raise ValueError("sigma_log must be finite and greater than zero.")

    if not isinstance(random_seed, (int, np.integer)):
        raise TypeError("random_seed must be an integer.")

    if isinstance(random_seed, (bool, np.bool_)):
        raise TypeError("random_seed must be an integer, not a boolean.")

    rng = np.random.default_rng(random_seed)

    retail_values = rng.lognormal(
        mean=mean_log,
        sigma=sigma_log,
        size=population_size,
    )

    population = pd.DataFrame(
        {
            "box_id": [
                f"BOX-{i:04d}" for i in range(1, population_size + 1)
            ],
            "retail_value_usd": retail_values,
        }
    )

    return population
