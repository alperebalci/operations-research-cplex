# CVRP in OPL

This directory contains a native IBM ILOG CPLEX Optimization Studio implementation of the Capacitated Vehicle Routing Problem (CVRP).

## Files

- `cvrp.mod` — OPL model with binary routing variables and MTZ-style load constraints.
- `cvrp.dat` — sample data matching the Python/DOcplex demo instance.

## Run in CPLEX Optimization Studio

1. Create or open an OPL project.
2. Add `cvrp.mod` and `cvrp.dat`.
3. Create a run configuration using the model and data file.
4. Run with CPLEX as the solver.

The model minimizes total Euclidean travel distance, visits every customer exactly once, respects vehicle capacity, and limits the number of routes to the available fleet.

## Formulation notes

The model uses `x[i][j]` to indicate whether arc `(i,j)` is selected. Continuous cumulative-load variables `u[i]` both enforce capacity and eliminate customer-only subtours through an MTZ-style formulation.

The Python and OPL versions intentionally implement the same mathematical structure so their model definitions can be compared directly.
