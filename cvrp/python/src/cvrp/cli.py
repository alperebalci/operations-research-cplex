from __future__ import annotations

import argparse
import json
from pathlib import Path

from .heuristic import nearest_neighbor
from .io import load_instance
from .model import solve_instance
from .visualize import plot_routes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Solve a Capacitated Vehicle Routing Problem with DOcplex/CPLEX."
    )
    parser.add_argument("--input", required=True, help="Path to CVRP instance JSON")
    parser.add_argument("--output", help="Optional path for solution JSON")
    parser.add_argument("--plot", help="Optional path for route plot PNG")
    parser.add_argument("--time-limit", type=float, default=None, help="CPLEX time limit in seconds")
    parser.add_argument("--mip-gap", type=float, default=None, help="Relative MIP optimality gap")
    parser.add_argument("--quiet", action="store_true", help="Disable solver log output")
    parser.add_argument(
        "--baseline-only",
        action="store_true",
        help="Run the nearest-neighbor heuristic without invoking CPLEX",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    instance = load_instance(args.input)
    baseline = nearest_neighbor(instance)

    if args.baseline_only:
        payload = {
            "method": "nearest_neighbor",
            "objective": baseline.objective,
            "routes": [list(route) for route in baseline.routes],
        }
        routes_for_plot = baseline.routes
    else:
        result = solve_instance(
            instance,
            time_limit=args.time_limit,
            mip_gap=args.mip_gap,
            log_output=not args.quiet,
        )
        payload = result.as_dict()
        payload["baseline"] = {
            "method": "nearest_neighbor",
            "objective": baseline.objective,
            "routes": [list(route) for route in baseline.routes],
        }
        if result.objective is not None and baseline.objective > 0:
            payload["improvement_over_baseline_pct"] = (
                100.0 * (baseline.objective - result.objective) / baseline.objective
            )
        routes_for_plot = result.routes

    print(json.dumps(payload, indent=2))

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if args.plot and routes_for_plot:
        plot_routes(instance, routes_for_plot, args.plot)


if __name__ == "__main__":
    main()
