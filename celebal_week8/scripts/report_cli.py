# ================================================
# E-Commerce Order Analytics System
# CLI Reporting Tool
# ================================================
import sqlite3
import argparse
from datetime import datetime, timedelta

DB_PATH = "output/ecommerce.db"

def get_connection():
    """Get database connection with error handling"""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Exception as e:
        print(f" Database connection error: {e}")
        return None

def print_table(headers, rows, title):
    """Print formatted table"""
    print(f"\n{'='*65}")
    print(f"  {title}")
    print('='*65)
    if not rows:
        print("  No data found for the given criteria.")
        return
    col_widths = [max(len(str(h)), max(len(str(r[i])) for r in rows))
                  for i, h in enumerate(headers)]
    header_row = " | ".join(str(h).ljust(col_widths[i])
                            for i, h in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))
    for row in rows:
        print(" | ".join(str(v).ljust(col_widths[i])
                         for i, v in enumerate(row)))

def validate_date(date_str):
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def revenue_report(conn, report_type, start_date, end_date):
    """Generate revenue report"""
    cursor = conn.cursor()

    if report_type == 'daily':
        group_by = "DATE(o.order_date)"
        label = "date"
    elif report_type == 'weekly':
        group_by = "strftime('%Y-W%W', o.order_date)"
        label = "week"
    else:
        group_by = "strftime('%Y-%m', o.order_date)"
        label = "month"

    query = f"""
        SELECT
            {group_by} AS period,
            COUNT(DISTINCT o.order_id) AS total_orders,
            COUNT(DISTINCT o.customer_id) AS unique_customers,
            ROUND(SUM(oi.quantity * oi.unit_price *
                (1 - oi.discount_percent/100.0)), 2) AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}'
          AND oi.is_return = 0
          AND o.status != 'CANCELLED'
        GROUP BY {group_by}
        ORDER BY period
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    headers = ["Period", "Orders", "Customers", "Revenue"]
    print_table(headers, rows, f"Revenue Report ({report_type.upper()}): {start_date} to {end_date}")

    # Previous period comparison
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    delta = end_dt - start_dt
    prev_start = (start_dt - timedelta(days=delta.days+1)).strftime('%Y-%m-%d')
    prev_end = (start_dt - timedelta(days=1)).strftime('%Y-%m-%d')

    cursor.execute(f"""
        SELECT
            COUNT(DISTINCT o.order_id) AS total_orders,
            ROUND(SUM(oi.quantity * oi.unit_price *
                (1 - oi.discount_percent/100.0)), 2) AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_date BETWEEN '{prev_start}' AND '{prev_end}'
          AND oi.is_return = 0
          AND o.status != 'CANCELLED'
    """)
    prev = cursor.fetchone()

    cursor.execute(f"""
        SELECT
            COUNT(DISTINCT o.order_id),
            ROUND(SUM(oi.quantity * oi.unit_price *
                (1 - oi.discount_percent/100.0)), 2)
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}'
          AND oi.is_return = 0
          AND o.status != 'CANCELLED'
    """)
    curr = cursor.fetchone()

    print(f"\n   Period Comparison:")
    print(f"  Current  → Orders: {curr[0]}, Revenue: ₹{curr[1]:,.2f}")
    print(f"  Previous → Orders: {prev[0]}, Revenue: ₹{prev[1]:,.2f}")
    if prev[1] and prev[1] > 0:
        change = ((curr[1] - prev[1]) / prev[1]) * 100
        print(f"  Change   → {change:+.2f}%")

def top_customers_report(conn, start_date, end_date):
    """Top customers report"""
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT
            c.customer_id,
            c.customer_name,
            c.customer_type,
            COUNT(DISTINCT o.order_id) AS orders,
            ROUND(SUM(oi.quantity * oi.unit_price *
                (1 - oi.discount_percent/100.0)), 2) AS revenue
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}'
          AND oi.is_return = 0
        GROUP BY c.customer_id
        ORDER BY revenue DESC
        LIMIT 5
    """)
    rows = cursor.fetchall()
    headers = ["Customer ID", "Name", "Type", "Orders", "Revenue"]
    print_table(headers, rows, f"Top Customers: {start_date} to {end_date}")

def top_products_report(conn, start_date, end_date):
    """Top products report"""
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT
            p.product_name,
            p.category,
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.quantity * oi.unit_price *
                (1 - oi.discount_percent/100.0)), 2) AS revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}'
          AND oi.is_return = 0
        GROUP BY p.product_id
        ORDER BY revenue DESC
        LIMIT 5
    """)
    rows = cursor.fetchall()
    headers = ["Product", "Category", "Units", "Revenue"]
    print_table(headers, rows, f"Top Products: {start_date} to {end_date}")

def retention_report(conn, start_date, end_date):
    """Customer retention report"""
    cursor = conn.cursor()
    cursor.execute(f"""
        WITH cohorts AS (
            SELECT customer_id,
                strftime('%Y-%m', MIN(order_date)) AS cohort_month
            FROM orders
            WHERE status != 'CANCELLED'
            GROUP BY customer_id
        ),
        cohort_size AS (
            SELECT cohort_month, COUNT(*) AS total
            FROM cohorts GROUP BY cohort_month
        )
        SELECT
            c.cohort_month,
            cs.total AS cohort_size,
            COUNT(DISTINCT o.customer_id) AS active,
            ROUND(100.0 * COUNT(DISTINCT o.customer_id) / cs.total, 2) AS retention_pct
        FROM cohorts c
        JOIN cohort_size cs ON c.cohort_month = cs.cohort_month
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY c.cohort_month
        ORDER BY c.cohort_month
        LIMIT 10
    """)
    rows = cursor.fetchall()
    headers = ["Cohort Month", "Cohort Size", "Active", "Retention %"]
    print_table(headers, rows, f"Retention Report: {start_date} to {end_date}")

def main():
    parser = argparse.ArgumentParser(
        description='E-Commerce Analytics CLI Tool'
    )
    parser.add_argument(
        '--report',
        choices=['revenue', 'top_customers', 'top_products', 'retention'],
        required=True,
        help='Report type'
    )
    parser.add_argument(
        '--type',
        choices=['daily', 'weekly', 'monthly'],
        default='monthly',
        help='Report period type (for revenue report)'
    )
    parser.add_argument(
        '--start',
        required=True,
        help='Start date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--end',
        required=True,
        help='End date (YYYY-MM-DD)'
    )

    args = parser.parse_args()

    # Validate dates
    if not validate_date(args.start) or not validate_date(args.end):
        print(" Invalid date format! Use YYYY-MM-DD")
        return

    if args.start > args.end:
        print(" Start date must be before end date!")
        return

    # Connect to database
    conn = get_connection()
    if not conn:
        return

    print(f"\n{'='*65}")
    print("  E-Commerce Order Analytics System")
    print(f"  Report: {args.report.upper()} | Period: {args.start} to {args.end}")
    print('='*65)

    try:
        if args.report == 'revenue':
            revenue_report(conn, args.type, args.start, args.end)
        elif args.report == 'top_customers':
            top_customers_report(conn, args.start, args.end)
        elif args.report == 'top_products':
            top_products_report(conn, args.start, args.end)
        elif args.report == 'retention':
            retention_report(conn, args.start, args.end)
    except Exception as e:
        print(f" Error generating report: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()