# Capacitated Vehicle Routing Problem (CVRP)

This project solves a small Capacitated Vehicle Routing Problem with IBM ILOG CPLEX in two ways:

1. **Python + DOcplex** — application-style implementation with input validation, CLI, heuristic baseline, JSON export, visualization, and tests.
2. **OPL** — native CPLEX Optimization Studio implementation using `.mod` and `.dat` files.

Both versions use the same sample instance and the same MILP structure.

## Mathematical formulation

Let `V` be all nodes, `C = V \ {0}` the customer set, `Q` vehicle capacity, `K` the maximum number of vehicles, and `c_ij` the distance between nodes.

Decision variables:

- `x_ij = 1` if arc `(i,j)` is used.
- `u_i` is cumulative vehicle load after serving customer `i`.

Objective:

```text
min  Σ_i Σ_j c_ij x_ij
```

Core constraints:

- each customer has exactly one incoming arc,
- each customer has exactly one outgoing arc,
- depot departures/returns are limited by `K`,
- depot flow is balanced,
- MTZ-style load propagation enforces capacity and removes customer-only subtours.

For distinct customers `i` and `j`:

```text
u_j >= u_i + demand_j - Q(1 - x_ij)
demand_i <= u_i <= Q
```

## Python / DOcplex

```bash
cd cvrp/python
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -e .

cvrp-cplex --input sample_instance.json --output ../results/solution.json
```

A compatible IBM CPLEX runtime/API is required to solve the DOcplex model. Unit tests and the heuristic baseline do not require a CPLEX solve.

Run tests:

```bash
cd cvrp/python
python -m unittest discover -s tests -v
```

## Native OPL

Open `cvrp/opl/cvrp.mod` with `cvrp/opl/cvrp.dat` in IBM ILOG CPLEX Optimization Studio and run the model with CPLEX.

See [`opl/README.md`](opl/README.md) for details.
