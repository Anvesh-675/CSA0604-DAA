"""Q2 - Sequential search on an unsorted list of tool-issue records.

Record = (tool_id, technician_id, issue_time, work_bay). Search key = tool_id.
Comparison counter = number of tool_id equality checks.
"""
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import rng, write_csv, save_plot


def make_records(n, r):
    ids = r.sample(range(1, 10 * n + 1), n)
    return [(f"T-{t}", f"TECH-{r.randint(1, 200)}", 800 + i, f"BAY-{r.randint(1, 12)}") for i, t in enumerate(ids)]


def seq_search(records, key):
    comps = 0
    for rec in records:
        comps += 1
        if rec[0] == key:
            return rec, comps
    return None, comps


def main():
    r = rng(2)
    rows = []
    for n in [100, 1000, 10000, 100000]:
        recs = make_records(n, r)
        cases = {
            "success: first": recs[0][0],
            "success: middle": recs[n // 2][0],
            "success: last": recs[-1][0],
            "unsuccessful": "T-NOTPRESENT",
        }
        for cname, key in cases.items():
            _, c = seq_search(recs, key)
            rows.append([n, cname, c])
        # average over 1000 random successful searches
        tot = 0
        q = 1000
        for _ in range(q):
            _, c = seq_search(recs, recs[r.randrange(n)][0])
            tot += c
        rows.append([n, "success: average of 1000 random", tot / q])
    write_csv("q2_sequential.csv", ["n", "case", "comparisons"], rows)

    # throughput boundary: total comparisons per day = n * requests
    # measured time per search at various n (unsuccessful = worst case)
    tbl = []
    for n in [1000, 10000, 100000, 1000000]:
        recs = make_records(n, r)
        reps = max(3, 200000 // n)
        t0 = time.perf_counter()
        for _ in range(reps):
            seq_search(recs, "T-NOTPRESENT")
        per = (time.perf_counter() - t0) / reps * 1000
        tbl.append([n, round(per, 4)])
    write_csv("q2_time_per_unsuccessful_search_ms.csv", ["n", "ms_per_search"], tbl)

    fig, ax = plt.subplots(figsize=(6, 4))
    ns = sorted({x[0] for x in rows})
    for case in ["success: first", "success: average of 1000 random", "success: last", "unsuccessful"]:
        ax.loglog(ns, [next(x[2] for x in rows if x[0] == n and x[1] == case) for n in ns], marker="o", label=case)
    ax.set_xlabel("list size n")
    ax.set_ylabel("comparisons")
    ax.set_title("Q2: sequential search comparisons")
    ax.legend(fontsize=7)
    save_plot(fig, "q2_comparisons.png")
    print("Q2 done")


if __name__ == "__main__":
    main()
