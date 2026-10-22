# DAA Assignment 2 (CO2): Brute-Force and Exhaustive Search

Experiments for Design and Analysis of Algorithms, Assignment 2. Every question is implemented in plain Python with
**operation counters** (comparisons, swaps/moves, pairs, character comparisons, side tests, candidates), because
counts are the primary evidence; execution time is recorded only as supporting data.

## Layout

| File | Question | What it does |
|---|---|---|
| `q1_sorting.py` | Q1 | Selection, Bubble (with/without early exit), Insertion sort on six input conditions |
| `q2_sequential_search.py` | Q2 | Sequential search on tool-issue records: first/middle/last/unsuccessful, four list sizes |
| `q3_string_matching.py` | Q3 | Brute-force string matching with character-comparison counter |
| `q4_closest_pair.py` | Q4 | Brute-force closest pair, pairs examined and distance calculations |
| `q5_convex_hull.py` | Q5 | Brute-force convex hull from the half-plane rule, plots, cross-check against monotone chain |
| `q6_q7_exhaustive_knapsack.py` | Q6, Q7 | Exhaustive search for the payload problem (Q6) and the pruned redesign (Q7) |
| `common.py` | all | Seeded random generator, CSV and plot helpers |
| `run_all.py` | all | Runs every experiment |
| `results/` | all | Raw CSV data and PNG graphs used in the report |

## Run

```bash
pip install -r requirements.txt
python run_all.py          # about 1.5 minutes, dominated by the n=24 exhaustive search in Q6/Q7
```

Each script can also be run alone, e.g. `python q4_closest_pair.py`.

## Reproducibility

* All random data uses a fixed seed (`SEED = 42` in `common.py`), so **operation counts are identical on every run**.
* Execution times depend on the machine and will differ from the report. Counts will not.
* Tested with Python 3.13 and matplotlib.

## Counting conventions

* Q1: a *comparison* is one comparison between two array elements. A *swap* is one exchange (Selection, Bubble);
  for Insertion Sort a *move* is one element write (each shift, plus the final placement of the key).
* Q2: one comparison = one `tool_id` equality check.
* Q3: one comparison = one text character compared with one pattern character.
* Q4: one pair examined = one distance calculation (squared distance, no square root until the end).
* Q5: one side test = one evaluation of the cross-product sign for a third point.
* Q6: one candidate = one complete subset of packages (an n-bit mask).
* Q7: the redesign counts every node of its decision tree (partial solutions included), which is a conservative
  comparison against the exhaustive search's complete candidates.
