# Facility Location in OPL

Native IBM ILOG CPLEX Optimization Studio implementation of a capacitated facility location problem.

## Files

- `facility_location.mod` — OPL MILP formulation.
- `facility_location.dat` — sample data.

## Run

1. Create or open an OPL project in CPLEX Optimization Studio.
2. Add `facility_location.mod` and `facility_location.dat`.
3. Create a run configuration containing both files.
4. Run with CPLEX.

The execute block prints the objective value, open facilities, customer assignments, and used capacity.
