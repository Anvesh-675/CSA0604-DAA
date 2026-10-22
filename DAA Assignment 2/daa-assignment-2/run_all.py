"""Run every experiment; outputs go to ./results (CSV + PNG)."""
import q1_sorting, q2_sequential_search, q3_string_matching, q4_closest_pair, q5_convex_hull, q6_q7_exhaustive_knapsack

for m in (q1_sorting, q2_sequential_search, q3_string_matching, q4_closest_pair, q5_convex_hull,
          q6_q7_exhaustive_knapsack):
    m.main()
