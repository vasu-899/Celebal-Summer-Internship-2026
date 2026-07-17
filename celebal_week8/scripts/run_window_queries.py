# Window Functions & CTEs Queries

import sqlite3
import pandas as pd

DB_PATH = "output/ecommerce.db"

def run_query(conn, title, query):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))
    return df

def main():
    conn = sqlite3.connect(DB_PATH)

    # Query 7: Running Total by Region
    run_query(conn, "Q7: Running Total of Revenue per Region", """
        WITH daily_revenue AS (
            SELECT
                o.region_code,
                DATE(o.order_date) AS order_date,
                ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)), 2) AS daily_revenue
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE oi.is_return = 0 AND o.status != 'CANCELLED'
            GROUP BY o.region_code, DATE(o.order_date)
        )
        SELECT
            region_code,
            order_date,
            daily_revenue,
            ROUND(SUM(daily_revenue) OVER (
                PARTITION BY region_code
                ORDER BY order_date
            ), 2) AS running_total
        FROM daily_revenue
        ORDER BY region_code, order_date
        LIMIT 20
    """)

    # Query 8: DENSE_RANK Products by Revenue per Category
    run_query(conn, "Q8: Product Ranking by Revenue (DENSE_RANK)", """
        WITH product_revenue AS (
            SELECT
                p.category,
                p.product_name,
                ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)), 2) AS total_revenue
            FROM products p
            JOIN order_items oi ON p.product_id = oi.product_id
            WHERE oi.is_return = 0
            GROUP BY p.category, p.product_name
        )
        SELECT
            category,
            product_name,
            total_revenue,
            DENSE_RANK() OVER (
                PARTITION BY category
                ORDER BY total_revenue DESC
            ) AS rank_in_category
        FROM product_revenue
        ORDER BY category, rank_in_category
        LIMIT 20
    """)

    # Query 9: LAG Analysis - Days between orders
    run_query(conn, "Q9: Days Between Consecutive Orders (LAG)", """
        WITH customer_orders AS (
            SELECT
                customer_id,
                DATE(order_date) AS order_date,
                LAG(DATE(order_date)) OVER (
                    PARTITION BY customer_id
                    ORDER BY order_date
                ) AS previous_order_date
            FROM orders
            WHERE status != 'CANCELLED'
        )
        SELECT
            customer_id,
            order_date,
            previous_order_date,
            CASE
                WHEN previous_order_date IS NULL THEN NULL
                ELSE CAST(julianday(order_date) - julianday(previous_order_date) AS INTEGER)
            END AS days_gap,
            CASE
                WHEN AVG(
                    CASE WHEN previous_order_date IS NOT NULL
                    THEN CAST(julianday(order_date) - julianday(previous_order_date) AS INTEGER)
                    END
                ) OVER (PARTITION BY customer_id) > 30
                THEN 'At Risk'
                ELSE 'Active'
            END AS customer_status
        FROM customer_orders
        ORDER BY customer_id, order_date
        LIMIT 20
    """)

    # Query 10: CTE Multi-level - Customer Revenue Categories
    run_query(conn, "Q10: Customer Revenue Categories per Month", """
        WITH monthly_customer_revenue AS (
            SELECT
                c.customer_id,
                strftime('%Y-%m', o.order_date) AS month,
                ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)), 2) AS monthly_revenue
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE oi.is_return = 0
            GROUP BY c.customer_id, month
        ),
        categorized AS (
            SELECT
                month,
                customer_id,
                monthly_revenue,
                CASE
                    WHEN monthly_revenue > 10000 THEN 'High'
                    WHEN monthly_revenue >= 5000 THEN 'Medium'
                    ELSE 'Low'
                END AS revenue_category
            FROM monthly_customer_revenue
        )
        SELECT
            month,
            revenue_category,
            COUNT(customer_id) AS customer_count
        FROM categorized
        GROUP BY month, revenue_category
        ORDER BY month, revenue_category
        LIMIT 20
    """)

    # Query 11: NTILE Customer Segmentation
    run_query(conn, "Q11: Customer Quartile Segmentation (NTILE)", """
        WITH customer_value AS (
            SELECT
                c.customer_id,
                ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)), 2) AS total_value
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE oi.is_return = 0
            GROUP BY c.customer_id
        )
        SELECT
            customer_id,
            total_value,
            NTILE(4) OVER (ORDER BY total_value DESC) AS quartile,
            CASE NTILE(4) OVER (ORDER BY total_value DESC)
                WHEN 1 THEN 'Platinum'
                WHEN 2 THEN 'Gold'
                WHEN 3 THEN 'Silver'
                WHEN 4 THEN 'Bronze'
            END AS quartile_label
        FROM customer_value
        ORDER BY total_value DESC
        LIMIT 20
    """)

    # Query 12: Year-over-Year Comparison
    run_query(conn, "Q12: Year-over-Year Revenue Comparison", """
        WITH monthly_revenue AS (
            SELECT
                strftime('%Y', o.order_date) AS year,
                strftime('%m', o.order_date) AS month,
                ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)), 2) AS revenue
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE oi.is_return = 0
            GROUP BY year, month
        )
        SELECT
            curr.year,
            curr.month,
            curr.revenue,
            prev.revenue AS prev_year_revenue,
            CASE
                WHEN prev.revenue IS NULL THEN 'N/A'
                ELSE ROUND(100.0 * (curr.revenue - prev.revenue) / prev.revenue, 2) || '%'
            END AS yoy_growth_percent
        FROM monthly_revenue curr
        LEFT JOIN monthly_revenue prev
            ON curr.month = prev.month
            AND CAST(curr.year AS INTEGER) = CAST(prev.year AS INTEGER) + 1
        ORDER BY curr.year, curr.month
        LIMIT 20
    """)

    conn.close()
    print("\n Window Function queries complete!")

if __name__ == "__main__":
    main()