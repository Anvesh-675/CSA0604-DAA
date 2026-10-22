"""Q4 - Brute-force closest pair. Examines each unordered pair (i<j) exactly once: n(n-1)/2 pairs."""
import math
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import rng, write_csv, save_plot


def closest_pair_bf(pts):
    """Return (best_dist, pair, pairs_examined, distance_calcs).
    Squared distance is used for comparison; sqrt is taken once at the end."""
    n = len(pts)
    best = float("inf")
    best_pair = None
    pairs = dists = 0
    for i in range(n - 1):
        xi, yi = pts[i]
        for j in range(i + 1, n):
            pairs += 1
            dx, dy = xi - pts[j][0], yi - pts[j][1]
            d2 = dx * dx + dy * dy
            dists += 1
            if d2 < best:
                best, best_pair = d2, (pts[i], pts[j])
    return math.sqrt(best), best_pair, pairs, dists


def random_points(n, r):
    return [(r.uniform(0, 10000), r.uniform(0, 10000)) for _ in range(n)]


def main():
    r = rng(4)
    rows = []
    for n in [100, 200, 400, 800, 1600, 3200]:
        pts = random_points(n, r)
        t0 = time.perf_counter()
        d, _, pairs, dists = closest_pair_bf(pts)
        dt = time.perf_counter() - t0
        assert pairs == n * (n - 1) // 2
        rows.append([n, pairs, n * (n - 1) // 2, dists, round(dt * 1000, 2)])
    write_csv("q4_closest_pair.csv", ["n", "pairs_examined", "n(n-1)/2", "distance_calcs", "time_ms"], rows)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ns = [x[0] for x in rows]
    ax[0].plot(ns, [x[1] for x in rows], marker="o", label="measured")
    ax[0].plot(ns, [x[2] for x in rows], "--", label="n(n-1)/2")
    ax[0].set_xlabel("n")
    ax[0].set_ylabel("pairs examined")
    ax[0].legend()
    ax[1].plot(ns, [x[4] for x in rows], marker="o", color="C3")
    ax[1].set_xlabel("n")
    ax[1].set_ylabel("time (ms)")
    fig.suptitle("Q4: brute-force closest pair")
    save_plot(fig, "q4_growth.png")
    print("Q4 done")


if __name__ == "__main__":
    main()
