import os
import sqlite3

def add_publisher(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT publisher_id FROM publishers WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
    return cur.lastrowid

def add_magazine(conn, name, publisher_id):
    cur = conn.cursor()
    cur.execute("SELECT magazine_id FROM magazines WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?)", (name, publisher_id))
    return cur.lastrowid

def add_subscriber(conn, name, address):
    cur = conn.cursor()
    cur.execute("SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?", (name, address))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address))
    return cur.lastrowid

def add_subscription(conn, subscriber_id, magazine_id, expiration_date):
    cur = conn.cursor()
    cur.execute("SELECT subscription_id FROM subscriptions WHERE subscriber_id = ? AND magazine_id = ?", (subscriber_id, magazine_id))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)", (subscriber_id, magazine_id, expiration_date))
    return cur.lastrowid

def main():
    os.makedirs("../db", exist_ok=True)
    conn = None
    try:
        conn = sqlite3.connect("../db/magazines.db")
        conn.execute("PRAGMA foreign_keys = 1")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS publishers (publisher_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)")
        cur.execute("CREATE TABLE IF NOT EXISTS magazines (magazine_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, publisher_id INTEGER NOT NULL, FOREIGN KEY (publisher_id) REFERENCES publishers (publisher_id))")
        cur.execute("CREATE TABLE IF NOT EXISTS subscribers (subscriber_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, address TEXT NOT NULL)")
        cur.execute("CREATE TABLE IF NOT EXISTS subscriptions (subscription_id INTEGER PRIMARY KEY AUTOINCREMENT, subscriber_id INTEGER NOT NULL, magazine_id INTEGER NOT NULL, expiration_date TEXT NOT NULL, FOREIGN KEY (subscriber_id) REFERENCES subscribers (subscriber_id), FOREIGN KEY (magazine_id) REFERENCES magazines (magazine_id), UNIQUE (subscriber_id, magazine_id))")

        pub1 = add_publisher(conn, "Tech Media Corp")
        pub2 = add_publisher(conn, "Science Weekly Group")
        pub3 = add_publisher(conn, "Fashion Lifestyle Inc")

        mag1 = add_magazine(conn, "Byte and Bit", pub1)
        mag2 = add_magazine(conn, "Quantum Physics Today", pub2)
        mag3 = add_magazine(conn, "Vogue Essentials", pub3)

        sub1 = add_subscriber(conn, "Alice Smith", "123 Main St")
        sub2 = add_subscriber(conn, "Bob Jones", "456 Oak Ave")
        sub3 = add_subscriber(conn, "Charlie Brown", "789 Pine Rd")

        add_subscription(conn, sub1, mag1, "2026-12-31")
        add_subscription(conn, sub2, mag2, "2027-06-30")
        add_subscription(conn, sub3, mag3, "2026-09-15")

        conn.commit()

        print("Query 1: All subscribers:")
        for row in cur.execute("SELECT * FROM subscribers").fetchall():
            print(row)

        print("\nQuery 2: Magazines sorted by name:")
        for row in cur.execute("SELECT * FROM magazines ORDER BY name").fetchall():
            print(row)

        print("\nQuery 3: Magazines published by 'Science Weekly Group':")
        for row in cur.execute("SELECT m.magazine_id, m.name, p.name FROM magazines m JOIN publishers p ON m.publisher_id = p.publisher_id WHERE p.name = ?", ("Science Weekly Group",)).fetchall():
            print(row)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    main()
