"""Q5 - Brute-force convex hull derived from the half-plane property.

For points P1=(x1,y1), P2=(x2,y2) the line through them is  a*x + b*y = c  with
    a = y2 - y1,  b = x1 - x2,  c = x1*y2 - y1*x2.
For any other point P, the sign of  s = a*x + b*y - c  tells which side P is on
(this equals minus the cross product (P2-P1) x (P-P1); the code uses the cross product, only the sign convention differs).  Segment P1P2 is a hull edge
iff every other point has s >= 0 or every other point has s <= 0
(points lying ON the line are allowed only if they lie between P1 and P2, otherwise
P1P2 is not the maximal edge; the code keeps extreme endpoints only).
"""
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import rng, write_csv, save_plot


def side(p1, p2, p):
    return (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0])


def on_segment(p1, p2, p):
    return (min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and
            min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1]))


def hull_edges_bf(pts):
    """Return (edges, side_tests). Handles collinear points by keeping only extreme vertices."""
    n = len(pts)
    edges = []
    tests = 0
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = pts[i], pts[j]
            pos = neg = False
            ok = True
            for k in range(n):
                if k == i or k == j:
                    continue
                tests += 1
                s = side(p1, p2, pts[k])
                if s > 0:
                    pos = True
                elif s < 0:
                    neg = True
                else:
                    # collinear: valid only if lies within the segment; otherwise P1P2 is a sub-segment
                    if not on_segment(p1, p2, pts[k]):
                        ok = False
                        break
                if pos and neg:
                    ok = False
                    break
            if ok:
                edges.append((p1, p2))
    return edges, tests


def order_hull(edges):
    """Stitch undirected edges into a closed ordered polygon."""
    if not edges:
        return []
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    start = edges[0][0]
    poly = [start]
    prev, cur = None, start
    while True:
        nxts = [x for x in adj[cur] if x != prev]
        nxt = nxts[0] if nxts else None
        if nxt is None or nxt == start:
            break
        poly.append(nxt)
        prev, cur = cur, nxt
        if len(poly) > len(adj):
            break
    return poly


def plot_hull(pts, edges, title, name):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=18, color="gray")
    for a, b in edges:
        ax.plot([a[0], b[0]], [a[1], b[1]], "r-")
    hv = {p for e in edges for p in e}
    ax.scatter([p[0] for p in hv], [p[1] for p in hv], s=30, color="red")
    ax.set_title(title)
    ax.set_aspect("equal")
    save_plot(fig, name)


def main():
    r = rng(5)
    # Test 1: boundary + interior points
    pts1 = [(0, 0), (10, 0), (10, 10), (0, 10), (5, 5), (3, 7), (7, 2), (4, 4), (6, 8), (2, 3)]
    e1, t1 = hull_edges_bf(pts1)
    plot_hull(pts1, e1, "Test 1: boundary + interior points", "q5_hull_test1.png")
    # Test 2: adversarial - collinear points on edges, duplicate-like clustering, all on a hull-ish circle
    pts2 = [(0, 0), (5, 0), (10, 0), (10, 5), (10, 10), (5, 10), (0, 10), (0, 5), (5, 5), (2, 2), (8, 8)]
    e2, t2 = hull_edges_bf(pts2)
    plot_hull(pts2, e2, "Test 2: collinear points on boundary", "q5_hull_test2.png")
    # Test 3: all points collinear
    pts3 = [(i, 2 * i) for i in range(6)]
    e3, t3 = hull_edges_bf(pts3)
    write_csv("q5_tests.csv", ["test", "n", "hull_edges", "hull_vertices", "side_tests"],
              [["1 boundary+interior", len(pts1), len(e1), len({p for e in e1 for p in e}), t1],
               ["2 collinear on boundary", len(pts2), len(e2), len({p for e in e2 for p in e}), t2],
               ["3 all collinear", len(pts3), len(e3), len({p for e in e3 for p in e}), t3]])
    # cross-check vs Andrew's monotone chain for random sets
    def monotone(points):
        P = sorted(set(points))
        if len(P) <= 2:
            return P
        def cross(o, a, b):
            return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
        lo, up = [], []
        for p in P:
            while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
                lo.pop()
            lo.append(p)
        for p in reversed(P):
            while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
                up.pop()
            up.append(p)
        return lo[:-1] + up[:-1]

    agree = 0
    for _ in range(50):
        pts = list({(r.randint(0, 30), r.randint(0, 30)) for _ in range(25)})
        e, _ = hull_edges_bf(pts)
        if {p for ed in e for p in ed} == set(monotone(pts)):
            agree += 1
    print("Q5 cross-check agreements:", agree, "/ 50")

    rows = []
    for n in [20, 40, 80, 160, 320]:
        pts = list({(r.uniform(0, 1000), r.uniform(0, 1000)) for _ in range(n)})
        t0 = time.perf_counter()
        e, tests = hull_edges_bf(pts)
        dt = (time.perf_counter() - t0) * 1000
        rows.append([n, len(e), tests, n * (n - 1) // 2, round(dt, 2)])
    write_csv("q5_growth.csv", ["n", "hull_edges", "side_tests", "pairs_n(n-1)/2", "time_ms"], rows)
    write_csv("q5_crosscheck.csv", ["random_sets", "agreements_with_monotone_chain"], [[50, agree]])

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([x[0] for x in rows], [x[2] for x in rows], marker="o", label="side tests")
    ax.set_xlabel("n")
    ax.set_ylabel("side tests")
    ax.set_title("Q5: work growth (random points)")
    ax.legend()
    save_plot(fig, "q5_growth.png")
    print("Q5 done")


if __name__ == "__main__":
    main()
