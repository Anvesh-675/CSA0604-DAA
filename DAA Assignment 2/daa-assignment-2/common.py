"""Shared helpers: seeded data generators, CSV writing and plotting."""
import csv
import os
import random

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "results")
os.makedirs(DATA_DIR, exist_ok=True)

SEED = 42


def rng(offset=0):
    return random.Random(SEED + offset)


def write_csv(name, header, rows):
    path = os.path.join(DATA_DIR, name)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    return path


def save_plot(fig, name):
    path = os.path.join(DATA_DIR, name)
    fig.savefig(path, dpi=140, bbox_inches="tight")
    return path
