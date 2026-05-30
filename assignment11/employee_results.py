import sqlite3

import pandas as pd
import matplotlib.pyplot as plt

query = """
SELECT last_name, SUM(price * quantity) AS revenue
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY e.employee_id;
"""

with sqlite3.connect("../db/lesson.db") as conn:
    employee_results = pd.read_sql_query(query, conn)

employee_results = employee_results.sort_values("revenue", ascending=False)

ax = employee_results.plot(
    kind="bar",
    x="last_name",
    y="revenue",
    color="teal",
    legend=False,
    figsize=(11, 6),
)
ax.set_title("Revenue by Employee")
ax.set_xlabel("Employee Last Name")
ax.set_ylabel("Revenue ($)")
plt.tight_layout()
plt.show()
