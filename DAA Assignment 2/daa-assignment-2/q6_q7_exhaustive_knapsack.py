"""Q6 - Exhaustive search for the airlift (0/1 knapsack) problem.
Q7 - Redesign: depth-first search with feasibility pruning + value-density bound (own design).

Representation: a candidate is an n-bit mask; bit i = 1 means package i is loaded.
Q6 exhaustive: enumerate all 2^n masks, check weight <= capacity, evaluate value, keep best.
"""
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import rng, write_csv, save_plot


def exhaustive(weights, values, cap):
    n = len(weights)
    best_v, best_mask = 0, 0
    examined = feasible = 0
    for mask in range(1 << n):
        examined += 1
        w = v = 0
        for i in range(n):
            if mask >> i & 1:
                w += weights[i]
                v += values[i]
        if w <= cap:
            feasible += 1
            if v > best_v:
                best_v, best_mask = v, mask
    return best_v, best_mask, examined, feasible


def redesigned(weights, values, cap):
    """Q7 redesign.
    Idea (own reasoning from the Q6 diagnosis): build solutions incrementally as a decision tree
    and never extend a partial solution that
      (a) is already overweight  -> every superset is infeasible (prune whole subtree), or
      (b) cannot beat the best value found so far even if the remaining capacity were filled
          at the best value/weight ratio still available (optimistic bound).
    Preprocessing: sort items by value/weight descending so the bound is tight and a good
    solution is found early. Extra memory: O(n) recursion stack + sorted order.
    """
    n = len(weights)
    order = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)
    w = [weights[i] for i in order]
    v = [values[i] for i in order]
    best = [0, []]
    nodes = [0]

    def bound(i, curw, curv):
        # fractional-fill optimistic bound
        room = cap - curw
        b = curv
        while i < n and w[i] <= room:
            room -= w[i]
            b += v[i]
            i += 1
        if i < n:
            b += v[i] * room / w[i]
        return b

    def dfs(i, curw, curv, chosen):
        nodes[0] += 1
        if curv > best[0]:
            best[0], best[1] = curv, chosen[:]
        if i == n:
            return
        if bound(i, curw, curv) <= best[0]:
            return  # cannot beat current best
        if curw + w[i] <= cap:  # include
            chosen.append(order[i])
            dfs(i + 1, curw + w[i], curv + v[i], chosen)
            chosen.pop()
        dfs(i + 1, curw, curv, chosen)  # exclude

    dfs(0, 0, 0, [])
    return best[0], sorted(best[1]), nodes[0]


def feasibility_only(weights, values, cap):
    """Ablation for Q7: decision tree that only skips overweight branches (no value bound).
    Returns (best_value, complete_candidates_reached) - comparable to 'candidates examined'."""
    n = len(weights)
    best = [0]
    leaves = [0]

    def dfs(i, cw, cv):
        if cv > best[0]:
            best[0] = cv
        if i == n:
            leaves[0] += 1
            return
        if cw + weights[i] <= cap:
            dfs(i + 1, cw + weights[i], cv + values[i])
        dfs(i + 1, cw, cv)

    dfs(0, 0, 0)
    return best[0], leaves[0]


def instance(n, r):
    weights = [r.randint(5, 50) for _ in range(n)]
    values = [r.randint(10, 100) for _ in range(n)]
    cap = sum(weights) // 2
    return weights, values, cap


def main():
    # ---- Q6 correctness: small hand-verifiable instance (4 packages) ----
    w, v, cap = [5, 4, 6, 3], [10, 40, 30, 50], 10
    # all 16 subsets verified by hand in the report; optimum = {B, D}: weight 7, value 90
    bv, bm, ex, fe = exhaustive(w, v, cap)
    write_csv("q6_correctness.csv", ["best_value", "best_mask_bits", "candidates", "feasible"],
              [[bv, bin(bm), ex, fe]])
    print("Q6 correctness:", bv, bin(bm), ex, fe)

    r = rng(6)
    rows = []
    for n in range(10, 25, 2):
        w, v, cap = instance(n, r)
        t0 = time.perf_counter()
        bv, bm, ex, fe = exhaustive(w, v, cap)
        dt = time.perf_counter() - t0
        rows.append([n, 2 ** n, ex, fe, bv, round(dt, 3)])
    write_csv("q6_growth.csv", ["n", "2^n", "candidates_examined", "feasible", "best_value", "time_s"], rows)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy([x[0] for x in rows], [x[2] for x in rows], marker="o", label="examined")
    ax.semilogy([x[0] for x in rows], [x[1] for x in rows], "--", label="2^n")
    ax.set_xlabel("n packages")
    ax.set_ylabel("candidates (log)")
    ax.legend()
    ax.set_title("Q6: exhaustive search growth")
    save_plot(fig, "q6_growth.png")

    # ---- Q7 validation: original vs redesign on identical instances ----
    rows7 = []
    for n in [10, 14, 18, 20, 22, 24]:
        w, v, cap = instance(n, rng(100 + n))
        t0 = time.perf_counter()
        bv1, _, ex, _ = exhaustive(w, v, cap)
        t1 = time.perf_counter() - t0
        t0 = time.perf_counter()
        bv2, _, nodes = redesigned(w, v, cap)
        t2 = time.perf_counter() - t0
        assert bv1 == bv2, (n, bv1, bv2)
        bv3, fo_leaves = feasibility_only(w, v, cap)
        assert bv3 == bv1
        rows7.append([n, ex, fo_leaves, nodes, round(ex / nodes, 1), round(t1, 4), round(t2, 5)])
    # push the redesign far beyond the exhaustive limit
    big = []
    for n in [30, 40, 50, 60, 80]:
        w, v, cap = instance(n, rng(200 + n))
        t0 = time.perf_counter()
        bv2, _, nodes = redesigned(w, v, cap)
        big.append([n, 2 ** n, nodes, round(time.perf_counter() - t0, 4)])
    write_csv("q7_original_vs_redesign.csv",
              ["n", "exhaustive_candidates", "feasibility_only_candidates", "redesign_nodes",
               "reduction_factor", "exhaustive_s", "redesign_s"], rows7)
    write_csv("q7_redesign_large_n.csv", ["n", "2^n", "redesign_nodes", "time_s"], big)

    # adversarial case for the redesign: all items have identical ratio -> bound gives little pruning
    adv = []
    for n in [12, 16, 20, 22]:
        w = [10 + (i % 3) for i in range(n)]
        v = [x * 3 for x in w]  # ratio exactly 3 for all
        cap = sum(w) // 2 + 1
        _, _, ex, _ = exhaustive(w, v, cap) if n <= 22 else (0, 0, 0, 0)
        _, _, nodes = redesigned(w, v, cap)
        adv.append([n, ex, nodes])
    write_csv("q7_adversarial_equal_ratio.csv", ["n", "exhaustive_candidates", "redesign_nodes"], adv)

    # genuinely hard case for the bound: strongly correlated items (value = weight + 10),
    # so value/weight ratios are almost identical and the optimistic bound stays close to the
    # incumbent for most of the tree. Multiple seeds per size; report mean and worst nodes visited.
    hard = []
    for n in [20, 24, 28, 32, 36, 40]:
        node_list = []
        for s in range(5):
            rr = rng(300 + 10 * n + s)
            w = [rr.randint(10, 100) for _ in range(n)]
            v = [x + 10 for x in w]
            cap = sum(w) // 2
            _, _, nodes = redesigned(w, v, cap)
            node_list.append(nodes)
        hard.append([n, 2 ** n, round(sum(node_list) / len(node_list)), max(node_list)])
    write_csv("q7_hard_correlated.csv", ["n", "2^n", "mean_nodes_5_seeds", "worst_nodes"], hard)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy([x[0] for x in rows7], [x[1] for x in rows7], marker="o", label="exhaustive (2^n)")
    ax.semilogy([x[0] for x in rows7], [x[2] for x in rows7], marker="^", label="feasibility pruning only")
    ax.semilogy([x[0] for x in rows7], [x[3] for x in rows7], marker="s", label="redesign (nodes visited)")
    ax.set_xlabel("n packages")
    ax.set_ylabel("candidates / nodes (log)")
    ax.legend()
    ax.set_title("Q7: original vs redesigned")
    save_plot(fig, "q7_comparison.png")
    print("Q6/Q7 done")


if __name__ == "__main__":
    main()
