# ================================================
# Cohort & Retention Analysis
# ================================================
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

    # Query 13: First/Last Category Analysis
    run_query(conn, "Q13: First vs Last Purchased Category", """
        WITH customer_categories AS (
            SELECT
                o.customer_id,
                p.category,
                MIN(o.order_date) AS first_order_date,
                MAX(o.order_date) AS last_order_date
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.status != 'CANCELLED'
            GROUP BY o.customer_id, p.category
        ),
        first_category AS (
            SELECT customer_id, category AS first_category
            FROM customer_categories
            WHERE first_order_date = (
                SELECT MIN(first_order_date)
                FROM customer_categories cc2
                WHERE cc2.customer_id = customer_categories.customer_id
            )
        ),
        last_category AS (
            SELECT customer_id, category AS last_category
            FROM customer_categories
            WHERE last_order_date = (
                SELECT MAX(last_order_date)
                FROM customer_categories cc2
                WHERE cc2.customer_id = customer_categories.customer_id
            )
        )
        SELECT
            f.customer_id,
            f.first_category,
            l.last_category,
            CASE WHEN f.first_category != l.last_category
                THEN 'Yes' ELSE 'No'
            END AS category_shift
        FROM first_category f
        JOIN last_category l ON f.customer_id = l.customer_id
        LIMIT 15
    """)

    # Query 14: Cumulative Revenue Distribution
    run_query(conn, "Q14: Cumulative Revenue Distribution", """
        WITH customer_revenue AS (
            SELECT
                c.customer_id,
                ROUND(SUM(oi.quantity * oi.unit_price *
                    (1 - oi.discount_percent/100.0)), 2) AS revenue
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE oi.is_return = 0
            GROUP BY c.customer_id
        ),
        total AS (
            SELECT SUM(revenue) AS total_revenue FROM customer_revenue
        )
        SELECT
            cr.customer_id,
            cr.revenue,
            ROUND(SUM(cr.revenue) OVER (
                ORDER BY cr.revenue DESC
            ), 2) AS cumulative_revenue,
            ROUND(100.0 * SUM(cr.revenue) OVER (
                ORDER BY cr.revenue DESC
            ) / t.total_revenue, 2) AS cumulative_percent
        FROM customer_revenue cr, total t
        ORDER BY cr.revenue DESC
        LIMIT 15
    """)

    # Query 15: Cohort Analysis
    run_query(conn, "Q15: Cohort Retention Analysis", """
        WITH cohorts AS (
            SELECT
                customer_id,
                strftime('%Y-%m', MIN(order_date)) AS cohort_month
            FROM orders
            WHERE status != 'CANCELLED'
            GROUP BY customer_id
        ),
        cohort_orders AS (
            SELECT
                c.cohort_month,
                strftime('%Y-%m', o.order_date) AS order_month,
                COUNT(DISTINCT o.customer_id) AS active_customers
            FROM cohorts c
            JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.status != 'CANCELLED'
            GROUP BY c.cohort_month, order_month
        ),
        cohort_size AS (
            SELECT cohort_month, COUNT(DISTINCT customer_id) AS total_customers
            FROM cohorts
            GROUP BY cohort_month
        )
        SELECT
            co.cohort_month,
            cs.total_customers,
            co.order_month,
            co.active_customers,
            ROUND(100.0 * co.active_customers / cs.total_customers, 2) AS retention_rate
        FROM cohort_orders co
        JOIN cohort_size cs ON co.cohort_month = cs.cohort_month
        ORDER BY co.cohort_month, co.order_month
        LIMIT 20
    """)

    # Query 16: Products Bought Together
    run_query(conn, "Q16: Products Frequently Bought Together", """
        SELECT
            p1.product_name AS product_a,
            p2.product_name AS product_b,
            COUNT(*) AS times_bought_together
        FROM order_items oi1
        JOIN order_items oi2 ON oi1.order_id = oi2.order_id
            AND oi1.product_id < oi2.product_id
        JOIN products p1 ON oi1.product_id = p1.product_id
        JOIN products p2 ON oi2.product_id = p2.product_id
        GROUP BY p1.product_name, p2.product_name
        ORDER BY times_bought_together DESC
        LIMIT 10
    """)

    conn.close()
    print("\n Cohort Analysis complete!")

if __name__ == "__main__":
    main()