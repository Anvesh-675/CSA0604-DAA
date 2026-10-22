import csv
import os
import random
import time
import statistics
import matplotlib.pyplot as plt

from linear_search import linear_search
from binary_search import binary_search
from hash_search import build_hash, hash_search

SIZES = [1000, 10000, 100000, 1000000]
REPEATS = 3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def measure(function, repeats=REPEATS):
    times = []

    for _ in range(repeats):
        start = time.perf_counter()
        function()
        times.append(time.perf_counter() - start)

    return statistics.median(times)


def run_experiments():
    rows = []

    for n in SIZES:
        print(f"\nTesting {n:,} records...")

        records = list(range(1000000, 1000000 + n))
        target = records[-1]  # Worst case for linear search

        linear_time = measure(
            lambda: linear_search(records, target)
        )

        binary_time = measure(
            lambda: binary_search(records, target, 0, len(records) - 1)
        )

        hash_build_time = measure(
            lambda: build_hash(records)
        )

        record_set = build_hash(records)

        hash_lookup_time = measure(
            lambda: hash_search(record_set, target)
        )

        _, linear_comparisons = linear_search(records, target)
        _, binary_comparisons = binary_search(
            records, target, 0, len(records) - 1
        )

        row = {
            "records": n,
            "linear_seconds": linear_time,
            "linear_comparisons": linear_comparisons,
            "binary_seconds": binary_time,
            "binary_comparisons": binary_comparisons,
            "hash_build_seconds": hash_build_time,
            "hash_lookup_seconds": hash_lookup_time
        }

        rows.append(row)

        print(f"Linear search: {linear_time:.6f} seconds")
        print(f"Binary search: {binary_time:.6f} seconds")
        print(f"Hash build:    {hash_build_time:.6f} seconds")
        print(f"Hash lookup:   {hash_lookup_time:.8f} seconds")
        print(f"Linear comparisons: {linear_comparisons}")
        print(f"Binary comparisons: {binary_comparisons}")

    csv_path = os.path.join(RESULTS_DIR, "performance.csv")

    with open(csv_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    sizes = [row["records"] for row in rows]

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, [r["linear_seconds"] for r in rows],
             marker="o", label="Linear Search")
    plt.plot(sizes, [r["binary_seconds"] for r in rows],
             marker="o", label="Binary Search")
    plt.plot(sizes, [r["hash_build_seconds"] for r in rows],
             marker="o", label="Hash Build")
    plt.plot(sizes, [r["hash_lookup_seconds"] for r in rows],
             marker="o", label="Hash Lookup")

    plt.xlabel("Number of Records")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Student Record Search Performance")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()

    graph_path = os.path.join(RESULTS_DIR, "performance_graph.png")
    plt.savefig(graph_path, dpi=300)
    plt.close()

    print("\nEXPERIMENT COMPLETED")
    print("CSV:", csv_path)
    print("Graph:", graph_path)


if __name__ == "__main__":
    run_experiments()
