# Capacitated Facility Location

This project implements the **Capacitated Facility Location Problem (CFLP)** in IBM ILOG CPLEX Optimization Studio using OPL.

The model decides:

- which candidate facilities to open,
- which facility serves each customer,
- how to respect facility-capacity limits.

The objective minimizes fixed facility-opening costs plus customer assignment/transportation costs.

## Why this model?

Facility location is a classic strategic operations-research problem that complements routing and production planning. It demonstrates:

- binary facility-opening decisions,
- binary customer-assignment decisions,
- linking constraints,
- capacity constraints,
- fixed-charge optimization,
- strategic network-design trade-offs.

## OPL files

- `facility_location.mod` — MILP model.
- `facility_location.dat` — sample instance with four candidate facilities and eight customers.
- `README.md` — model and execution notes.

## Mathematical structure

Decision variables:

- `open[f] = 1` if facility `f` is opened.
- `assign[f][c] = 1` if customer `c` is served by facility `f`.

Objective:

```text
min  Σ_f fixedCost[f] * open[f]
   + Σ_f Σ_c assignmentCost[f,c] * assign[f,c]
```

Assignment:

```text
Σ_f assign[f,c] = 1      for every customer c
```

Linking:

```text
assign[f,c] <= open[f]
```

Capacity:

```text
Σ_c demand[c] * assign[f,c] <= capacity[f] * open[f]
```

## Sample-instance verification

The small sample instance was independently checked by exhaustive enumeration. The best objective is `2460`, with the South and West facilities open. This provides a reference value for validating a local CPLEX/OPL run.

Open the `.mod` and `.dat` files in IBM ILOG CPLEX Optimization Studio and run them with CPLEX.
