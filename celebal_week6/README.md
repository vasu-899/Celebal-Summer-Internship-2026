# Celebal Technologies Summer Internship 2026
## Week 6 - Spark Architecture and Optimized Data Processing

## Objective
Understand Spark architecture and perform efficient data processing using transformations, filtering, schema handling, and optimized file formats.

## Project Structure
spark-assignment-week6/

├── data/

│   └── dataset.csv          # Superstore sales dataset (9994 rows)

├── notebook/

│   └── spark_week6.ipynb    # Complete PySpark implementation

├── output/

│   └── results.csv          # Final pipeline output

└── README.md

## Topics Covered
- Spark Architecture (Driver, Cluster Manager, Executors)
- Lazy Evaluation and DAG (Lineage Graph)
- CSV vs Parquet file formats
- Predicate Pushdown optimization
- Transformations vs Actions
- Client Mode vs Cluster Mode
- Data pipeline (Read → Transform → Filter → Write)
- Best practices for large datasets

## Theory + Code Questions (Q1-Q15)
All 15 questions covered with detailed explanations and working PySpark code.

## Key Results
- Pipeline processed 9994 rows → 374 rows after filtering
- Output saved in both CSV and Parquet formats
- Performance comparison: CSV vs Parquet demonstrated

## Tech Stack
- PySpark (Apache Spark Python API)
- Google Colab (execution environment)

## How to Run
1. Open `notebook/spark_week6.ipynb` in Google Colab
2. Upload `data/dataset.csv` to working directory
3. Run all cells sequentially
