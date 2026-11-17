# Wholesale Inventory & Fulfillment Analytics
### A Zaryn Data Engineering Portfolio Showcase

A runnable local Python starter for order-fulfillment analytics, with synthetic CSV data and automated tests. The broader Microsoft inventory and fulfillment architecture remains a design target. This is not a client deployment.

## Business Problem

Purchasing, sales, and warehouse teams need consistent definitions of outstanding demand, partial fulfillment, and on-time performance. This starter demonstrates those rules on a deliberately small, inspectable dataset.

## Run Locally

Use Python 3.10 or later. No third-party packages or cloud account are required. From the repository root:

```bash
python pipeline.py --as-of 2026-01-31
python -m unittest -v
```

The pipeline writes `output/fulfillment.csv`, replacing that file on rerun. Choose a dedicated output directory with `--target` if needed. Do not point this starter at customer data.

## Included Implementation

- `pipeline.py`: CSV ingestion, quantity and key validation, and order-line fulfillment calculations
- `data/sample/orders.csv`: four fictional order lines across two warehouses
- `data/sample/shipments.csv`: four fictional shipment lines
- `test_pipeline.py`: five standard-library unit tests

All sample records are fabricated for this project; they contain no customer data. Quantities are integer base units. Orders are a fixed snapshot, not a historical change log. Use the supplied cutoff for the documented expected results. Other cutoffs filter shipments and due dates but cannot reconstruct past cancellations or order creation.

## Expected Results for the Supplied Sample

At 2026-01-31, eligible due quantity is 25 units and on-time filled quantity is 21 units: quantity fill rate is 84%. One of two eligible due lines is complete on time: line completion rate is 50%. Sum numerators and denominators before calculating rates; do not average row-level percentages.

The example includes a partial on-time shipment, a late shipment, a partly cancelled order, a fully cancelled order, and a future shipment excluded by the cutoff.

## Local Validation

Five tests passed in the development sandbox before publication: expected metrics, duplicate shipment rejection, unknown order rejection, negative quantity rejection, and deterministic output on rerun. This is not evidence of SQL Server, Azure, Fabric, or Power BI deployment. The pipeline is an in-memory batch starter, not a production transactional publication system.

## Design Documents

- [Proposed Microsoft architecture](docs/architecture.md)
- [Broader metric definitions](docs/metric-definitions.md)

These documents describe the wider target. Inventory snapshots, receipts, unit conversions, returns, cloud orchestration, alerting, and Power BI reports are not implemented in this starter.

## Next Implementation Steps

- Add inventory snapshots and purchasing datasets
- Add SQL Server schemas and source-to-target integration
- Implement and validate the selected Azure/Fabric workflow
- Add Power BI reporting and documented operating procedures
- Expand tests for historical changes, returns, and publication failures

## Discuss a Similar Project

Zaryn Data Engineering | Manufacturing & Wholesale Distribution

Email: [admin@zaryndata.onmicrosoft.com](mailto:admin@zaryndata.onmicrosoft.com)

Do not send credentials or confidential datasets in an initial inquiry.
