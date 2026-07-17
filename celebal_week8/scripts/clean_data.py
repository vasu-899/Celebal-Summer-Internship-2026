# Celebal Technologies Summer Internship 2026
# E-Commerce Order Analytics System
# Part 2: Data Cleaning

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

# Load Raw Data
def load_raw_data():
    """Load all raw CSV files into DataFrames"""
    df_customers = pd.read_csv("data/raw/customers.csv")
    df_products = pd.read_csv("data/raw/products.csv")
    df_orders = pd.read_csv("data/raw/orders.csv")
    df_order_items = pd.read_csv("data/raw/order_items.csv")

    print("=" * 55)
    print("Raw Data Loaded:")
    print(f"  customers:   {len(df_customers)} rows")
    print(f"  products:    {len(df_products)} rows")
    print(f"  orders:      {len(df_orders)} rows")
    print(f"  order_items: {len(df_order_items)} rows")
    print("=" * 55)

    return df_customers, df_products, df_orders, df_order_items

# Clean Orders
def clean_orders(df):
    """
    Cleans orders DataFrame:
    - Fix date formats (DD-MM-YYYY → YYYY-MM-DD)
    - Handle NULL customer_ids
    - Remove duplicates
    """
    issues = []
    print("\n=== Cleaning Orders ===")

    # Fix date formats
    def fix_date(date_str):
        if pd.isna(date_str):
            return None
        date_str = str(date_str)
        # Try standard format first
        for fmt in ['%Y-%m-%d %H:%M:%S', '%d-%m-%Y %H:%M:%S',
                    '%Y-%m-%d', '%d-%m-%Y']:
            try:
                return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d %H:%M:%S')
            except:
                continue
        return None

    wrong_dates = df['order_date'].apply(
        lambda x: str(x).startswith(tuple('0123456789')) and
        len(str(x)) > 0 and str(x)[2] == '-'
    ).sum()

    df['order_date'] = df['order_date'].apply(fix_date)
    issues.append(f"Fixed {wrong_dates} wrong date formats")
    print(f"   Fixed {wrong_dates} wrong date formats")

    # Handle NULL customer_ids
    null_customers = df['customer_id'].isna().sum()
    df['customer_id'] = df['customer_id'].fillna('UNKNOWN')
    issues.append(f"Filled {null_customers} NULL customer_ids with UNKNOWN")
    print(f"   Filled {null_customers} NULL customer_ids")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=['order_id'])
    after = len(df)
    issues.append(f"Removed {before - after} duplicate orders")
    print(f"   Removed {before - after} duplicates")

    print(f"   Orders cleaned: {len(df)} rows")
    return df, issues

# Clean Products
def clean_products(df):
    """
    Cleans products DataFrame:
    - Normalize product names (trim spaces, title case)
    - Handle missing values
    """
    issues = []
    print("\n=== Cleaning Products ===")

    # Fix product names
    before_names = df['product_name'].tolist()
    df['product_name'] = df['product_name'].str.strip().str.title()
    changed = sum(1 for a, b in zip(before_names, df['product_name'].tolist()) if a != b)
    issues.append(f"Normalized {changed} product names")
    print(f"   Normalized {changed} product names")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=['product_id'])
    issues.append(f"Removed {before - len(df)} duplicate products")
    print(f"   Removed {before - len(df)} duplicates")

    print(f"   Products cleaned: {len(df)} rows")
    return df, issues

# Validate Emails
def validate_emails(df):
    """
    Returns list of customer_ids with invalid emails
    """
    print("\n=== Validating Emails ===")

    def is_valid_email(email):
        if pd.isna(email):
            return False
        email = str(email)
        return '@' in email and '.' in email.split('@')[-1]

    df['email_valid'] = df['email'].apply(is_valid_email)
    invalid = df[~df['email_valid']]['customer_id'].tolist()
    print(f"   Invalid emails found: {len(invalid)}")
    print(f"  Invalid customer_ids: {invalid[:5]}...")

    df = df.drop(columns=['email_valid'])
    return df, invalid

# Check Referential Integrity
def check_referential_integrity(df_orders, df_order_items):
    """
    Find order_items that reference non-existent orders
    """
    print("\n=== Checking Referential Integrity ===")

    valid_order_ids = set(df_orders['order_id'].tolist())
    orphan_items = df_order_items[
        ~df_order_items['order_id'].isin(valid_order_ids)
    ]

    print(f"   Orphan order_items found: {len(orphan_items)}")
    if len(orphan_items) > 0:
        print(f"  Orphan order_ids: {orphan_items['order_id'].tolist()}")

    # Remove orphan items
    df_clean = df_order_items[df_order_items['order_id'].isin(valid_order_ids)]
    print(f"   Clean order_items: {len(df_clean)} rows")

    return df_clean, orphan_items


# Clean Order Items
def clean_order_items(df):
    """
    Cleans order_items DataFrame:
    - Flag negative quantities (returns)
    - Fix invalid discount_percent > 100
    - Remove duplicates
    """
    issues = []
    print("\n=== Cleaning Order Items ===")

    # Flag negative quantities
    negative_qty = (df['quantity'] < 0).sum()
    df['is_return'] = df['quantity'] < 0
    issues.append(f"Flagged {negative_qty} negative quantities as returns")
    print(f"   Flagged {negative_qty} returns")

    # Fix invalid discounts
    invalid_discount = (df['discount_percent'] > 100).sum()
    df.loc[df['discount_percent'] > 100, 'discount_percent'] = 100
    issues.append(f"Fixed {invalid_discount} invalid discount_percent > 100")
    print(f"   Fixed {invalid_discount} invalid discounts")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=['item_id'])
    issues.append(f"Removed {before - len(df)} duplicate items")
    print(f"   Removed {before - len(df)} duplicates")

    print(f"   Order items cleaned: {len(df)} rows")
    return df, issues


# Generate Issues Report
def generate_report(all_issues, invalid_emails, orphan_items):
    """Generate a report of all issues found"""

    report = {
        "report_generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "summary": {
            "total_issues": len(all_issues) + len(invalid_emails) + len(orphan_items),
            "invalid_emails": len(invalid_emails),
            "orphan_order_items": len(orphan_items)
        },
        "issues": all_issues,
        "invalid_email_customers": invalid_emails,
        "orphan_order_ids": orphan_items['order_id'].tolist() if len(orphan_items) > 0 else []
    }

    os.makedirs("output", exist_ok=True)
    with open("output/issues_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n=== Issues Report ===")
    print(f"  Total issues found: {report['summary']['total_issues']}")
    print(f"  Invalid emails:     {report['summary']['invalid_emails']}")
    print(f"  Orphan items:       {report['summary']['orphan_order_items']}")
    print("   Report saved to output/issues_report.json")


# Main
def main():
    print("=" * 55)
    print("E-Commerce Data Cleaning Pipeline")
    print("=" * 55)

    # Load data
    df_customers, df_products, df_orders, df_order_items = load_raw_data()

    all_issues = []

    # Clean each table
    df_orders_clean, order_issues = clean_orders(df_orders)
    all_issues.extend(order_issues)

    df_products_clean, product_issues = clean_products(df_products)
    all_issues.extend(product_issues)

    df_customers_clean, invalid_emails = validate_emails(df_customers)
    all_issues.append(f"Found {len(invalid_emails)} invalid emails")

    df_order_items_clean, orphan_items = check_referential_integrity(
        df_orders_clean, df_order_items
    )

    df_order_items_clean, item_issues = clean_order_items(df_order_items_clean)
    all_issues.extend(item_issues)

    # Save cleaned files
    os.makedirs("data/cleaned", exist_ok=True)
    df_customers_clean.to_csv("data/cleaned/customers_clean.csv", index=False)
    df_products_clean.to_csv("data/cleaned/products_clean.csv", index=False)
    df_orders_clean.to_csv("data/cleaned/orders_clean.csv", index=False)
    df_order_items_clean.to_csv("data/cleaned/order_items_clean.csv", index=False)

    print("\n=== Cleaned Files Saved ===")
    print(f"  customers_clean.csv:   {len(df_customers_clean)} rows")
    print(f"  products_clean.csv:    {len(df_products_clean)} rows")
    print(f"  orders_clean.csv:      {len(df_orders_clean)} rows")
    print(f"  order_items_clean.csv: {len(df_order_items_clean)} rows")

    # Generate report
    generate_report(all_issues, invalid_emails, orphan_items)

    print("\n" + "=" * 55)
    print(" Data Cleaning Complete!")
    print("=" * 55)

if __name__ == "__main__":
    main()