"""Synthetic fulfillment demo; Python standard library only."""
import argparse
import csv
from datetime import date
from pathlib import Path


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def transform(orders, shipments, as_of):
    cutoff = date.fromisoformat(as_of)
    indexed = {}
    for row in orders:
        key = row["order_line_id"]
        if key in indexed:
            raise ValueError("Duplicate order line: " + key)
        ordered, cancelled = int(row["ordered_qty"]), int(row["cancelled_qty"])
        if ordered < 0 or not 0 <= cancelled <= ordered:
            raise ValueError("Invalid order quantities: " + key)
        promised = date.fromisoformat(row["promised_date"])
        indexed[key] = dict(row, net=ordered-cancelled, promised=promised)
    seen, totals, timely = set(), {}, {}
    for row in shipments:
        key, shipment = row["order_line_id"], row["shipment_line_id"]
        if shipment in seen:
            raise ValueError("Duplicate shipment line: " + shipment)
        seen.add(shipment)
        if key not in indexed:
            raise ValueError("Unknown order line: " + key)
        qty = int(row["shipped_qty"])
        if qty < 0:
            raise ValueError("Negative shipment quantity")
        shipped = date.fromisoformat(row["ship_date"])
        if shipped <= cutoff:
            totals[key] = totals.get(key, 0) + qty
            if shipped <= indexed[key]["promised"]:
                timely[key] = timely.get(key, 0) + qty
    results = []
    for key, row in sorted(indexed.items()):
        net, shipped = row["net"], totals.get(key, 0)
        eligible = net > 0 and row["promised"] <= cutoff
        results.append(dict(order_line_id=key, product_id=row["product_id"],
            warehouse_id=row["warehouse_id"], net_ordered_qty=net,
            shipped_qty=shipped, outstanding_qty=max(net-shipped, 0),
            overshipped_qty=max(shipped-net, 0), eligible_due_line=int(eligible),
            due_qty=net if eligible else 0,
            on_time_filled_qty=min(timely.get(key, 0), net) if eligible else 0,
            complete_on_time=int(eligible and timely.get(key, 0) >= net)))
    return results


def run(source, target, as_of):
    source, target = Path(source), Path(target)
    rows = transform(read_csv(source / "orders.csv"), read_csv(source / "shipments.csv"), as_of)
    if not rows:
        raise ValueError("No orders supplied")
    target.mkdir(parents=True, exist_ok=True)
    with (target / "fulfillment.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="data/sample")
    parser.add_argument("--target", default="output")
    parser.add_argument("--as-of", default="2026-01-31")
    args = parser.parse_args()
    run(args.source, args.target, args.as_of)
