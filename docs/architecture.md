# Proposed Architecture

## Status

Design only. No cloud deployment or executable pipeline is included in this version. Product selection and deployment details must be validated during implementation.

## Data Flow

1. Generate synthetic SQL Server tables and CSV extracts for products, warehouses, order lines, inventory snapshots, receipts, and shipments.
2. Use Azure Data Factory to orchestrate batch ingestion into Azure Data Lake Storage.
3. Preserve source-aligned landing data with batch identifiers and ingestion timestamps.
4. Transform data using SQL and Python, with explicit business keys and unit conversions.
5. Publish curated SQL Server analytical tables for Power BI.
6. Optionally use Power Automate for reviewed exception notifications.

## Proposed Analytical Grain

- Inventory snapshot: one product, warehouse, and snapshot timestamp.
- Sales order line: one source system, order, and line identifier.
- Shipment line: one source system, shipment, and shipment line identifier, linked to an order line.
- Receipt line: one source system, receipt, and receipt line identifier, linked to a purchase order line where available.

## Incremental Processing Design

Use a source modification timestamp plus a stable key where supported. Advance the successful watermark only after validation and publication. A timestamp alone does not capture deleted rows; deletion and cancellation handling require explicit source rules. Use replayable batches and idempotent target writes.

## Reliability Requirements

Record batch ID, source, start/end time, row counts, status, and error details. Quarantine invalid records with reasons. Reconcile counts and quantities before publishing. Test late-arriving updates and duplicate delivery. Preserve the previous valid published dataset when a new batch fails acceptance checks.

## Security and Deployment Requirements

Keep credentials and customer data out of Git. Prefer managed identities where supported; document any required alternative and store secrets in an appropriate secret store. Define least-privilege access and environment-specific configuration. Cost estimates require a chosen region, resource sizing, workload, and licensing assumptions.

## Not in First Release

Real-time inventory reservations, automated purchasing, production ERP connectors, and production availability commitments.
