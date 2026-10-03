import unittest

from cvrp.routes import reconstruct_routes


class TestRoutes(unittest.TestCase):
    def test_reconstructs_multiple_routes(self):
        arcs = [(0, 1), (1, 2), (2, 0), (0, 3), (3, 0)]
        routes = reconstruct_routes(arcs, depot=0)
        self.assertEqual(routes, [[0, 1, 2, 0], [0, 3, 0]])

    def test_rejects_non_depot_cycle(self):
        arcs = [(0, 1), (1, 2), (2, 1)]
        with self.assertRaises(ValueError):
            reconstruct_routes(arcs, depot=0)


if __name__ == "__main__":
    unittest.main()
