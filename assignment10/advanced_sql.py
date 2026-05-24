import sqlite3

def get_first_5_orders(conn):
    return conn.execute("""
        SELECT o.order_id, SUM(p.price * l.quantity)
        FROM orders o
        JOIN line_items l ON o.order_id = l.order_id
        JOIN products p ON l.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id
        LIMIT 5
    """).fetchall()

def get_customer_average_prices(conn):
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

def create_perez_order(conn):
    cust_id = conn.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'").fetchone()[0]
    emp_id = conn.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris'").fetchone()[0]
    prod_ids = [row[0] for row in conn.execute("SELECT product_id FROM products ORDER BY price LIMIT 5").fetchall()]

    try:
        conn.execute("BEGIN TRANSACTION")
        order_id = conn.execute("INSERT INTO orders (customer_id, employee_id, date) VALUES (?, ?, ?) RETURNING order_id", (cust_id, emp_id, '2026-05-24')).fetchone()[0]
        for prod_id in prod_ids:
            conn.execute("INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, 10)", (order_id, prod_id))
        conn.commit()
        return order_id
    except sqlite3.Error:
        conn.rollback()
        raise

def get_order_line_items(conn, order_id):
    return conn.execute("""
        SELECT l.line_item_id, l.quantity, p.product_name
        FROM line_items l
        JOIN products p ON l.product_id = p.product_id
        WHERE l.order_id = ?
    """, (order_id,)).fetchall()

def get_employees_with_many_orders(conn):
    return conn.execute("""
        SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id)
        FROM employees e
        JOIN orders o ON e.employee_id = o.employee_id
        GROUP BY e.employee_id
        HAVING COUNT(o.order_id) > 5
    """).fetchall()

def main():
    conn = sqlite3.connect("../db/lesson.db")
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
    except sqlite3.Error as e:
        print(f"\nTransaction failed: {e}")

    print("\nTask 4:")
    for row in get_employees_with_many_orders(conn):
        print(row)

    conn.close()

if __name__ == '__main__':
    main()
