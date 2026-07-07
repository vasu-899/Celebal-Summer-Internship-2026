
# Celebal Technologies Summer Internship 2026
## Week 5 - Apache Spark Fundamentals

## Objective
Understand Spark fundamentals and perform data cleaning, transformation, and aggregation using PySpark DataFrames on the Superstore dataset.

## Project Structure
spark-assignment/

├── data/

│   └── dataset.csv          # Superstore sales dataset (9994 rows)

├── notebook/

│   └── spark_basics.ipynb   # Complete PySpark implementation

├── output/

│   └── results.csv          # Final pipeline output (revenue by region)

└── README.md

## What This Project Covers

### Core Concepts
- Spark vs MapReduce — in-memory computing advantages
- DataFrame immutability and its impact on data cleaning
- Data cleaning: duplicate removal, null handling
- Filtering, aggregation (count, sum, avg, min, max)
- GroupBy operations with conditional filtering
- Wide transformations and shuffle operations
- Schema modification (casting, renaming)
- End-to-end data processing pipeline

### Theory + Code Questions (Q1-Q15)
The notebook includes 15 questions covering Spark fundamentals, each with:
- Detailed explanation
- Working PySpark code demonstration

## Key Insights
- **Technology** category has the highest average sale value (₹452.7) despite fewer orders than Office Supplies
- **West region** leads in both total sales and profit
- Real-world data quality issue encountered: malformed CSV rows with embedded commas, resolved using `regexp_extract()` for safe numeric parsing
- 13 cities have more than 100 orders, led by New York City (915 orders)

## Tech Stack
- PySpark (Apache Spark Python API)
- Google Colab (execution environment)
- Pandas (for output export)

## How to Run
1. Open `notebook/spark_basics.ipynb` in Google Colab or Jupyter
2. Upload `data/dataset.csv` to the working directory
3. Run all cells sequentially
4. Final output saved to `output/results.csv`