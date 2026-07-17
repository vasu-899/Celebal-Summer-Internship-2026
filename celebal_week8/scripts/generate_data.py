# Celebal Technologies Summer Internship 2026
## E-Commerce Order Analytics System
## Part 1: Data Generation

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker('en_IN')
random.seed(42)
np.random.seed(42)

# Configuration
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 100
NUM_ORDERS = 600
NUM_ORDER_ITEMS = 1500

CATEGORIES = ['Electronics', 'Clothing', 'Home', 'Books']
SUBCATEGORIES = {
    'Electronics': ['Mobile', 'Laptop', 'Tablet', 'Accessories'],
    'Clothing': ['Men', 'Women', 'Kids', 'Sports'],
    'Home': ['Kitchen', 'Furniture', 'Decor', 'Bedding'],
    'Books': ['Fiction', 'Non-Fiction', 'Academic', 'Comics']
}
STATUS_LIST = ['PLACED', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED']
CUSTOMER_TYPES = ['REGULAR', 'PREMIUM', 'VIP']
REGIONS = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'CENTRAL']


# Generate Customers
def generate_customers():
    """
    Generates customer data with intentional issues:
    - 2% invalid emails (missing @ or domain)
    """
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        customer_id = f"CUST{i:04d}"
        name = fake.name()
        email = fake.email()

        # Introduce 2% invalid emails
        if random.random() < 0.02:
            if random.random() < 0.5:
                email = email.replace('@', '')  # missing @
            else:
                email = email.split('@')[0]  # missing domain

        reg_date = fake.date_between(
            start_date='-3y', end_date='today'
        ).strftime('%Y-%m-%d')

        customer_type = random.choice(CUSTOMER_TYPES)

        customers.append({
            'customer_id': customer_id,
            'customer_name': name,
            'email': email,
            'registration_date': reg_date,
            'customer_type': customer_type
        })

    df = pd.DataFrame(customers)
    print(f" Customers generated: {len(df)} rows")
    return df

# Generate Products
def generate_products():
    """
    Generates product data with intentional issues:
    - Some product names have extra spaces or mixed case
    """
    products = []
    for i in range(1, NUM_PRODUCTS + 1):
        product_id = f"PROD{i:04d}"
        category = random.choice(CATEGORIES)
        subcategory = random.choice(SUBCATEGORIES[category])
        product_name = f"{fake.word().title()} {subcategory} {fake.word().title()}"

        # Introduce mixed case / extra spaces
        if random.random() < 0.15:
            product_name = product_name.upper()
        if random.random() < 0.15:
            product_name = "  " + product_name + "  "

        cost_price = round(random.uniform(50, 5000), 2)

        products.append({
            'product_id': product_id,
            'product_name': product_name,
            'category': category,
            'subcategory': subcategory,
            'cost_price': cost_price
        })

    df = pd.DataFrame(products)
    print(f" Products generated: {len(df)} rows")
    return df


# Generate Orders
def generate_orders(customer_ids):
    """
    Generates order data with intentional issues:
    - 5% NULL customer_id
    - Some wrong date formats (DD-MM-YYYY)
    """
    orders = []
    for i in range(1, NUM_ORDERS + 1):
        order_id = f"ORD{i:05d}"

        # 5% NULL customer_id
        if random.random() < 0.05:
            customer_id = None
        else:
            customer_id = random.choice(customer_ids)

        # Generate order date
        order_dt = fake.date_time_between(
            start_date='-2y', end_date='now'
        )

        # Some wrong date formats (10% DD-MM-YYYY)
        if random.random() < 0.10:
            order_date = order_dt.strftime('%d-%m-%Y %H:%M:%S')
        else:
            order_date = order_dt.strftime('%Y-%m-%d %H:%M:%S')

        status = random.choice(STATUS_LIST)
        region_code = random.choice(REGIONS)

        orders.append({
            'order_id': order_id,
            'customer_id': customer_id,
            'order_date': order_date,
            'status': status,
            'region_code': region_code
        })

    df = pd.DataFrame(orders)
    print(f" Orders generated: {len(df)} rows")
    return df

# Generate Order Items
def generate_order_items(order_ids, product_ids):
    """
    Generates order items with intentional issues:
    - 3% negative quantity (returns)
    - Some discount_percent > 100
    """
    order_items = []
    item_id = 1

    for i in range(NUM_ORDER_ITEMS):
        item = f"ITEM{item_id:05d}"
        order_id = random.choice(order_ids)
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 10)

        # 3% negative quantity (returns)
        if random.random() < 0.03:
            quantity = -random.randint(1, 5)

        unit_price = round(random.uniform(100, 10000), 2)
        discount_percent = round(random.uniform(0, 30), 2)

        # Some invalid discounts > 100
        if random.random() < 0.01:
            discount_percent = round(random.uniform(101, 150), 2)

        order_items.append({
            'item_id': item,
            'order_id': order_id,
            'product_id': product_id,
            'quantity': quantity,
            'unit_price': unit_price,
            'discount_percent': discount_percent
        })
        item_id += 1

    # Add some orphan order_ids (not in orders table)
    for i in range(10):
        order_items.append({
            'item_id': f"ITEM{item_id:05d}",
            'order_id': f"ORD99{i:03d}",
            'product_id': random.choice(product_ids),
            'quantity': random.randint(1, 5),
            'unit_price': round(random.uniform(100, 1000), 2),
            'discount_percent': round(random.uniform(0, 30), 2)
        })
        item_id += 1

    df = pd.DataFrame(order_items)
    print(f" Order Items generated: {len(df)} rows")
    return df


# Main: Generate and Save All Files
def main():
    print("=" * 50)
    print("Generating E-Commerce Dataset...")
    print("=" * 50)

    # Create directories
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/cleaned", exist_ok=True)

    # Generate data
    df_customers = generate_customers()
    df_products = generate_products()
    df_orders = generate_orders(df_customers['customer_id'].tolist())
    df_order_items = generate_order_items(
        df_orders['order_id'].tolist(),
        df_products['product_id'].tolist()
    )

    # Save raw files
    df_customers.to_csv("data/raw/customers.csv", index=False)
    df_products.to_csv("data/raw/products.csv", index=False)
    df_orders.to_csv("data/raw/orders.csv", index=False)
    df_order_items.to_csv("data/raw/order_items.csv", index=False)

    print("\n" + "=" * 50)
    print("Raw CSV files saved to data/raw/")
    print("=" * 50)
    print(f"customers.csv:   {len(df_customers)} rows")
    print(f"products.csv:    {len(df_products)} rows")
    print(f"orders.csv:      {len(df_orders)} rows")
    print(f"order_items.csv: {len(df_order_items)} rows")

if __name__ == "__main__":
    main()