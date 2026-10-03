from __future__ import annotations

from dataclasses import dataclass

from .io import CVRPInstance


@dataclass(frozen=True)
class HeuristicResult:
    objective: float
    routes: tuple[tuple[int, ...], ...]


def nearest_neighbor(instance: CVRPInstance) -> HeuristicResult:
    """Capacity-aware nearest-neighbor baseline.

    This is intentionally simple: it repeatedly starts a route at the depot,
    chooses the nearest unserved customer that still fits, and returns to the
    depot when no additional customer can be added.
    """
    unserved = set(instance.customer_ids)
    routes: list[tuple[int, ...]] = []
    total_distance = 0.0

    while unserved:
        if len(routes) >= instance.max_vehicles:
            raise ValueError(
                "Nearest-neighbor baseline needs more vehicles than max_vehicles."
            )

        current = instance.depot
        remaining_capacity = instance.vehicle_capacity
        route = [instance.depot]

        while True:
            feasible = [
                j for j in unserved if instance.demand(j) <= remaining_capacity
            ]
            if not feasible:
                break

            nxt = min(
                feasible,
                key=lambda j: (instance.distance(current, j), j),
            )
            total_distance += instance.distance(current, nxt)
            route.append(nxt)
            remaining_capacity -= instance.demand(nxt)
            unserved.remove(nxt)
            current = nxt

        if len(route) == 1:
            raise ValueError("No unserved customer can fit into an empty vehicle.")

        total_distance += instance.distance(current, instance.depot)
        route.append(instance.depot)
        routes.append(tuple(route))

    return HeuristicResult(
        objective=total_distance,
        routes=tuple(routes),
    )
