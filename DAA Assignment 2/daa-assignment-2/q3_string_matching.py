"""Q3 - Brute-force string matching with a character-comparison counter."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import rng, write_csv, save_plot


def brute_force_match(text, pat):
    """Return (first match index or -1, character comparisons). Stops at first match."""
    n, m = len(text), len(pat)
    comps = 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comps += 1
            if text[i + j] != pat[j]:
                break
            j += 1
        if j == m:
            return i, comps
    return -1, comps


def brute_force_all(text, pat):
    n, m = len(text), len(pat)
    comps = 0
    hits = []
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comps += 1
            if text[i + j] != pat[j]:
                break
            j += 1
        if j == m:
            hits.append(i)
    return hits, comps


def main():
    n, m = 10000, 100
    r = rng(3)
    log_chars = "abcdefghijklmnopqrstuvwxyz0123456789 :-"
    random_text = "".join(r.choice(log_chars) for _ in range(n))
    tests = {
        # best case: pattern's first char never appears -> 1 comparison per alignment
        "A best case (first char absent)": ("a" * n, "b" + "a" * (m - 1)),
        # worst case: text all 'a', pattern 'a'*(m-1)+'b' -> m comparisons at every alignment
        "B worst case (aaa..ab)": ("a" * n, "a" * (m - 1) + "b"),
        # realistic log-like random text, 100-char pattern copied from the middle
        "C random log-like text": (random_text, random_text[5000:5000 + m]),
        # extra: random text, pattern that is absent
        "D random text, absent pattern": (random_text, "".join(r.choice("XYZ") for _ in range(m))),
    }
    rows = []
    for name, (t, p) in tests.items():
        idx, c = brute_force_match(t, p)
        rows.append([name, len(t), len(p), idx, c, (len(t) - len(p) + 1)])
    write_csv("q3_string_matching.csv",
              ["test", "n", "m", "match_index", "char_comparisons", "alignments"], rows)

    # growth of the worst case with m for fixed n
    g = []
    for mm in [5, 10, 20, 50, 100, 200, 500]:
        t = "a" * n
        p = "a" * (mm - 1) + "b"
        _, c = brute_force_match(t, p)
        g.append([n, mm, c, (n - mm + 1) * mm])
    write_csv("q3_worst_case_growth.csv", ["n", "m", "measured", "(n-m+1)*m"], g)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([x[1] for x in g], [x[2] for x in g], marker="o", label="measured")
    ax.plot([x[1] for x in g], [x[3] for x in g], "--", label="(n-m+1)*m")
    ax.set_xlabel("pattern length m (n=10000)")
    ax.set_ylabel("character comparisons")
    ax.set_title("Q3: worst-case growth")
    ax.legend()
    save_plot(fig, "q3_worst_case.png")
    print("Q3 done")


if __name__ == "__main__":
    main()
