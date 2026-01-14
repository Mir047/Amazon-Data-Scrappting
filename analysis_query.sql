SELECT
    strftime('%Y-%m', o.order_date) AS month,
    SUM(od.quantity * p.price) AS revenue
FROM orders o
JOIN order_details od ON o.order_id = od.order_id
JOIN products p ON od.product_id = p.product_id
GROUP BY month
ORDER BY month;


SELECT
    p.product_name,
    SUM(od.quantity * p.price) AS total_revenue
FROM order_details od
JOIN products p ON od.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC
LIMIT 10;

SELECT
    c.customer_id,
    c.country,
    SUM(od.quantity * p.price) AS lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_details od ON o.order_id = od.order_id
JOIN products p ON od.product_id = p.product_id
GROUP BY c.customer_id, c.country
ORDER BY lifetime_value DESC
LIMIT 10;

SELECT
    AVG(order_value) AS avg_order_value
FROM (
    SELECT
        o.order_id,
        SUM(od.quantity * p.price) AS order_value
    FROM orders o
    JOIN order_details od ON o.order_id = od.order_id
    JOIN products p ON od.product_id = p.product_id
    GROUP BY o.order_id
);
