# Operations Research with IBM CPLEX

A portfolio repository for mathematical optimization projects implemented with **IBM ILOG CPLEX**.

The repository focuses on formulation, implementation, validation, and interpretation rather than treating the solver as a black box. Where useful, models are implemented through **Python/DOcplex**, native **OPL**, and **CP Optimizer** scheduling constructs.

## Projects

### 1. Capacitated Vehicle Routing Problem (CVRP)

Route a capacity-constrained vehicle fleet from a depot to customers while minimizing total travel distance.

- `cvrp/python/` — Python + DOcplex, CLI, heuristic baseline, visualization, JSON output, and tests.
- `cvrp/opl/` — native OPL model and data.

See [`cvrp/README.md`](cvrp/README.md).

### 2. Multi-Period Production Planning

Plan production, inventory, setup decisions, and overtime capacity across multiple products and periods while minimizing total operating cost.

- `production-planning/opl/` — native OPL MILP.

See [`production-planning/README.md`](production-planning/README.md).

### 3. Capacitated Facility Location

Select facilities to open and assign customers while minimizing fixed opening and assignment costs under capacity constraints.

- `facility-location/opl/` — native OPL MILP.

See [`facility-location/README.md`](facility-location/README.md).

### 4. Workforce Scheduling

Assign employees to day/night shifts subject to staffing demand, availability, workload bounds, and consecutive-work limits.

- `workforce-scheduling/opl/` — native OPL MILP.

See [`workforce-scheduling/README.md`](workforce-scheduling/README.md).

### 5. Job-Shop Scheduling

Sequence machine-dependent operations while respecting job precedence and machine no-overlap constraints, minimizing makespan.

- `job-shop-scheduling/opl/` — OPL model using IBM CP Optimizer.

See [`job-shop-scheduling/README.md`](job-shop-scheduling/README.md).

### 6. Cutting Stock

Choose integer cutting patterns to satisfy item demand using the fewest stock rolls.

- `cutting-stock/opl/` — pattern-based integer programming model.

See [`cutting-stock/README.md`](cutting-stock/README.md).

## Repository structure

```text
.
├── cvrp/
│   ├── python/
│   ├── opl/
│   └── results/
├── production-planning/
│   └── opl/
├── facility-location/
│   └── opl/
├── workforce-scheduling/
│   └── opl/
├── job-shop-scheduling/
│   └── opl/
├── cutting-stock/
│   └── opl/
├── .github/workflows/tests.yml
├── LICENSE
└── README.md
```

## Modeling interfaces

- **DOcplex + CPLEX** for Python-integrated mathematical programming.
- **OPL + CPLEX** for algebraic MILP/integer programming models.
- **OPL + CP Optimizer** for scheduling models with interval variables and no-overlap constraints.

## Current scope

The repository currently covers routing, production planning, facility location, workforce scheduling, job-shop scheduling, and cutting stock. Natural extensions include vehicle-routing time windows, bin packing, project scheduling, assignment variants, and supply-network design.

## License

Original code in this repository is MIT licensed. IBM CPLEX, DOcplex, CP Optimizer, and CPLEX Optimization Studio are IBM products and are subject to their respective licensing terms.
