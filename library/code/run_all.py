# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Tyler O'Bryan, where applicable
"""Runs every example program in this folder. Plain Python 3 only.   Usage:  python3 run_all.py"""
import importlib, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
for name in ("hypercube_counts", "tetragon", "controlled_sum", "herald_reliability", "memory_thresholds", "two_tetragons"):
    print("=" * 8, name)
    importlib.import_module(name).main()
print("\nALL EXAMPLES PASS")
