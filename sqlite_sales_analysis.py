import pandas as pd
import sqlite3

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(
    "online_retail.csv",
    encoding="ISO-8859-1"
)

# -----------------------------
# Data cleaning
# -----------------------------
df = df.dropna(subset=["Customer ID"])
df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]

df["Customer ID"] = df["Customer ID"].astype(int)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# -----------------------------
# Create tables dataframes
# -----------------------------
customers = (
    df[["Customer ID", "Country"]]
    .drop_duplicates()
    .rename(columns={
        "Customer ID": "customer_id",
        "Country": "country"
    })
)

products = (
    df[["StockCode", "Description", "Price"]]
    .drop_duplicates()
    .rename(columns={
        "StockCode": "product_id",
        "Description": "product_name",
        "Price": "price"
    })
)

orders = (
    df[["Invoice", "InvoiceDate", "Customer ID"]]
    .drop_duplicates()
    .rename(columns={
        "Invoice": "order_id",
        "InvoiceDate": "order_date",
        "Customer ID": "customer_id"
    })
)

order_details = df.rename(columns={
    "Invoice": "order_id",
    "StockCode": "product_id",
    "Quantity": "quantity"
})[["order_id", "product_id", "quantity"]]

# -----------------------------
# Create SQLite DB
# -----------------------------
conn = sqlite3.connect("sales_analysis.db")

customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)
order_details.to_sql("order_details", conn, if_exists="replace", index=False)

conn.close()

print("SQLite database created successfully.")
