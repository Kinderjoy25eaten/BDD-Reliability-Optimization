# BDD Reliability Optimization for Phased Mission Systems

This repository contains a recursive ROBDD engine implemented in Python to validate the efficiency of the **Modified Backward Phase-Dependent Operation (PDO)** and the **Superscript Rule**.

## Key Highlights
- **Linear Growth**: Proves that reliability modeling can scale linearly ($O(M)$) with mission phases.
- [cite_start]**Node Merging**: Demonstrates the physical collapse of redundant state-spaces using the Superscript Rule: $x^i \cdot x^{i+1} = x^{(i, i+1)}$[cite: 376, 377].
- [cite_start]**Benchmark Results**: At 100 mission phases, our approach reduces model scale and recursive calls by orders of magnitude compared to traditional forward-based methods.

## Usage
Run `main.py` to generate the three-panel benchmark plots for Model Scale, Construction Time, and Recursive Calls.
