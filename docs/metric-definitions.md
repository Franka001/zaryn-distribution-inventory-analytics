# Proposed Metric Definitions

These are demonstration rules to implement and test, not universal industry definitions. All quantities must be converted to an agreed product base unit before aggregation. Every report must disclose its as-of timestamp and date filters.

## On-Hand Inventory

Sum the reported stock quantity from the latest successful snapshot at or before the selected as-of timestamp for each product and warehouse. Do not sum stock snapshots across dates. On-hand does not mean available-to-promise; allocation and reservation data would be required for that calculation.

## Outstanding Order Quantity

At order-line grain: max(ordered quantity minus cancelled quantity minus cumulative shipped quantity, 0), evaluated as of the selected timestamp. Identify over-shipments separately rather than hiding them. Returns do not reopen an order automatically in this demonstration.

## On-Time Quantity Fill Rate

For non-cancelled order lines due within the selected period, divide the sum of quantity shipped by the promised date, capped at each line's net ordered quantity, by the sum of net ordered quantity. Net ordered quantity is ordered minus cancelled quantity as of the reporting cutoff. Exclude zero-net-quantity lines. Return blank when the denominator is zero. Partial on-time shipments contribute proportionally. Use the promised date recorded at order acceptance for this demonstration; later promise changes must not silently rewrite the baseline.

## Order-Line Completion Rate by Promise Date

Number of eligible order lines fully shipped by their promised date divided by all eligible order lines due in the selected period. This is a line-count metric, unlike the quantity-based fill rate. Return blank when no lines are eligible.

## Low-Activity Stock

Flag product/warehouse combinations with positive on-hand quantity and no outbound shipment during a configurable lookback ending at the as-of timestamp. This is an activity flag, not FIFO inventory aging or proof that stock is obsolete.

## Required Edge-Case Tests

Partial shipments; multiple shipments per order line; cancellations before and after shipment; late-arriving events; zero denominators; over-shipments; warehouse transfers; missing unit conversions; and negative stock. Document the treatment of each before publishing report results.
