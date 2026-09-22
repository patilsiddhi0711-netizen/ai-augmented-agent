import cProfile
import pstats
import random
import time


# --- 1. ALGORITHM IMPLEMENTATIONS ---


def run_linear_search(arr, target):
    """Linear Search: Checks elements one by one.

    Complexity: O(1) Best | O(n) Avg | O(n) Worst
    """
    comparisons = 0
    for item in arr:
        comparisons += 1
        if item == target:
            return True, comparisons
    return False, comparisons


def run_binary_search(arr, target):
    """Binary Search: Divides search space in half each step.

    Complexity: O(1) Best | O(log n) Avg | O(log n) Worst
    """
    comparisons = 0
    low = 0
    high = len(arr) - 1

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return True, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return False, comparisons


# --- 2. BENCHMARK SUITE FOR BEST, AVERAGE, AND WORST CASES ---


def evaluate_case(case_name, dataset, target_val, iterations=1000):
    print(f"\n==================================================")
    print(f" TESTING: {case_name}")
    print(f" Target Value: {target_val}")
    print(f"==================================================")

    # --- Linear Search Benchmark ---
    t0 = time.perf_counter()
    for _ in range(iterations):
        found_lin, lin_comp = run_linear_search(dataset, target_val)
    lin_time = ((time.perf_counter() - t0) / iterations) * 1000  # ms

    # --- Binary Search Benchmark ---
    t0 = time.perf_counter()
    for _ in range(iterations):
        found_bin, bin_comp = run_binary_search(dataset, target_val)
    bin_time = ((time.perf_counter() - t0) / iterations) * 1000  # ms

    # Output Comparative Results Table
    print(
        f"{'Metric':<25} | {'Linear Search':<15} | {'Binary Search':<15}"
    )
    print("-" * 62)
    print(
        f"{'Target Found?':<25} | {str(found_lin):<15} | {str(found_bin):<15}"
    )
    print(
        f"{'Comparisons Made':<25} | {lin_comp:<15} | {bin_comp:<15}"
    )
    print(
        f"{'Avg Time (ms)':<25} | {lin_time:<15.6f} | {bin_time:<15.6f}"
    )

    return (lin_comp, lin_time), (bin_comp, bin_time)


# --- 3. MAIN EXPERIMENT RUNNER ---

if __name__ == "__main__":
    DATA_SIZE = 100000
    dataset = list(range(DATA_SIZE))  # Sorted array from 0 to 99,999

    # Define Best, Average, and Worst Case Target Values
    best_target_linear = dataset[0]  # Element at first index
    best_target_binary = dataset[
        (len(dataset) - 1) // 2
    ]  # Element at exact middle index

    avg_target = random.choice(
        dataset
    )  # Random element somewhere in array
    worst_target = 999999  # Target not present in array

    # Run Benchmark Suite
    print(f"Dataset Size: {DATA_SIZE:,} sorted elements\n")

    # 1. Best Case Runs
    evaluate_case("BEST CASE (Linear)", dataset, best_target_linear)
    evaluate_case("BEST CASE (Binary)", dataset, best_target_binary)

    # 2. Average Case Run
    evaluate_case("AVERAGE CASE", dataset, avg_target)

    # 3. Worst Case Run
    evaluate_case("WORST CASE (Element Missing)", dataset, worst_target)

    # --- 4. CPROFILE FOR REPORT VISUALIZATION ---
    print("\n\n--------------------------------------------------")
    print(" CPROFILE FUNCTION TIMINGS (Average Case Workload)")
    print("--------------------------------------------------")
    profiler = cProfile.Profile()
    profiler.enable()

    for _ in range(5000):
        run_linear_search(dataset, avg_target)
        run_binary_search(dataset, avg_target)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("cumtime")
    stats.print_stats(10)