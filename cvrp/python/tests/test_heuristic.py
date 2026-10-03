import unittest

from cvrp.heuristic import nearest_neighbor
from cvrp.io import CVRPInstance, Node


class TestHeuristic(unittest.TestCase):
    def test_serves_every_customer_once(self):
        instance = CVRPInstance(
            name="heuristic-test",
            vehicle_capacity=6,
            max_vehicles=2,
            depot=0,
            nodes=(
                Node(0, 0, 0, 0),
                Node(1, 1, 0, 3),
                Node(2, 2, 0, 3),
                Node(3, 10, 0, 3),
            ),
        )
        result = nearest_neighbor(instance)
        visited = [node for route in result.routes for node in route[1:-1]]
        self.assertEqual(sorted(visited), [1, 2, 3])
        self.assertEqual(len(visited), len(set(visited)))
        self.assertLessEqual(len(result.routes), instance.max_vehicles)


if __name__ == "__main__":
    unittest.main()
