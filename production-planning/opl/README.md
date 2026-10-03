# Production Planning in OPL

This directory contains a native IBM ILOG CPLEX Optimization Studio model for a multi-product, multi-period capacitated production planning problem.

## Files

- `production_planning.mod` — OPL MILP model.
- `production_planning.dat` — sample data for three products across six periods.

## Run in CPLEX Optimization Studio

1. Create or open an OPL project.
2. Add `production_planning.mod` and `production_planning.dat`.
3. Create a run configuration containing both files.
4. Run the configuration with CPLEX.

## Decision variables

- `production[p][t]`: quantity of product `p` produced in period `t`.
- `inventory[p][t]`: end-of-period inventory.
- `setup[p][t]`: binary setup decision.
- `overtime[t]`: overtime capacity used.

## Objective

Minimize the sum of:

- variable production cost,
- fixed setup cost,
- inventory holding cost,
- overtime capacity cost.

## Constraints

The model enforces:

- inventory flow balance for every product and period,
- fixed initial inventory,
- minimum terminal inventory,
- shared regular-capacity plus overtime limits,
- maximum overtime per period,
- setup-to-production linking constraints.

The `execute` block prints the objective value, period-level capacity usage, overtime, and product-level production/inventory decisions.
