# Data Dictionary
## FMCG Data Consolidation & Analytics Platform

---

## Bronze Layer

### bronze_fmcg.company_a_raw
| Column | Type | Description |
|--------|------|-------------|
| row_id | Integer | Row identifier |
| order_id | String | Unique order ID |
| order_date | Date | Order placed date |
| ship_date | Date | Shipment date |
| ship_mode | String | Shipping method |
| customer_id | String | Customer identifier |
| customer_name | String | Customer full name |
| Segment | String | Customer segment |
| Country | String | Country name |
| City | String | City name |
| State | String | State name |
| postal_code | Integer | Postal code |
| Region | String | Geographic region |
| product_id | String | Product identifier |
| Category | String | Product category |
| sub_category | String | Product sub-category |
| product_name | String | Product name |
| Sales | Double | Sales amount |
| Quantity | Double | Units sold |
| Discount | Double | Discount rate |
| Profit | Double | Net profit |
| source_company | String | Source: Company_A |
| source_system | String | Superstore_ERP |
| ingestion_timestamp | Timestamp | When data was ingested |
| batch_id | String | Batch identifier |

### bronze_fmcg.company_b_raw
| Column | Type | Description |
|--------|------|-------------|
| order_ref | String | Order reference |
| order_date | String | Order date |
| cust_code | String | Customer code |
| cust_name | String | Customer name |
| business_type | String | Business type |
| zone | String | Geographic zone |
| city | String | City name |
| product_category | String | Product category |
| product_name | String | Product name |
| revenue | Double | Revenue amount |
| units_sold | Integer | Units sold |
| discount_rate | Double | Discount rate |
| net_profit | Double | Net profit |
| source_company | String | Source: Company_B |
| source_system | String | Legacy_FMCG_System |

---

## Silver Layer

### silver_fmcg.unified_sales
| Column | Type | Description |
|--------|------|-------------|
| order_id | String | Unified order ID |
| order_date | Date | Order date |
| ship_date | Date | Ship date |
| customer_id | String | Unified customer ID |
| customer_name | String | Customer name |
| Segment | String | Standardized segment (UPPER) |
| Region | String | Standardized region (UPPER) |
| city | String | City name |
| Country | String | Country name |
| Category | String | Unified category |
| sub_category | String | Sub-category |
| product_name | String | Product name |
| Sales | Double | Sales amount |
| Quantity | Double | Quantity sold |
| Discount | Double | Discount rate |
| Profit | Double | Net profit |
| source_company | String | Company_A or Company_B |

---

## Gold Layer

### gold_fmcg.fact_sales
| Column | Type | Description |
|--------|------|-------------|
| order_id | String | Order identifier |
| order_date | Date | Order date |
| customer_id | String | FK → dim_customer |
| product_name | String | FK → dim_product |
| region | String | FK → dim_region |
| city | String | City name |
| sales_amount | Double | Total sales |
| quantity | Double | Units sold |
| discount | Double | Discount applied |
| profit | Double | Net profit |
| profit_margin | Double | Profit percentage |
| source_company | String | Source company |

### gold_fmcg.dim_customer
| Column | Type | Description |
|--------|------|-------------|
| customer_id | String | PK - Customer ID |
| customer_name | String | Full name |
| segment | String | CONSUMER/CORPORATE/HOME OFFICE |
| country | String | Country |

### gold_fmcg.dim_product
| Column | Type | Description |
|--------|------|-------------|
| product_name | String | PK - Product name |
| category | String | Product category |
| sub_category | String | Sub-category |

### gold_fmcg.dim_region
| Column | Type | Description |
|--------|------|-------------|
| region | String | PK - Region name |
| city | String | City name |
| country | String | Country |

### gold_fmcg.dim_time
| Column | Type | Description |
|--------|------|-------------|
| order_date | Date | PK - Date |
| year | Integer | Year |
| month | Integer | Month (1-12) |
| quarter | Integer | Quarter (1-4) |
| day_of_week | Integer | Day (1=Sunday) |

---

## KPI Tables

### gold_fmcg.kpi_sales_by_region
| Column | Description |
|--------|-------------|
| region | Geographic region |
| total_sales | Sum of sales |
| total_profit | Sum of profit |
| total_orders | Count of orders |
| avg_profit_margin | Average profit % |

### gold_fmcg.kpi_product_performance
| Column | Description |
|--------|-------------|
| product_name | Product name |
| total_sales | Total revenue |
| total_profit | Total profit |
| total_orders | Number of orders |

### gold_fmcg.kpi_customer_lifetime_value
| Column | Description |
|--------|-------------|
| customer_id | Customer ID |
| lifetime_value | Total spend |
| total_profit | Total profit |
| total_orders | Number of orders |

### gold_fmcg.kpi_company_comparison
| Column | Description |
|--------|-------------|
| source_company | Company A or B |
| total_sales | Total revenue |
| total_profit | Total profit |
| total_orders | Number of orders |