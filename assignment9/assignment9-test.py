import os
import sqlite3
import pytest
import pandas as pd
import sql_intro as si
import sql_intro_2 as si2

def test_database_creation(tmp_path):
    db_file = tmp_path / "test_magazines.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute("PRAGMA foreign_keys = 1")
    
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS publishers (publisher_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)")
    cur.execute("CREATE TABLE IF NOT EXISTS magazines (magazine_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, publisher_id INTEGER NOT NULL, FOREIGN KEY (publisher_id) REFERENCES publishers (publisher_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS subscribers (subscriber_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, address TEXT NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS subscriptions (subscription_id INTEGER PRIMARY KEY AUTOINCREMENT, subscriber_id INTEGER NOT NULL, magazine_id INTEGER NOT NULL, expiration_date TEXT NOT NULL, FOREIGN KEY (subscriber_id) REFERENCES subscribers (subscriber_id), FOREIGN KEY (magazine_id) REFERENCES magazines (magazine_id), UNIQUE (subscriber_id, magazine_id))")
    
    pub_id1 = si.add_publisher(conn, "Pub A")
    pub_id2 = si.add_publisher(conn, "Pub A")
    assert pub_id1 == pub_id2
    
    pub_id3 = si.add_publisher(conn, "Pub B")
    assert pub_id3 != pub_id1

    mag_id1 = si.add_magazine(conn, "Mag A", pub_id1)
    mag_id2 = si.add_magazine(conn, "Mag A", pub_id1)
    assert mag_id1 == mag_id2

    with pytest.raises(sqlite3.Error):
        si.add_magazine(conn, "Mag B", 9999)

    sub_id1 = si.add_subscriber(conn, "User A", "Addr A")
    sub_id2 = si.add_subscriber(conn, "User A", "Addr A")
    assert sub_id1 == sub_id2

    sub_id3 = si.add_subscriber(conn, "User A", "Addr B")
    assert sub_id3 != sub_id1

    sub_id_test = si.add_subscription(conn, sub_id1, mag_id1, "2026-12-31")
    sub_id_test2 = si.add_subscription(conn, sub_id1, mag_id1, "2026-12-31")
    assert sub_id_test == sub_id_test2

    conn.close()

def test_order_summary_creation(tmp_path):
    csv_file = "order_summary.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
    
    si2.main()
    
    assert os.path.exists(csv_file)
    df = pd.read_csv(csv_file)
    assert "product_id" in df.columns
    assert "line_item_id" in df.columns
    assert "total" in df.columns
    assert "product_name" in df.columns
    
    names = df["product_name"].tolist()
    assert names == sorted(names)
