"""Q1 - Selection, Bubble (with early exit) and Insertion sort under different data conditions.

Counters
  comparisons : key comparisons between two array elements
  moves       : element writes/swaps (a swap counts as 1 swap; an insertion shift counts as 1 move)
"""
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import rng, write_csv, save_plot


def selection_sort(a):
    a = a[:]
    comps = swaps = 0
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
            swaps += 1
    return a, comps, swaps


def bubble_sort(a):
    """Bubble sort with the standard 'no swap in a pass -> stop' optimisation."""
    a = a[:]
    comps = swaps = 0
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return a, comps, swaps


def bubble_sort_plain(a):
    """Bubble sort WITHOUT early exit (to show why the optimisation matters)."""
    a = a[:]
    comps = swaps = 0
    n = len(a)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
    return a, comps, swaps


def insertion_sort(a):
    a = a[:]
    comps = moves = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                moves += 1
                j -= 1
            else:
                break
        if j + 1 != i:
            a[j + 1] = key
            moves += 1
    return a, comps, moves


ALGOS = {
    "Selection": selection_sort,
    "Bubble": bubble_sort,
    "Bubble (no early exit)": bubble_sort_plain,
    "Insertion": insertion_sort,
}


def make_datasets(n, r):
    base = list(range(1, n + 1))
    rand = base[:]
    r.shuffle(rand)
    nearly = base[:]
    for _ in range(max(1, n // 100)):  # ~1% random swaps -> nearly sorted
        i, j = r.randrange(n), r.randrange(n)
        nearly[i], nearly[j] = nearly[j], nearly[i]
    # 95% sorted + small batch of new orders appended at the end (the fulfilment-centre case)
    k = max(1, n // 20)
    ninety_five = base[: n - k] + [r.randint(1, n) for _ in range(k)]
    return {
        "Random": rand,
        "Already sorted": base,
        "Reverse sorted": base[::-1],
        "Nearly sorted (1% swaps)": nearly,
        "95% sorted + 5% new batch": ninety_five,
        "All equal (edge case)": [7] * n,
    }


def main():
    n = 1000
    r = rng(1)
    rows = []
    for dname, data in make_datasets(n, r).items():
        for aname, fn in ALGOS.items():
            t0 = time.perf_counter()
            out, c, m = fn(data)
            dt = (time.perf_counter() - t0) * 1000
            assert out == sorted(data), (aname, dname)
            rows.append([dname, aname, n, c, m, round(dt, 3)])
    write_csv("q1_sorting.csv", ["dataset", "algorithm", "n", "comparisons", "swaps_or_moves", "time_ms"], rows)

    # scaling on the recommended scenario: 95% sorted
    sizes = [100, 200, 400, 800, 1600]
    scale = []
    for s in sizes:
        d = make_datasets(s, rng(s))["95% sorted + 5% new batch"]
        for aname in ("Selection", "Bubble", "Insertion"):
            _, c, m = ALGOS[aname](d)
            scale.append([s, aname, c, m])
    write_csv("q1_scaling_95pct.csv", ["n", "algorithm", "comparisons", "swaps_or_moves"], scale)

    # plots
    fig, ax = plt.subplots(figsize=(9, 4.5))
    dnames = list(dict.fromkeys(r_[0] for r_ in rows))
    width = 0.2
    for k, aname in enumerate(ALGOS):
        vals = [next(r_[3] for r_ in rows if r_[0] == d and r_[1] == aname) for d in dnames]
        ax.bar([i + k * width for i in range(len(dnames))], vals, width, label=aname)
    ax.set_xticks([i + 1.5 * width for i in range(len(dnames))])
    ax.set_xticklabels(dnames, rotation=20, ha="right", fontsize=8)
    ax.set_ylabel("Comparisons (n=1000)")
    ax.set_title("Q1: comparisons by dataset and algorithm")
    ax.legend(fontsize=8)
    save_plot(fig, "q1_comparisons.png")

    fig, ax = plt.subplots(figsize=(6, 4))
    for aname in ("Selection", "Bubble", "Insertion"):
        ax.plot(sizes, [x[2] for x in scale if x[1] == aname], marker="o", label=aname)
    ax.set_xlabel("n")
    ax.set_ylabel("Comparisons")
    ax.set_title("Q1: 95%-sorted input, growth with n")
    ax.legend()
    save_plot(fig, "q1_scaling.png")
    print("Q1 done")


if __name__ == "__main__":
    main()
