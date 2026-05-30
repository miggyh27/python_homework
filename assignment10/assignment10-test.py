import sqlite3
import pytest
import advanced_sql as si

@pytest.fixture
def db_conn():
    conn = sqlite3.connect("../db/lesson.db")
    conn.execute("PRAGMA foreign_keys = 1")
    yield conn
    conn.close()

def test_first_5_orders(db_conn):
    orders = si.get_first_5_orders(db_conn)
    assert len(orders) == 5
    for row in orders:
        assert len(row) == 2
        assert isinstance(row[0], int)
        assert isinstance(row[1], (int, float))

def test_customer_average_prices(db_conn):
    prices = si.get_customer_average_prices(db_conn)
    assert len(prices) > 0
    for row in prices:
        assert len(row) == 2
        assert isinstance(row[0], str)
        assert row[1] is None or isinstance(row[1], (int, float))

def test_perez_order_creation(db_conn):
    order_id = None
    try:
        order_id = si.create_perez_order(db_conn)
        assert isinstance(order_id, int)
        items = si.get_order_line_items(db_conn, order_id)
        assert len(items) == 5
        for row in items:
            assert len(row) == 3
            assert isinstance(row[0], int)
            assert row[1] == 10
            assert isinstance(row[2], str)
    finally:
        if order_id is not None:
            db_conn.execute("DELETE FROM line_items WHERE order_id = ?", (order_id,))
            db_conn.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
            db_conn.commit()

def test_employees_with_many_orders(db_conn):
    employees = si.get_employees_with_many_orders(db_conn)
    assert len(employees) > 0
    for row in employees:
        assert len(row) == 4
        assert isinstance(row[0], int)
        assert isinstance(row[1], str)
        assert isinstance(row[2], str)
        assert row[3] > 5
