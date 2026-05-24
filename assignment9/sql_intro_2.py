import sqlite3
import pandas as pd

def main():
    conn = sqlite3.connect("../db/lesson.db")
    df = pd.read_sql_query("""
        SELECT line_items.line_item_id, line_items.quantity, products.product_id, products.product_name, products.price
        FROM line_items
        JOIN products ON line_items.product_id = products.product_id
    """, conn)
    print("First 5 lines of the joined DataFrame:\n", df.head())

    df['total'] = df['quantity'] * df['price']
    print("\nFirst 5 lines with total column:\n", df.head())

    df_grouped = df.groupby('product_id').agg({
        'line_item_id': 'count',
        'total': 'sum',
        'product_name': 'first'
    })
    df_grouped['total'] = df_grouped['total'].round(2)
    print("\nFirst 5 lines of the grouped DataFrame:\n", df_grouped.head())

    df_grouped.sort_values(by='product_name').to_csv('order_summary.csv')
    conn.close()

if __name__ == '__main__':
    main()
