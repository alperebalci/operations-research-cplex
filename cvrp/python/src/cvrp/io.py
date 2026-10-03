from __future__ import annotations

import json
from dataclasses import dataclass
from math import hypot
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Node:
    id: int
    x: float
    y: float
    demand: float


@dataclass(frozen=True)
class CVRPInstance:
    name: str
    vehicle_capacity: float
    max_vehicles: int
    depot: int
    nodes: tuple[Node, ...]

    @property
    def node_ids(self) -> tuple[int, ...]:
        return tuple(node.id for node in self.nodes)

    @property
    def customer_ids(self) -> tuple[int, ...]:
        return tuple(node.id for node in self.nodes if node.id != self.depot)

    def node_by_id(self, node_id: int) -> Node:
        for node in self.nodes:
            if node.id == node_id:
                return node
        raise KeyError(f"Unknown node id: {node_id}")

    def demand(self, node_id: int) -> float:
        return self.node_by_id(node_id).demand

    def distance(self, i: int, j: int) -> float:
        a = self.node_by_id(i)
        b = self.node_by_id(j)
        return hypot(a.x - b.x, a.y - b.y)


def _validate_unique_ids(nodes: Iterable[Node]) -> None:
    ids = [node.id for node in nodes]
    if len(ids) != len(set(ids)):
        raise ValueError("Node ids must be unique.")


def validate_instance(instance: CVRPInstance) -> None:
    if not instance.nodes:
        raise ValueError("Instance must contain at least one node.")
    _validate_unique_ids(instance.nodes)

    if instance.depot not in instance.node_ids:
        raise ValueError("Depot id must correspond to a node.")
    if instance.vehicle_capacity <= 0:
        raise ValueError("vehicle_capacity must be positive.")
    if instance.max_vehicles <= 0:
        raise ValueError("max_vehicles must be positive.")

    depot = instance.node_by_id(instance.depot)
    if depot.demand != 0:
        raise ValueError("Depot demand must be zero.")

    for node in instance.nodes:
        if node.demand < 0:
            raise ValueError(f"Demand cannot be negative (node {node.id}).")
        if node.id != instance.depot and node.demand > instance.vehicle_capacity:
            raise ValueError(
                f"Node {node.id} demand ({node.demand}) exceeds vehicle capacity "
                f"({instance.vehicle_capacity})."
            )

    total_capacity = instance.max_vehicles * instance.vehicle_capacity
    total_demand = sum(instance.demand(i) for i in instance.customer_ids)
    if total_demand > total_capacity:
        raise ValueError(
            f"Total demand ({total_demand}) exceeds total fleet capacity ({total_capacity})."
        )


def load_instance(path: str | Path) -> CVRPInstance:
    path = Path(path)
    raw = json.loads(path.read_text(encoding="utf-8"))

    try:
        nodes = tuple(
            Node(
                id=int(item["id"]),
                x=float(item["x"]),
                y=float(item["y"]),
                demand=float(item["demand"]),
            )
            for item in raw["nodes"]
        )
        instance = CVRPInstance(
            name=str(raw.get("name", path.stem)),
            vehicle_capacity=float(raw["vehicle_capacity"]),
            max_vehicles=int(raw["max_vehicles"]),
            depot=int(raw["depot"]),
            nodes=nodes,
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid instance file: {path}") from exc

    validate_instance(instance)
    return instance
