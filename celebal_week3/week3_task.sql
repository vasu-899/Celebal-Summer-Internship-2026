-- ================================================
-- Week 3: Subqueries, CTEs, Window Functions
-- Dataset: Superstore Sales Data
-- ================================================

CREATE DATABASE IF NOT EXISTS superstore;
USE superstore;

-- ================================================
-- STEP 1: Create superstore_raw table
-- ================================================
CREATE TABLE IF NOT EXISTS superstore_raw (
    row_id          INT,
    order_id        VARCHAR(50),
    order_date      VARCHAR(20),
    ship_date       VARCHAR(20),
    ship_mode       VARCHAR(50),
    customer_id     VARCHAR(50),
    customer_name   VARCHAR(100),
    segment         VARCHAR(50),
    country         VARCHAR(50),
    city            VARCHAR(50),
    state           VARCHAR(50),
    postal_code     VARCHAR(20),
    region          VARCHAR(20),
    product_id      VARCHAR(50),
    category        VARCHAR(50),
    sub_category    VARCHAR(50),
    product_name    VARCHAR(255),
    sales           DECIMAL(10,2),
    quantity        INT,
    discount        DECIMAL(5,2),
    profit          DECIMAL(10,2)
);

-- ================================================
-- STEP 1B: Create customers, orders, products tables
-- ================================================

-- Customers table
USE superstore;
CREATE TABLE IF NOT EXISTS customers AS
SELECT DISTINCT 
    customer_id,
    customer_name,
    segment,
    country,
    city,
    state,
    region
FROM superstore_raw;

-- Products table
CREATE TABLE IF NOT EXISTS products AS
SELECT DISTINCT
    product_id,
    product_name,
    category,git,
    sub_category
FROM superstore_raw;

-- Orders table
CREATE TABLE IF NOT EXISTS orders AS
SELECT DISTINCT
    order_id,
    order_date,
    ship_date,
    ship_mode,
    customer_id,
    product_id,
    sales,
    quantity,
    discount,
    profit
FROM superstore_raw;

USE superstore;

-- ================================================
-- STEP 2: Required Queries
-- ================================================

-- Query 1: Orders where sales > average sales (Subquery)
-- Business use: Identify high-value orders above market average
SELECT 
    order_id,
    customer_name,
    sales
FROM superstore_raw
WHERE sales > (SELECT AVG(sales) FROM superstore_raw)
ORDER BY sales DESC;

-- Query 2: Highest sales order per customer (Subquery)
-- Business use: Find each customer's best performing order
SELECT 
    customer_name,
    order_id,
    sales
FROM superstore_raw s1
WHERE sales = (
    SELECT MAX(sales) 
    FROM superstore_raw s2 
    WHERE s1.customer_id = s2.customer_id
)
ORDER BY sales DESC;

-- Query 3: Total sales per customer (CTE)
-- Business use: Understand overall customer contribution
WITH customer_sales AS (
    SELECT 
        customer_id,
        customer_name,
        ROUND(SUM(sales), 2) AS total_sales
    FROM superstore_raw
    GROUP BY customer_id, customer_name
)
SELECT * FROM customer_sales
ORDER BY total_sales DESC;

-- Query 4: Customers with above average total sales (CTE + Subquery)
-- Business use: Identify premium/high-value customers
WITH customer_sales AS (
    SELECT 
        customer_id,
        customer_name,
        ROUND(SUM(sales), 2) AS total_sales
    FROM superstore_raw
    GROUP BY customer_id, customer_name
)
SELECT * FROM customer_sales
WHERE total_sales > (SELECT AVG(total_sales) FROM customer_sales)
ORDER BY total_sales DESC;

-- Query 5: Rank customers by total sales (Window Function)
-- Business use: Customer performance ranking
WITH customer_sales AS (
    SELECT 
        customer_name,
        ROUND(SUM(sales), 2) AS total_sales
    FROM superstore_raw
    GROUP BY customer_id, customer_name
)
SELECT 
    customer_name,
    total_sales,
    RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM customer_sales;

-- Query 6: Row numbers per customer orders (Window Function + PARTITION BY)
-- Business use: Track order sequence per customer
SELECT 
    customer_name,
    order_id,
    order_date,
    sales,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS order_number
FROM superstore_raw;

-- Query 7: Top 3 customers by total sales (Window Function)
-- Business use: Identify top performing customers
WITH customer_sales AS (
    SELECT 
        customer_name,
        ROUND(SUM(sales), 2) AS total_sales,
        RANK() OVER (ORDER BY SUM(sales) DESC) AS sales_rank
    FROM superstore_raw
    GROUP BY customer_id, customer_name
)
SELECT * FROM customer_sales
WHERE sales_rank <= 3;

-- ================================================
-- STEP 3: Final Combined Query
-- Customer Name + Total Sales + Rank
-- (JOIN + CTE + Window Function)
-- ================================================
WITH customer_sales AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        ROUND(SUM(o.sales), 2) AS total_sales
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT 
    customer_name,
    total_sales,
    RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM customer_sales
ORDER BY sales_rank;

-- ================================================
-- MINI PROJECT: Customer Sales Insights
-- ================================================

-- 1. Top 5 customers
WITH customer_sales AS (
    SELECT 
        customer_name,
        ROUND(SUM(sales), 2) AS total_sales
    FROM superstore_raw
    GROUP BY customer_id, customer_name
)
SELECT 
    customer_name,
    total_sales,
    RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM customer_sales
ORDER BY total_sales DESC
LIMIT 5;

-- 2. Bottom 5 customers
WITH customer_sales AS (
    SELECT 
        customer_name,
        ROUND(SUM(sales), 2) AS total_sales
    FROM superstore_raw
    GROUP BY customer_id, customer_name
)
SELECT 
    customer_name,
    total_sales,
    RANK() OVER (ORDER BY total_sales ASC) AS sales_rank
FROM customer_sales
ORDER BY total_sales ASC
LIMIT 5;

-- 3. Customers with only one order
SELECT 
    customer_name,
    COUNT(DISTINCT order_id) AS order_count
FROM superstore_raw
GROUP BY customer_id, customer_name
HAVING COUNT(DISTINCT order_id) = 1;

-- 4. Customers with above average sales
WITH customer_sales AS (
    SELECT 
        customer_name,
        ROUND(SUM(sales), 2) AS total_sales
    FROM superstore_raw
    GROUP BY customer_id, customer_name
)
SELECT 
    customer_name,
    total_sales
FROM customer_sales
WHERE total_sales > (SELECT AVG(total_sales) FROM customer_sales)
ORDER BY total_sales DESC

-- 5. Highest order value per customer
SELECT 
    customer_name,
    order_id,
    ROUND(MAX(sales), 2) AS highest_order_value
FROM superstore_raw
GROUP BY customer_id, customer_name, order_id
ORDER BY highest_order_value DESC;





