# Celebal Technologies Summer Internship 2026
## FMCG Data Consolidation & Analytics Platform
### Medallion Architecture: Bronze → Silver → Gold

---

## Business Problem
Post-acquisition of a smaller FMCG company, the organization faced:
- Data silos across multiple systems (Company A & Company B)
- Inconsistent product, customer, and sales data
- Lack of unified reporting and analytics
- Delayed business decision-making

---

## Solution Architecture
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                              │
│  Company A (Superstore ERP)  +  Company B (Legacy FMCG)    │
└──────────────────┬──────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│               BRONZE LAYER (Raw Ingestion)                   │
│         Delta Tables: company_a_raw, company_b_raw          │
└──────────────────┬──────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│           SILVER LAYER (Cleaned & Standardized)              │
│              Delta Table: unified_sales                      │
└──────────────────┬──────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│              GOLD LAYER (Business Ready)                     │
│        Star Schema: fact_sales + 4 dimension tables          │
│              4 KPI Tables for Analytics                      │
└──────────────────┬──────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│                BI & ANALYTICS                                │
│         Databricks SQL + Power BI Dashboards                │
└─────────────────────────────────────────────────────────────┘

---

## Project Structure
fmcg-project/
├── notebooks/
│   ├── 01_bronze_ingestion.ipynb
│   ├── 02_silver_transformation.ipynb
│   ├── 03_gold_aggregation.ipynb
│   └── 04_pipeline_orchestration.ipynb
├── data/
│   ├── raw/
│   │   └── superstore.csv
│   └── incremental/
│       └── company_b_data.csv
├── screenshots/
│   ├── 01_bronze/
│   ├── 02_silver/
│   ├── 03_gold/
│   └── 04_pipeline/
├── docs/
│   ├── architecture.md
│   └── data_dictionary.md
├── README.md


---

## Notebooks
| Notebook | Description |
|----------|-------------|
| 01_bronze_ingestion | Raw data ingestion from Company A & B |
| 02_silver_transformation | Data cleaning, standardization & merging |
| 03_gold_aggregation | Star schema creation & KPI calculation |
| 04_pipeline_orchestration | End-to-end pipeline validation & reporting |

---

## Pipeline Results

### Bronze Layer
| Source | System | Records |
|--------|--------|---------|
| Company A | Superstore ERP | 9,994 |
| Company B | Legacy FMCG | 15 |
| **Total** | | **10,009** |

### Silver Layer
| Operation | Result |
|-----------|--------|
| Nulls handled | 301 values |
| Duplicates removed | 8 rows |
| Final records | 10,001 |

### Gold Layer
| Table | Type | Rows |
|-------|------|------|
| fact_sales | Fact | 10,001 |
| dim_customer | Dimension | 804 |
| dim_product | Dimension | 1,862 |
| dim_region | Dimension | 593 |
| dim_time | Dimension | 1,252 |

---

## Key Business KPIs
| KPI | Value |
|-----|-------|
| Top Region | WEST (₹7,13,369) |
| Top Product | Canon imageCLASS (₹61,599) |
| Top Customer | SM-20320 (₹25,043 CLV) |
| Company A Sales | ₹22,70,758 |
| Company B Sales | ₹39,400 |

---

## Technology Stack
| Component | Technology |
|-----------|-----------|
| Platform | Databricks Community Edition |
| Processing | Apache Spark 4.1.0 (PySpark) |
| Storage | Delta Lake |
| Architecture | Medallion (Bronze/Silver/Gold) |
| Data Model | Star Schema |
| Language | Python (PySpark) |

---

## How to Run
1. Open Databricks workspace
2. Upload `data/raw/superstore.csv`
3. Run notebooks in order: 01 → 02 → 03 → 04
4. Check Gold layer tables for KPIs

---

## Business Impact
- Unified view of enterprise data across 2 companies
- Faster reporting with pre-built KPI tables
- Improved decision-making via Star Schema
- Scalable architecture for future data sources
- Reduced data inconsistencies