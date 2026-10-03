from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any

from .io import CVRPInstance
from .routes import reconstruct_routes


@dataclass(frozen=True)
class SolveResult:
    status: str
    objective: float | None
    solve_time_seconds: float
    mip_gap: float | None
    selected_arcs: tuple[tuple[int, int], ...]
    routes: tuple[tuple[int, ...], ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "objective": self.objective,
            "solve_time_seconds": self.solve_time_seconds,
            "mip_gap": self.mip_gap,
            "selected_arcs": [list(arc) for arc in self.selected_arcs],
            "routes": [list(route) for route in self.routes],
        }


def build_model(instance: CVRPInstance):
    try:
        from docplex.mp.model import Model
    except ImportError as exc:
        raise RuntimeError(
            "DOcplex is not installed. Run `pip install -e .` first."
        ) from exc

    nodes = instance.node_ids
    customers = instance.customer_ids
    depot = instance.depot
    capacity = instance.vehicle_capacity

    mdl = Model(name=f"cvrp_{instance.name}")

    arcs = [(i, j) for i in nodes for j in nodes if i != j]
    x = mdl.binary_var_dict(arcs, name="x")

    # Cumulative vehicle load after serving customer i.
    u = {
        i: mdl.continuous_var(
            lb=instance.demand(i),
            ub=capacity,
            name=f"u_{i}",
        )
        for i in customers
    }

    mdl.minimize(
        mdl.sum(instance.distance(i, j) * x[i, j] for i, j in arcs)
    )

    # Every customer is entered and left exactly once.
    for i in customers:
        mdl.add_constraint(
            mdl.sum(x[i, j] for j in nodes if j != i) == 1,
            ctname=f"leave_{i}",
        )
        mdl.add_constraint(
            mdl.sum(x[j, i] for j in nodes if j != i) == 1,
            ctname=f"enter_{i}",
        )

    # Number of routes is limited by the available fleet.
    mdl.add_constraint(
        mdl.sum(x[depot, j] for j in customers) <= instance.max_vehicles,
        ctname="fleet_departures",
    )
    mdl.add_constraint(
        mdl.sum(x[i, depot] for i in customers) <= instance.max_vehicles,
        ctname="fleet_returns",
    )

    # Flow balance at the depot ensures the same number of departures/returns.
    mdl.add_constraint(
        mdl.sum(x[depot, j] for j in customers)
        == mdl.sum(x[i, depot] for i in customers),
        ctname="depot_flow_balance",
    )

    # Capacity + subtour elimination for customer-to-customer arcs.
    for i in customers:
        for j in customers:
            if i == j:
                continue
            mdl.add_constraint(
                u[j]
                >= u[i] + instance.demand(j) - capacity * (1 - x[i, j]),
                ctname=f"load_{i}_{j}",
            )

    return mdl, x, u


def solve_instance(
    instance: CVRPInstance,
    *,
    time_limit: float | None = None,
    mip_gap: float | None = None,
    log_output: bool = True,
) -> SolveResult:
    mdl, x, _ = build_model(instance)

    if time_limit is not None:
        mdl.parameters.timelimit = float(time_limit)
    if mip_gap is not None:
        mdl.parameters.mip.tolerances.mipgap = float(mip_gap)

    start = perf_counter()
    try:
        solution = mdl.solve(log_output=log_output)
    except Exception as exc:  # solver runtime/licensing errors vary by installation
        raise RuntimeError(
            "The model was built successfully, but CPLEX could not solve it. "
            "Verify that a compatible IBM CPLEX runtime/API is installed and "
            "available to this Python environment."
        ) from exc
    elapsed = perf_counter() - start

    details = mdl.solve_details
    status = str(details.status)

    if solution is None:
        return SolveResult(
            status=status,
            objective=None,
            solve_time_seconds=elapsed,
            mip_gap=None,
            selected_arcs=tuple(),
            routes=tuple(),
        )

    selected_arcs = tuple(
        sorted((i, j) for (i, j), var in x.items() if solution.get_value(var) > 0.5)
    )
    routes = tuple(tuple(r) for r in reconstruct_routes(selected_arcs, instance.depot))

    gap = None
    try:
        gap = float(details.mip_relative_gap)
    except (TypeError, ValueError, AttributeError):
        pass

    return SolveResult(
        status=status,
        objective=float(solution.objective_value),
        solve_time_seconds=elapsed,
        mip_gap=gap,
        selected_arcs=selected_arcs,
        routes=routes,
    )
