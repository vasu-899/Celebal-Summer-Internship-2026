# Celebal Technologies Summer Internship 2026
## Week 7: Delta Lake - Incremental Data Processing

## Objective
Perform incremental data processing using Delta Lake with MERGE operation to handle upserts efficiently.

## Dataset
- **Source:** Superstore Sales Dataset (Kaggle)
- **customer_master.csv:** 793 unique customers extracted from Superstore
- **customer_incremental.csv:** 6 records (3 updates + 3 new customers)

## Project Structure
delta-lake-assignment/
├── data/
│   ├── customer_master.csv
│   └── customer_incremental.csv
├── notebooks/
│   └── delta_scd_assignment.ipynb
├── screenshots/
│   ├── data_loading/
│   ├── data_cleaning/
│   ├── scd1/
│   ├── validation/
│   └── final_output/
├── report/
│   └── assignment_summary.pdf
└── README.md

## Steps Performed
1. Loaded Superstore dataset (9994 rows)
2. Extracted 793 unique customers → customer_master Delta table
3. Created incremental dataset (7 records, 1 duplicate removed)
4. Applied MERGE operation (SCD Type 1)
5. Validated results

## MERGE Results
| Metric | Value |
|--------|-------|
| Initial records | 793 |
| Records updated | 3 |
| Records inserted | 3 |
| Duplicates removed | 1 |
| Final total records | 796 |
| Status | SUCCESS  |

## Delta Lake Features Used
- ACID Transactions
- MERGE (Upsert) Operation
- Transaction History / Audit Log
- Schema Enforcement

## Key Insights
- Consumer segment leads with 410 customers (avg sales ₹2,848)
- Corporate segment: 238 customers (avg sales ₹2,988)
- MERGE is more efficient than DELETE + INSERT
- Delta Lake maintains full transaction history for rollback

## Tech Stack
- Apache Spark (Databricks Community Edition)
- Delta Lake
- PySpark
- Superstore Dataset (Kaggle)

## How to Run
1. Open `notebooks/delta_scd_assignment.ipynb` in Databricks
2. Upload `data/` CSV files to Databricks workspace
3. Run all cells sequentially