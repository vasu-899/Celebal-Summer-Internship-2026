# Run SQL Queries and Show Results

import sqlite3
import pandas as pd

DB_PATH = "output/ecommerce.db"

def run_query(conn, title, query):
    """Run a SQL query and display results"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))
    return df

def main():
    conn = sqlite3.connect(DB_PATH)

    # Query 1: Revenue per category
    run_query(conn, "Q1: Total Revenue per Category", """
        SELECT p.category,
            ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)), 2) AS total_revenue,
            COUNT(DISTINCT o.order_id) AS total_orders
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.is_return = 0 AND o.status != 'CANCELLED'
        GROUP BY p.category ORDER BY total_revenue DESC
    """)

    # Query 2: Top 10 customers
    run_query(conn, "Q2: Top 10 Customers by Order Value", """
        SELECT c.customer_id, c.customer_name, c.customer_type,
            ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)), 2) AS total_value,
            COUNT(DISTINCT o.order_id) AS total_orders
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE oi.is_return = 0 AND o.status != 'CANCELLED'
        GROUP BY c.customer_id ORDER BY total_value DESC LIMIT 10
    """)

    # Query 3: Monthly orders
    run_query(conn, "Q3: Month-wise Order Count", """
        SELECT strftime('%Y-%m', order_date) AS year_month,
            COUNT(order_id) AS total_orders,
            COUNT(DISTINCT customer_id) AS unique_customers
        FROM orders
        WHERE order_date >= date('now', '-12 months')
        GROUP BY year_month ORDER BY year_month
    """)

    # Query 6: Return rate
    run_query(conn, "Q6: Return Rate per Category", """
        SELECT p.category,
            SUM(CASE WHEN oi.is_return = 0 THEN oi.quantity ELSE 0 END) AS purchased,
            SUM(CASE WHEN oi.is_return = 1 THEN ABS(oi.quantity) ELSE 0 END) AS returned,
            ROUND(100.0 * SUM(CASE WHEN oi.is_return = 1 THEN ABS(oi.quantity) ELSE 0 END) /
            NULLIF(SUM(CASE WHEN oi.is_return = 0 THEN oi.quantity ELSE 0 END), 0), 2) AS return_rate
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.category ORDER BY return_rate DESC
    """)

    conn.close()
    print("\n All aggregation queries complete!")

if __name__ == "__main__":
    main()