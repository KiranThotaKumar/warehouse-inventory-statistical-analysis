from src.data_generation import generate_population
from src.sampling import draw_random_sample
from src.estimation import estimate_mean, estimate_value_per_sqft

population = generate_population()
sample = draw_random_sample(population, sample_size=100)

estimation = estimate_mean(sample, population_size=len(population))
area_estimate = estimate_value_per_sqft(
    estimation,
    floor_area_sqft=10_000,
)

for key, value in area_estimate.items():
    print(f"{key}: {value}")
