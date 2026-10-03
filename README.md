# Operations Research with IBM CPLEX

A portfolio repository for mathematical optimization projects implemented with **IBM ILOG CPLEX**.

The repository focuses on formulation, implementation, validation, and interpretation rather than treating the solver as a black box. Where useful, models are implemented through **Python/DOcplex** and/or CPLEX's native **OPL (Optimization Programming Language)**.

## Projects

### 1. Capacitated Vehicle Routing Problem (CVRP)

Route a capacity-constrained vehicle fleet from a depot to a set of customers while minimizing total travel distance.

Implemented in:

- `cvrp/python/` — Python + DOcplex, CLI, heuristic baseline, visualization, JSON output, and tests.
- `cvrp/opl/` — native OPL model (`.mod`) and data (`.dat`).

The formulation uses binary arc variables and MTZ-style cumulative-load constraints for capacity enforcement and subtour elimination.

See [`cvrp/README.md`](cvrp/README.md).

### 2. Multi-Period Production Planning

Plan production, inventory, setup decisions, and overtime capacity across multiple products and periods while minimizing total operating cost.

Implemented in:

- `production-planning/opl/` — native OPL MILP model and a three-product, six-period sample instance.

The formulation includes inventory-flow equations, binary setup decisions, Big-M production/setup linking, shared capacity, overtime, and terminal inventory targets.

See [`production-planning/README.md`](production-planning/README.md).

### 3. Capacitated Facility Location

Select facilities to open and assign customers to them while minimizing fixed opening and assignment costs under capacity constraints.

Implemented in:

- `facility-location/opl/` — native OPL MILP model with four candidate facilities and eight customers.

The formulation combines binary facility-opening decisions, binary customer assignments, linking constraints, and capacity limits.

See [`facility-location/README.md`](facility-location/README.md).

## Repository structure

```text
.
├── cvrp/
│   ├── python/
│   ├── opl/
│   ├── results/
│   └── README.md
├── production-planning/
│   ├── opl/
│   │   ├── production_planning.mod
│   │   ├── production_planning.dat
│   │   └── README.md
│   └── README.md
├── facility-location/
│   ├── opl/
│   │   ├── facility_location.mod
│   │   ├── facility_location.dat
│   │   └── README.md
│   └── README.md
├── .github/workflows/tests.yml
├── LICENSE
└── README.md
```

## Modeling interfaces

DOcplex is useful when optimization is embedded in a Python data/application workflow. OPL is a compact algebraic modeling language designed specifically for IBM ILOG CPLEX Optimization Studio. The repository uses both styles to demonstrate mathematical modeling as well as application-oriented solver integration.

## Current scope

The repository currently covers vehicle routing, multi-period production planning, and capacitated facility location. Natural extensions include workforce scheduling, job-shop scheduling, cutting stock, and vehicle-routing time windows.

## License

Original code in this repository is MIT licensed. IBM CPLEX, DOcplex, and CPLEX Optimization Studio are IBM products and are subject to their respective licensing terms.
