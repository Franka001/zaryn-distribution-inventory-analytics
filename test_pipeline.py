import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from pipeline import read_csv, transform, run

ROOT = Path(__file__).resolve().parent

class FulfillmentTests(unittest.TestCase):
    def setUp(self):
        self.orders = read_csv(ROOT / "data/sample/orders.csv")
        self.shipments = read_csv(ROOT / "data/sample/shipments.csv")

    def test_expected_metrics(self):
        rows = transform(self.orders, self.shipments, "2026-01-31")
        self.assertEqual(sum(r["due_qty"] for r in rows), 25)
        self.assertEqual(sum(r["on_time_filled_qty"] for r in rows), 21)
        self.assertEqual(sum(r["complete_on_time"] for r in rows), 1)
        self.assertEqual(sum(r["eligible_due_line"] for r in rows), 2)
        self.assertEqual(rows[3]["outstanding_qty"], 12)

    def test_duplicate_shipment_rejected(self):
        with self.assertRaises(ValueError):
            transform(self.orders, self.shipments + [self.shipments[0]], "2026-01-31")

    def test_unknown_order_rejected(self):
        with self.assertRaises(ValueError):
            transform(self.orders, [dict(self.shipments[0], order_line_id="UNKNOWN")], "2026-01-31")

    def test_negative_shipment_rejected(self):
        with self.assertRaises(ValueError):
            transform(self.orders, [dict(self.shipments[0], shipped_qty="-1")], "2026-01-31")

    def test_rerun_replaces_output(self):
        with TemporaryDirectory() as folder:
            run(ROOT / "data/sample", folder, "2026-01-31")
            first = (Path(folder) / "fulfillment.csv").read_bytes()
            run(ROOT / "data/sample", folder, "2026-01-31")
            self.assertEqual(first, (Path(folder) / "fulfillment.csv").read_bytes())

if __name__ == "__main__":
    unittest.main()
