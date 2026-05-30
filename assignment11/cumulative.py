import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


query = """
SELECT o.order_id, SUM(p.price * l.quantity) AS total_price
FROM orders o
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id;
"""

with sqlite3.connect("../db/lesson.db") as conn:
    df = pd.read_sql_query(query, conn)


df["cumulative"] = df["total_price"].cumsum()

ax = df.plot(
    kind="line",
    x="order_id",
    y="cumulative",
    color="darkgreen",
    legend=False,
    figsize=(11, 6),
)
ax.set_title("Cumulative Revenue by Order")
ax.set_xlabel("Order ID")
ax.set_ylabel("Cumulative Revenue ($)")
plt.tight_layout()
plt.show()
