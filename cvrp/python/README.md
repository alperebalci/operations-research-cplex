# CVRP with Python and DOcplex

Python implementation of the Capacitated Vehicle Routing Problem using IBM DOcplex as the modeling API and IBM ILOG CPLEX as the solver engine.

Features include instance validation, a MILP formulation, CLI execution, a capacity-aware nearest-neighbor baseline, JSON result export, route visualization, and unit tests.

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -e .

cvrp-cplex --input sample_instance.json --output ../results/solution.json
```

A compatible CPLEX runtime/API is required for the exact solve. The heuristic baseline and unit tests do not require CPLEX.
