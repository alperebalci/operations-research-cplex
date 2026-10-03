from __future__ import annotations

from collections import defaultdict
from typing import Iterable


def reconstruct_routes(
    selected_arcs: Iterable[tuple[int, int]], depot: int
) -> list[list[int]]:
    """Convert selected CVRP arcs into ordered depot-to-depot routes.

    Assumes a feasible CVRP solution: each visited customer has exactly one
    selected successor and each route starts/ends at the depot.
    """
    successor: dict[int, list[int]] = defaultdict(list)
    for i, j in selected_arcs:
        successor[i].append(j)

    starts = list(successor.get(depot, []))
    routes: list[list[int]] = []

    for first_customer in starts:
        route = [depot, first_customer]
        current = first_customer
        seen = {depot, first_customer}

        while current != depot:
            next_nodes = successor.get(current, [])
            if len(next_nodes) != 1:
                raise ValueError(
                    f"Cannot reconstruct route: node {current} has "
                    f"{len(next_nodes)} selected successors."
                )
            nxt = next_nodes[0]
            route.append(nxt)
            if nxt == depot:
                break
            if nxt in seen:
                raise ValueError("Cycle detected that does not return to the depot.")
            seen.add(nxt)
            current = nxt

        routes.append(route)

    return routes
