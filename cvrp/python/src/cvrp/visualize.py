from __future__ import annotations

from pathlib import Path

from .io import CVRPInstance


def plot_routes(
    instance: CVRPInstance,
    routes: list[list[int]] | tuple[tuple[int, ...], ...],
    output_path: str | Path,
) -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 7))

    depot = instance.node_by_id(instance.depot)
    customers = [node for node in instance.nodes if node.id != instance.depot]

    ax.scatter([n.x for n in customers], [n.y for n in customers], s=55)
    ax.scatter([depot.x], [depot.y], marker="s", s=120)

    for node in instance.nodes:
        label = f"{node.id}" if node.id == instance.depot else f"{node.id} (d={node.demand:g})"
        ax.annotate(label, (node.x, node.y), xytext=(5, 5), textcoords="offset points")

    for route in routes:
        xs = [instance.node_by_id(node_id).x for node_id in route]
        ys = [instance.node_by_id(node_id).y for node_id in route]
        ax.plot(xs, ys, marker="o", linewidth=1.8)

    ax.set_title(f"CVRP routes — {instance.name}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=160)
    plt.close(fig)
