# Multi-Period Production Planning

This project models a **capacitated multi-product production planning problem** as a mixed-integer linear program (MILP) in IBM ILOG CPLEX Optimization Studio using OPL.

The model decides, for each product and planning period:

- how much to produce,
- whether production should be set up,
- how much inventory to carry,
- how much overtime capacity to purchase.

The objective is to minimize total production, setup, inventory holding, and overtime costs while satisfying demand and capacity constraints.

## Why this model?

This project complements the CVRP example with a different class of operations-research problem. It demonstrates:

- multi-period inventory balance,
- binary setup decisions,
- fixed-charge production costs,
- shared capacity constraints,
- overtime trade-offs,
- linking constraints using Big-M bounds,
- terminal inventory requirements.

## OPL implementation

The native OPL implementation is in `opl/`.

Files:

- `production_planning.mod` — optimization model.
- `production_planning.dat` — sample six-period, three-product instance.
- `README.md` — execution and formulation notes.

## Mathematical structure

For product `p` and period `t`:

- `production[p][t]` = production quantity,
- `inventory[p][t]` = end-of-period inventory,
- `setup[p][t]` = 1 when product `p` is produced in period `t`,
- `overtime[t]` = extra capacity purchased in period `t`.

Inventory balance:

```text
inventory[p,t-1] + production[p,t]
    = demand[p,t] + inventory[p,t]
```

Setup linkage:

```text
production[p,t] <= maxProduction[p,t] * setup[p,t]
```

Capacity:

```text
Σ_p processingTime[p] * production[p,t]
    <= regularCapacity[t] + overtime[t]
```

The terminal inventory requirement prevents the model from depleting all stock merely to reduce cost at the end of the planning horizon.
