from __future__ import annotations
import sqlite3

# Task 1
def get_first_5_orders(conn: sqlite3.Connection) -> list[tuple[int, float]]:
    return conn.execute("""
        SELECT o.order_id, SUM(p.price * l.quantity)
        FROM orders o
        JOIN line_items l ON o.order_id = l.order_id
        JOIN products p ON l.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id
        LIMIT 5
    """).fetchall()

# Task 2
def get_customer_average_prices(conn: sqlite3.Connection) -> list[tuple[str, float | None]]:
    return conn.execute("""
        SELECT c.customer_name, AVG(sub.total_price)
        FROM customers c
        LEFT JOIN (
            SELECT o.customer_id AS customer_id_b, SUM(p.price * l.quantity) AS total_price
            FROM orders o
            JOIN line_items l ON o.order_id = l.order_id
            JOIN products p ON l.product_id = p.product_id
            GROUP BY o.order_id
        ) AS sub ON c.customer_id = sub.customer_id_b
        GROUP BY c.customer_id
    """).fetchall()

# Task 3
def create_perez_order(conn: sqlite3.Connection) -> int:
    cust_row = conn.execute(
        "SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'"
    ).fetchone()
    if cust_row is None:
        raise ValueError("Customer 'Perez and Sons' not found")
    cust_id = cust_row[0]

    emp_row = conn.execute(
        "SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris'"
    ).fetchone()
    if emp_row is None:
        raise ValueError("Employee 'Miranda Harris' not found")
    emp_id = emp_row[0]

    prod_rows = conn.execute(
        "SELECT product_id FROM products ORDER BY price LIMIT 5"
    ).fetchall()
    prod_ids = [row[0] for row in prod_rows]

    with conn:
        order_row = conn.execute(
            "INSERT INTO orders (customer_id, employee_id, date) "
            "VALUES (?, ?, ?) RETURNING order_id",
            (cust_id, emp_id, "2026-05-24")
        ).fetchone()
        if order_row is None:
            raise RuntimeError("Failed to retrieve inserted order_id")
        order_id = order_row[0]

        for prod_id in prod_ids:
            conn.execute(
                "INSERT INTO line_items (order_id, product_id, quantity) "
                "VALUES (?, ?, 10)",
                (order_id, prod_id)
            )

    return order_id

def get_order_line_items(conn: sqlite3.Connection, order_id: int) -> list[tuple[int, int, str]]:
    return conn.execute("""
        SELECT l.line_item_id, l.quantity, p.product_name
        FROM line_items l
        JOIN products p ON l.product_id = p.product_id
        WHERE l.order_id = ?
    """, (order_id,)).fetchall()

# Task 4
def get_employees_with_many_orders(conn: sqlite3.Connection) -> list[tuple[int, str, str, int]]:
    return conn.execute("""
        SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id)
        FROM employees e
        JOIN orders o ON e.employee_id = o.employee_id
        GROUP BY e.employee_id
        HAVING COUNT(o.order_id) > 5
    """).fetchall()

def main() -> None:
    conn = sqlite3.connect("../db/lesson.db")
    try:
        conn.execute("PRAGMA foreign_keys = 1")

        print("Task 1:")
        for row in get_first_5_orders(conn):
            print(row)

        print("\nTask 2:")
        for row in get_customer_average_prices(conn):
            print(row)

        try:
            order_id = create_perez_order(conn)
            print("\nTask 3:")
            for row in get_order_line_items(conn, order_id):
                print(row)
        except (sqlite3.Error, ValueError, RuntimeError) as e:
            print(f"\nTransaction failed: {e}")

        print("\nTask 4:")
        for row in get_employees_with_many_orders(conn):
            print(row)
    finally:
        conn.close()

if __name__ == "__main__":
    main()

