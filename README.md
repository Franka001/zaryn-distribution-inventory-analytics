# Wholesale Inventory & Fulfillment Analytics
### A Zaryn Data Engineering Portfolio Showcase

A planned Microsoft-based demonstration for connecting inventory, purchasing, sales orders, and shipment data across a wholesale distribution business.

> Status: Design-stage portfolio demonstration. This repository currently contains a project brief, proposed architecture, and metric definitions. Executable pipelines, datasets, reports, and validation results are not yet included. This is not a client deployment.

## Business Problem

Purchasing, sales, and warehouse teams need a consistent view of stock, outstanding demand, supplier receipts, and fulfillment exceptions without repeatedly combining spreadsheets.

## Intended Users

- Purchasing managers reviewing supply and inventory exposure
- Warehouse managers reviewing stock and fulfillment exceptions
- Sales operations teams reviewing open orders and backorders

## Proposed First Release

- Synthetic products, warehouses, inventory snapshots, order lines, receipts, and shipment lines
- Documented source-to-target transformations
- Inventory and order fulfillment analytical models
- Data-quality and reconciliation checks
- Power BI report with warehouse and product filters
- One exception notification workflow; no automatic purchasing actions

## Proposed Microsoft Architecture

Synthetic SQL Server tables and CSV extracts → Azure Data Factory → Azure Data Lake Storage → SQL/Python transformations → SQL Server analytical tables → Power BI

Power Automate is a proposed option for exception notifications. This is a batch analytics design, not a real-time inventory reservation system.

## Business Questions

1. What stock is on hand by product and warehouse?
2. Which orders have outstanding quantities?
3. Which due order lines were fulfilled by their promised date?
4. Which products have low recent shipment activity?

## Documentation

- [Architecture and implementation plan](docs/architecture.md)
- [Metric definitions](docs/metric-definitions.md)

## Implementation Roadmap

- [x] Define project scope and metric rules
- [ ] Generate reproducible synthetic source data
- [ ] Implement SQL Server source and target schemas
- [ ] Implement ingestion and incremental processing
- [ ] Add automated quality and reconciliation tests
- [ ] Build the Power BI model and report
- [ ] Document deployment, operating costs, and recovery
- [ ] Publish measured test results and screenshots

## Validation Plan

Test partial shipments, cancellations, returns, duplicate records, late-arriving shipments, missing product references, and unit-of-measure conversions. Reconcile source quantities to curated quantities and demonstrate a safe rerun without duplicate outputs. No validation results are claimed yet.

## Run Status

There is no executable end-to-end demo in this version. Azure resources and Power BI artifacts have not been deployed or validated through this repository.

## Discuss a Similar Project

Zaryn Data Engineering provides Microsoft-focused data engineering services for manufacturing and wholesale distribution.

Email: [admin@zaryndata.onmicrosoft.com](mailto:admin@zaryndata.onmicrosoft.com)

Please share only a high-level business challenge initially; do not send credentials or confidential datasets.
