# Cutting Stock

This project implements a pattern-based one-dimensional cutting stock model in IBM ILOG CPLEX Optimization Studio using OPL.

Given a fixed stock length, item lengths, demand, and a predefined set of feasible cutting patterns, the integer program minimizes the number of stock rolls required.

The model demonstrates:

- nonnegative integer decision variables,
- covering constraints,
- pattern-based modeling,
- material utilization and waste calculation.

The native OPL implementation is in `opl/`.
