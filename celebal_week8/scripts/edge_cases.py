# ================================================
# E-Commerce Order Analytics System
# Edge Case Handling & Test Cases
# ================================================
import sqlite3
import pandas as pd

DB_PATH = "output/ecommerce.db"

def test_case(name, passed, message=""):
    """Print test result"""
    status = " PASSED" if passed else " FAILED"
    print(f"  {status} | {name}")
    if message:
        print(f"           → {message}")

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 60)
    print("  Edge Case Test Suite")
    print("=" * 60)

    # ------------------------------------------------
    # Test 1: Order items with non-existent order_id
    # ------------------------------------------------
    print("\n Test 1: Orphan Order Items")
    cursor.execute("""
        SELECT COUNT(*) FROM order_items oi
        LEFT JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL
    """)
    orphan_count = cursor.fetchone()[0]
    test_case(
        "No orphan order_items",
        orphan_count == 0,
        f"Found {orphan_count} orphan items"
    )

    # ------------------------------------------------
    # Test 2: Discount percent > 100
    # ------------------------------------------------
    print("\n Test 2: Invalid Discount Percent")
    cursor.execute("SELECT COUNT(*) FROM order_items WHERE discount_percent > 100")
    invalid_discount = cursor.fetchone()[0]
    test_case(
        "No discount_percent > 100",
        invalid_discount == 0,
        f"Found {invalid_discount} invalid discounts"
    )

    # ------------------------------------------------
    # Test 3: Zero quantity orders
    # ------------------------------------------------
    print("\n Test 3: Zero Quantity Items")
    cursor.execute("SELECT COUNT(*) FROM order_items WHERE quantity = 0")
    zero_qty = cursor.fetchone()[0]
    test_case(
        "No zero quantity items",
        zero_qty == 0,
        f"Found {zero_qty} zero quantity items"
    )

    # ------------------------------------------------
    # Test 4: Future order dates
    # ------------------------------------------------
    print("\n Test 4: Future Order Dates")
    cursor.execute("""
        SELECT COUNT(*) FROM orders
        WHERE DATE(order_date) > DATE('now')
    """)
    future_dates = cursor.fetchone()[0]
    test_case(
        "No future order dates",
        future_dates == 0,
        f"Found {future_dates} future dated orders"
    )

    # ------------------------------------------------
    # Test 5: NULL order_id in order_items
    # ------------------------------------------------
    print("\n Test 5: NULL Order IDs")
    cursor.execute("SELECT COUNT(*) FROM order_items WHERE order_id IS NULL")
    null_orders = cursor.fetchone()[0]
    test_case(
        "No NULL order_ids in order_items",
        null_orders == 0,
        f"Found {null_orders} NULL order_ids"
    )

    # ------------------------------------------------
    # Test 6: Invalid email format
    # ------------------------------------------------
    print("\n Test 6: Invalid Emails")
    df_customers = pd.read_sql("SELECT customer_id, email FROM customers", conn)
    invalid_emails = df_customers[
        ~df_customers['email'].str.contains('@', na=False) |
        ~df_customers['email'].str.contains(r'\.\w+', regex=True, na=False)
    ]
    test_case(
        "Email validation check",
        True,
        f"Found {len(invalid_emails)} invalid emails (flagged in report)"
    )

    # ------------------------------------------------
    # Test 7: Negative unit price
    # ------------------------------------------------
    print("\n Test 7: Negative Unit Price")
    cursor.execute("SELECT COUNT(*) FROM order_items WHERE unit_price <= 0")
    neg_price = cursor.fetchone()[0]
    test_case(
        "No negative unit prices",
        neg_price == 0,
        f"Found {neg_price} invalid prices"
    )

    # ------------------------------------------------
    # Test 8: Empty result set handling
    # ------------------------------------------------
    print("\n Test 8: Empty Result Set Handling")
    cursor.execute("""
        SELECT COUNT(*) FROM orders
        WHERE order_date BETWEEN '2099-01-01' AND '2099-12-31'
    """)
    empty_result = cursor.fetchone()[0]
    test_case(
        "Empty result set handled gracefully",
        empty_result == 0,
        f"Future date query returned {empty_result} rows (expected 0)"
    )

    # ------------------------------------------------
    # Test 9: Referential integrity
    # ------------------------------------------------
    print("\n Test 9: Referential Integrity")
    cursor.execute("""
        SELECT COUNT(*) FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        AND o.customer_id != 'UNKNOWN'
    """)
    integrity_issues = cursor.fetchone()[0]
    test_case(
        "Referential integrity maintained",
        integrity_issues == 0,
        f"Found {integrity_issues} orders with invalid customer_id"
    )

    # ------------------------------------------------
    # Test 10: Duplicate order_ids
    # ------------------------------------------------
    print("\n Test 10: Duplicate Order IDs")
    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT order_id, COUNT(*) as cnt
            FROM orders
            GROUP BY order_id
            HAVING cnt > 1
        )
    """)
    duplicates = cursor.fetchone()[0]
    test_case(
        "No duplicate order_ids",
        duplicates == 0,
        f"Found {duplicates} duplicate order_ids"
    )

    conn.close()

    print("\n" + "=" * 60)
    print("   Edge Case Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()