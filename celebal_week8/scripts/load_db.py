# E-Commerce Order Analytics System
# Load Cleaned Data into SQLite Database


import sqlite3
import pandas as pd
import os

DB_PATH = "output/ecommerce.db"

def create_database():
    """Create SQLite database and tables from schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open("sql/schema.sql", "r") as f:
        schema = f.read()

    cursor.executescript(schema)
    conn.commit()
    print(" Database schema created!")
    return conn

def load_data(conn):
    """Load cleaned CSV files into SQLite tables"""

    tables = {
        "customers": "data/cleaned/customers_clean.csv",
        "products": "data/cleaned/products_clean.csv",
        "orders": "data/cleaned/orders_clean.csv",
        "order_items": "data/cleaned/order_items_clean.csv"
    }

    for table, path in tables.items():
        df = pd.read_csv(path)
        df.to_sql(table, conn, if_exists="replace", index=False)
        count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table}", conn)['cnt'][0]
        print(f" {table}: {count} rows loaded")

def verify_data(conn):
    """Verify data loaded correctly"""
    print("\n=== Verification ===")
    queries = {
        "Total Customers": "SELECT COUNT(*) FROM customers",
        "Total Products": "SELECT COUNT(*) FROM products",
        "Total Orders": "SELECT COUNT(*) FROM orders",
        "Total Order Items": "SELECT COUNT(*) FROM order_items",
        "Delivered Orders": "SELECT COUNT(*) FROM orders WHERE status='DELIVERED'",
        "Return Items": "SELECT COUNT(*) FROM order_items WHERE is_return=1"
    }

    for name, query in queries.items():
        result = pd.read_sql(query, conn).iloc[0, 0]
        print(f"  {name}: {result}")

def main():
    print("=" * 50)
    print("Loading Data into SQLite Database")
    print("=" * 50)

    os.makedirs("output", exist_ok=True)
    conn = create_database()
    load_data(conn)
    verify_data(conn)
    conn.close()

    print("\n Database ready at:", DB_PATH)

if __name__ == "__main__":
    main()