# Operations Research with IBM CPLEX

A portfolio repository for mathematical optimization projects implemented with **IBM ILOG CPLEX**.

The repository focuses on formulation, implementation, validation, and interpretation rather than treating the solver as a black box. Where useful, the same model is implemented through both **Python/DOcplex** and CPLEX's native **OPL (Optimization Programming Language)**.

## Projects

### 1. Capacitated Vehicle Routing Problem (CVRP)

Route a capacity-constrained vehicle fleet from a depot to a set of customers while minimizing total travel distance.

Implemented in:

- `cvrp/python/` — Python + DOcplex, CLI, heuristic baseline, visualization, JSON output, and tests.
- `cvrp/opl/` — native OPL model (`.mod`) and data (`.dat`).

The formulation uses binary arc variables and MTZ-style cumulative-load constraints for capacity enforcement and subtour elimination.

See [`cvrp/README.md`](cvrp/README.md).

## Repository structure

```text
.
├── cvrp/
│   ├── python/
│   │   ├── src/cvrp/
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── sample_instance.json
│   ├── opl/
│   │   ├── cvrp.mod
│   │   ├── cvrp.dat
│   │   └── README.md
│   ├── results/
│   └── README.md
├── .github/workflows/tests.yml
├── LICENSE
└── README.md
```

## Why two modeling interfaces?

DOcplex is useful when optimization is embedded in a Python data/application workflow. OPL is a compact algebraic modeling language designed specifically for IBM ILOG CPLEX Optimization Studio. Implementing the same model in both makes the mathematical formulation easier to compare with the application-layer code.

## Current scope

The repository currently contains CVRP. Natural extensions include vehicle-routing time windows, production scheduling, facility location, workforce scheduling, and other mixed-integer programming models.

## License

Original code in this repository is MIT licensed. IBM CPLEX, DOcplex, and CPLEX Optimization Studio are IBM products and are subject to their respective licensing terms.
