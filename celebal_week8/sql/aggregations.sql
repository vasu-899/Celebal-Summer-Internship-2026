-- E-Commerce Order Analytics System
-- SQL Analytics: Joins & Aggregations


-- Query 1: Total Revenue per Category
-- Revenue = quantity × unit_price × (1 - discount_percent/100)
SELECT
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)), 2) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity) AS total_units_sold
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE oi.is_return = 0
  AND o.status != 'CANCELLED'
GROUP BY p.category
ORDER BY total_revenue DESC;

-- ------------------------------------------------
-- Query 2: Top 10 Customers by Total Order Value
-- ------------------------------------------------
SELECT
    c.customer_id,
    c.customer_name,
    c.customer_type,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)), 2) AS total_order_value,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE oi.is_return = 0
  AND o.status != 'CANCELLED'
GROUP BY c.customer_id, c.customer_name, c.customer_type
ORDER BY total_order_value DESC
LIMIT 10;

-- ------------------------------------------------
-- Query 3: Month-wise Order Count (Last 12 Months)
-- ------------------------------------------------
SELECT
    strftime('%Y-%m', order_date) AS year_month,
    COUNT(order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM orders
WHERE order_date >= date('now', '-12 months')
  AND status != 'CANCELLED'
GROUP BY year_month
ORDER BY year_month;

-- ------------------------------------------------
-- Query 4: Customers who placed orders but never had items DELIVERED
-- ------------------------------------------------
SELECT DISTINCT
    c.customer_id,
    c.customer_name,
    c.customer_type,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_id NOT IN (
    SELECT DISTINCT customer_id
    FROM orders
    WHERE status = 'DELIVERED'
)
GROUP BY c.customer_id, c.customer_name, c.customer_type
ORDER BY total_orders DESC;

-- ------------------------------------------------
-- Query 5: Products with more returns than purchases
-- ------------------------------------------------
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(CASE WHEN oi.is_return = 0 THEN oi.quantity ELSE 0 END) AS total_purchased,
    SUM(CASE WHEN oi.is_return = 1 THEN ABS(oi.quantity) ELSE 0 END) AS total_returned
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, p.category
HAVING total_returned > total_purchased
ORDER BY total_returned DESC;

-- ------------------------------------------------
-- Query 6: Return Rate per Category
-- ------------------------------------------------
SELECT
    p.category,
    SUM(CASE WHEN oi.is_return = 0 THEN oi.quantity ELSE 0 END) AS total_purchased,
    SUM(CASE WHEN oi.is_return = 1 THEN ABS(oi.quantity) ELSE 0 END) AS total_returned,
    ROUND(
        100.0 * SUM(CASE WHEN oi.is_return = 1 THEN ABS(oi.quantity) ELSE 0 END) /
        NULLIF(SUM(CASE WHEN oi.is_return = 0 THEN oi.quantity ELSE 0 END), 0),
    2) AS return_rate_percent
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY return_rate_percent DESC;