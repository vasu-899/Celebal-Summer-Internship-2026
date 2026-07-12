# Architecture Documentation
## FMCG Data Consolidation & Analytics Platform

---

## 1. Overview
This platform implements Medallion Architecture (Bronze → Silver → Gold) on Databricks to consolidate data from two FMCG companies post-acquisition.

---

## 2. Layer Details

### Bronze Layer
- **Purpose:** Raw data ingestion and storage
- **Tables:** `bronze_fmcg.company_a_raw`, `bronze_fmcg.company_b_raw`
- **Format:** Delta Lake
- **Operations:** Ingest, add metadata (source_company, ingestion_timestamp, batch_id)

### Silver Layer
- **Purpose:** Data cleaning and standardization
- **Table:** `silver_fmcg.unified_sales`
- **Format:** Delta Lake
- **Operations:**
  - Null handling
  - Duplicate removal
  - Schema standardization
  - Category normalization
  - Company data merging

### Gold Layer
- **Purpose:** Business-ready data for analytics
- **Tables:** fact_sales, dim_customer, dim_product, dim_region, dim_time
- **Format:** Delta Lake
- **Operations:** Star schema creation, KPI calculation

---

## 3. Star Schema Design
          dim_time
             │
dim_region ── fact_sales ── dim_customer
│
dim_product

### Fact Table: fact_sales
| Column | Type | Description |
|--------|------|-------------|
| order_id | String | Unique order identifier |
| order_date | Date | Order date |
| customer_id | String | FK to dim_customer |
| product_name | String | FK to dim_product |
| region | String | FK to dim_region |
| sales_amount | Double | Total sales value |
| quantity | Double | Units sold |
| discount | Double | Discount applied |
| profit | Double | Net profit |
| profit_margin | Double | Profit % |
| source_company | String | Company A or B |

### Dimension Tables
| Table | Key | Description |
|-------|-----|-------------|
| dim_customer | customer_id | Customer details |
| dim_product | product_name | Product details |
| dim_region | region + city | Geographic details |
| dim_time | order_date | Time attributes |

---

## 4. Data Flow
CSV Files → spark.read.csv() → Bronze Delta Tables
Bronze → clean() + standardize() → Silver Delta Table
Silver → groupBy() + agg() → Gold Delta Tables
Gold → Databricks SQL → BI Dashboards

---

## 5. Technology Decisions
| Decision | Reason |
|----------|--------|
| Delta Lake | ACID transactions, schema enforcement |
| Medallion Architecture | Separation of raw/clean/business data |
| Star Schema | Optimized for analytical queries |
| PySpark | Distributed processing for large datasets |