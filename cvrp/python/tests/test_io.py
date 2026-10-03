import json
import tempfile
import unittest
from pathlib import Path

from cvrp.io import load_instance


class TestIO(unittest.TestCase):
    def _write(self, payload: dict) -> Path:
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        with tmp:
            json.dump(payload, tmp)
        return Path(tmp.name)

    def test_valid_instance(self):
        path = self._write(
            {
                "name": "test",
                "vehicle_capacity": 10,
                "max_vehicles": 1,
                "depot": 0,
                "nodes": [
                    {"id": 0, "x": 0, "y": 0, "demand": 0},
                    {"id": 1, "x": 3, "y": 4, "demand": 5},
                ],
            }
        )
        instance = load_instance(path)
        self.assertEqual(instance.customer_ids, (1,))
        self.assertAlmostEqual(instance.distance(0, 1), 5.0)

    def test_rejects_customer_above_vehicle_capacity(self):
        path = self._write(
            {
                "vehicle_capacity": 4,
                "max_vehicles": 2,
                "depot": 0,
                "nodes": [
                    {"id": 0, "x": 0, "y": 0, "demand": 0},
                    {"id": 1, "x": 1, "y": 1, "demand": 5},
                ],
            }
        )
        with self.assertRaises(ValueError):
            load_instance(path)

    def test_rejects_insufficient_total_fleet_capacity(self):
        path = self._write(
            {
                "vehicle_capacity": 5,
                "max_vehicles": 1,
                "depot": 0,
                "nodes": [
                    {"id": 0, "x": 0, "y": 0, "demand": 0},
                    {"id": 1, "x": 1, "y": 1, "demand": 3},
                    {"id": 2, "x": 2, "y": 2, "demand": 3},
                ],
            }
        )
        with self.assertRaises(ValueError):
            load_instance(path)


if __name__ == "__main__":
    unittest.main()
