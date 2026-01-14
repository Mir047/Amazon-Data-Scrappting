CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    country TEXT
);

CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    price REAL
);

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    order_date TEXT,
    customer_id INTEGER
);

CREATE TABLE order_details (
    order_id TEXT,
    product_id TEXT,
    quantity INTEGER
);
