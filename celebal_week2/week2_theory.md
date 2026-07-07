# Week 2 - SQL Assignment: E-Commerce Sales Database
## Celebal Technologies Summer Internship 2026

---

## Q4: Primary Keys in the Schema

The Primary Key of each table is as follows:
- **customers** → `customer_id`
- **products** → `product_id`
- **orders** → `order_id`
- **order_items** → `item_id`

**Why must a Primary Key be UNIQUE and NOT NULL?**
A Primary Key uniquely identifies each row in a table. If two rows had the same Primary Key, the database would be unable to distinguish between them, leading to data integrity issues. A NULL value means "unknown" — if a Primary Key were NULL, the row could not be reliably referenced by other tables through Foreign Keys. Therefore, every Primary Key must be both unique and non-null.

---

## Q5: Constraints on the Email Column

The `email` column in the `customers` table has two constraints applied:
1. **UNIQUE** – No two customers can have the same email address.
2. **NOT NULL** – Every customer must have an email address; it cannot be left empty.

**What happens if a duplicate email is inserted?**
MySQL will throw an error:
`ERROR 1062: Duplicate entry 'example@email.com' for key 'email'`
The insert operation will be rejected, and no data will be added to the table.

---

## Q6: Inserting a Product with Negative Price

**INSERT Statement:**
```sql
INSERT INTO products VALUES (209, 'Test Product', 'Electronics', 'TestBrand', -50, 100);
```

**Result:**
MySQL will throw an error:
`ERROR 3819: Check constraint 'products_chk_1' is violated.`

**Explanation:**
The `unit_price` column has a CHECK constraint: `unit_price > 0`. Since -50 is not greater than 0, the database rejects the insert. This constraint ensures that no product can be stored with an invalid or negative price, maintaining data quality.

---

## Q11: Role of idx_orders_date Index

The index `idx_orders_date` is created on the `order_date` column of the `orders` table. It stores the values of `order_date` in a sorted structure (B-Tree), allowing MySQL to locate matching rows quickly without scanning the entire table.

**Performance Benefit:**
Without the index, MySQL performs a full table scan — checking every row. With the index, it jumps directly to the relevant rows, significantly reducing query execution time as the table grows.

**Sample Query that benefits from this index:**
```sql
SELECT * FROM orders WHERE order_date = '2024-08-15';
```

---

## Q12: SARGable Query Rewrite

**Original Query (not index-friendly):**
```sql
SELECT * FROM customers WHERE YEAR(join_date) = 2024;
```
This query wraps the column inside a function `YEAR()`. When a function is applied to an indexed column, MySQL cannot use the index — it must evaluate the function for every row, resulting in a full table scan.

**Rewritten SARGable Query:**
```sql
SELECT * FROM customers 
WHERE join_date BETWEEN '2024-01-01' AND '2024-12-31';
```
This version directly compares the column value against a range, allowing MySQL to use the index on `join_date` efficiently.

---

## Q22: LEFT JOIN vs RIGHT JOIN vs FULL OUTER JOIN

**LEFT JOIN:**
Returns all rows from the left table, and matching rows from the right table. If no match exists, NULL is returned for right table columns.

**RIGHT JOIN:**
Returns all rows from the right table, and matching rows from the left table. If no match exists, NULL is returned for left table columns.

**Example from this schema:**
```sql
-- Shows all customers, even those who have never placed an order
SELECT c.first_name, c.last_name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

**FULL OUTER JOIN:**
Returns all rows from both tables, with NULLs where there is no match. This is useful when you want to see all records from both sides regardless of whether a match exists. Note: MySQL does not support FULL OUTER JOIN directly — it can be achieved using a UNION of LEFT JOIN and RIGHT JOIN.

---

## Q23: Foreign Key Relationships & Referential Integrity

**Foreign Key Relationships in the Schema:**
- `orders.customer_id` → references `customers.customer_id`
- `order_items.order_id` → references `orders.order_id`
- `order_items.product_id` → references `products.product_id`

**What happens if you insert an order with customer_id = 999?**
Since customer_id = 999 does not exist in the `customers` table, MySQL will throw a referential integrity error:
`ERROR 1452: Cannot add or update a child row: a foreign key constraint fails`

The insert will be rejected. This ensures that every order must belong to a valid, existing customer — preventing orphan records in the database.

---

## Q26: ACID Properties

**A – Atomicity:**
A transaction is treated as a single unit — either all operations succeed, or none of them are applied. If any step fails, the entire transaction is rolled back.
*Example:* In a bank transfer, if ₹5000 is debited from Account A but the credit to Account B fails, the debit is also reversed. The money is never lost.

**C – Consistency:**
A transaction brings the database from one valid state to another. All rules, constraints, and integrity checks must be satisfied before and after the transaction.
*Example:* A bank account balance cannot go below zero. If a withdrawal would violate this rule, the transaction is rejected, keeping the database consistent.

**I – Isolation:**
Concurrent transactions execute independently without interfering with each other. Intermediate states of a transaction are not visible to other transactions.
*Example:* If two users book the last seat on a flight simultaneously, isolation ensures only one booking succeeds — the other sees the updated (unavailable) state.

**D – Durability:**
Once a transaction is committed, the changes are permanently saved — even if the system crashes immediately after.
*Example:* After a successful payment, the transaction record is written to disk. Even if the server restarts, the payment remains recorded.

## Brief Insights

- Total 10 orders placed, out of which 6 were Delivered, 2 Shipped, 1 Cancelled, 1 Pending.
- Total revenue from Delivered orders: ₹17,191
- Electronics is the highest priced category with average unit price of ₹2,224
- Aarav Sharma (customer 101) is the most active customer with 2 orders
- Running Shoes (₹4,599) is the most expensive product overall
- Budget category products: Laptop Stand and Cushion Covers
- Premium category products: Running Shoes and Bluetooth Speaker