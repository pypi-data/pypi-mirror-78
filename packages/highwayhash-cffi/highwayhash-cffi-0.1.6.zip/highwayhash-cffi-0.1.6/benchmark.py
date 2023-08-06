import time

# Relevant Module Imports
from highwayhash import highwayhash_64, highwayhash_128, highwayhash_256

# Setup and Preparation
ITERATION_NUMERATOR = 800000
ITERATION_ADDITIVE = 100
HIGHWAYHASH_VARIANTS = (highwayhash_64, highwayhash_128, highwayhash_256)
HIGHWAYHASH_DATA_SIZES = (8, 31, 32, 63, 64, 128, 256, 512, 1024, 1500, 1024 ** 2)
HIGHWAYHASH_DATA_CHUNKS = (b"\0" * size for size in HIGHWAYHASH_DATA_SIZES)
HIGHWAYHASH_KEY = b"\0" * 32


# Benchmark Definitions
def benchmark_factory(variant, highwayhash_key, highwayhash_data, highwayhash_data_length):
    def benchmark():
        variant(highwayhash_key, highwayhash_data)

    return (
        "Algorithm {} - Size {}".format(variant.__name__, highwayhash_data_length),
        highwayhash_data_length,
        benchmark,
    )


benchmarks = []

for data_size, data_chunk in zip(HIGHWAYHASH_DATA_SIZES, HIGHWAYHASH_DATA_CHUNKS):
    for variant in HIGHWAYHASH_VARIANTS:
        benchmarks.append(benchmark_factory(variant, HIGHWAYHASH_KEY, data_chunk, data_size))

# Reporting
for benchmark_name, benchmark_weight, benchmark in benchmarks:
    actual_iterations = (ITERATION_NUMERATOR // benchmark_weight) + ITERATION_ADDITIVE
    time_start = time.time()

    for i in range(actual_iterations):
        benchmark()

    time_delta = time.time() - time_start

    print("BENCHMARK:", benchmark_name)
    print("\tCALLS / SEC  ", actual_iterations / time_delta)
    print("\tMICRO / CALL ", time_delta / actual_iterations * 1000 ** 2)
