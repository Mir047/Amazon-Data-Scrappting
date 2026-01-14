import sqlite3
import pandas as pd

conn = sqlite3.connect("sales_analysis.db")

query = """
SELECT country, SUM(quantity * price) AS revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_details od ON o.order_id = od.order_id
JOIN products p ON od.product_id = p.product_id
GROUP BY country
ORDER BY revenue DESC;
"""

df = pd.read_sql_query(query, conn)
print(df)

conn.close()
