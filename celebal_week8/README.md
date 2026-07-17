# E-Commerce Order Analytics System
---

## Objective
Design and develop an end-to-end e-commerce order analytics system combining Python and SQL — from dataset generation to business reporting.

---

## Project Structure

    ecommerce-analytics-system/
    │
    ├── data/
    │   ├── raw/                    # Generated raw CSV files
    │   │   ├── customers.csv
    │   │   ├── products.csv
    │   │   ├── orders.csv
    │   │   └── order_items.csv
    │   └── cleaned/                # Cleaned CSV files
    │       ├── customers_clean.csv
    │       ├── products_clean.csv
    │       ├── orders_clean.csv
    │       └── order_items_clean.csv
    │
    ├── scripts/
    │   ├── generate_data.py        # Data generation script
    │   ├── clean_data.py           # Data cleaning script
    │   ├── load_db.py              # Load data into SQLite
    │   ├── run_queries.py          # Run aggregation queries
    │   ├── run_window_queries.py   # Run window function queries
    │   ├── cohort_analysis.py      # Cohort & retention analysis
    │   ├── report_cli.py           # CLI reporting tool
    │   └── edge_cases.py           # Edge case test suite
    │
    ├── sql/
    │   ├── schema.sql              # Database schema
    │   ├── aggregations.sql        # Aggregation queries
    │   ├── window_functions.sql    # Window function queries
    │   └── cohort_analysis.sql     # Cohort analysis queries
    │
    ├── output/
    │   ├── ecommerce.db            # SQLite database
    │   ├── issues_report.json      # Data quality report
    │   └── sample_reports/         # Screenshots
    │
    └── README.md

---

## How to Run

### Step 1: Install Dependencies
```bash
pip install faker pandas tabulate
```

### Step 2: Generate Data
```bash
cd celebal_week8
python scripts/generate_data.py
```

### Step 3: Clean Data
```bash
python scripts/clean_data.py
```

### Step 4: Load into Database
```bash
python scripts/load_db.py
```

### Step 5: Run SQL Queries
```bash
python scripts/run_queries.py
python scripts/run_window_queries.py
python scripts/cohort_analysis.py
```

### Step 6: CLI Reporting Tool
```bash
python scripts/report_cli.py --report revenue --type monthly --start 2025-01-01 --end 2025-12-31
python scripts/report_cli.py --report top_customers --start 2025-01-01 --end 2025-12-31
python scripts/report_cli.py --report top_products --start 2025-01-01 --end 2025-12-31
python scripts/report_cli.py --report retention --start 2025-01-01 --end 2025-12-31
```

### Step 7: Run Edge Case Tests
```bash
python scripts/edge_cases.py
```

---

## Dataset Details

| File | Rows | Intentional Issues |
|------|------|--------------------|
| customers.csv | 500 | 2% invalid emails |
| products.csv | 100 | Extra spaces, mixed case |
| orders.csv | 600 | 5% NULL customer_id, 10% wrong dates |
| order_items.csv | 1510 | 3% negative qty, 1% discount > 100 |

---

## Data Cleaning Results

| Issue | Count | Action |
|-------|-------|--------|
| Wrong date formats | 46 | Fixed to YYYY-MM-DD |
| NULL customer_ids | 32 | Filled with UNKNOWN |
| Invalid emails | 6 | Flagged in report |
| Orphan order_items | 10 | Removed |
| Negative quantities | 49 | Flagged as returns |
| Invalid discounts | 15 | Capped at 100 |

---

## SQL Queries Implemented

### Aggregations (Q1-Q6)
- Total revenue per category
- Top 10 customers by order value
- Month-wise order count
- Customers with no delivered items
- Products with more returns than purchases
- Return rate per category

### Window Functions & CTEs (Q7-Q12)
- Running totals by region
- DENSE_RANK products by revenue
- LAG analysis for order gaps
- CTE multi-level customer categorization
- NTILE customer segmentation (Platinum/Gold/Silver/Bronze)
- Year-over-Year revenue comparison

### Cohort Analysis (Q13-Q16)
- First vs last purchased category
- Cumulative revenue distribution
- Cohort retention analysis
- Products frequently bought together

---

## CLI Tool Usage
python scripts/report_cli.py --report [TYPE] --start YYYY-MM-DD --end YYYY-MM-DD
Report Types:
revenue        Monthly/weekly/daily revenue with period comparison
top_customers  Top 5 customers by revenue
top_products   Top 5 products by revenue
retention      Cohort retention rates

---

## Edge Cases Handled

| Test | Result |
|------|--------|
| Orphan order_items |  PASSED |
| Discount > 100% |  PASSED |
| Zero quantity |  PASSED |
| Future dates |  PASSED |
| NULL order_ids | PASSED |
| Invalid emails |  PASSED |
| Negative prices |  PASSED |
| Empty result sets |  PASSED |
| Referential integrity | PASSED |
| Duplicate order_ids |  PASSED |

---

## Technology Stack
| Component | Technology |
|-----------|-----------|
| Language | Python 3.14 |
| Data Generation | Faker, Random |
| Data Processing | Pandas |
| Database | SQLite3 |
| Reporting | Argparse, Tabulate |

---

## Key Business Insights
- **Home** category leads with ₹97,68,849 revenue
- **Top Customer:** CUST0061 with ₹3,78,202 lifetime value
- **Best Product:** Cupiditate Bedding Iste (₹3,91,299)
- **Revenue Growth:** +125.22% YoY in 2025
- **Retention:** July 2024 cohort shows 30% retention after 6 months