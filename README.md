# Sales & Revenue Analysis using SQL (SQLite)

## Objective
Analyze real-world e-commerce sales data and extract business insights using SQL.

## Dataset
Online Retail Dataset (UCI / Kaggle) containing transactional sales data.

## Tools & Technologies
- Python
- SQLite
- SQL
- Pandas

## Data Preparation
- Cleaned missing and invalid values (null customers, negative quantities)
- Normalized data into relational tables:
  - customers
  - products
  - orders
  - order_details

## Key Analysis
- Monthly revenue trends
- Top-performing products
- Customer lifetime value
- Average order value
- Revenue by country

## How to Run
1. Place `online_retail.csv` in the `data/` folder
2. Run `sqlite_sales_analysis.py`
3. SQLite database will be generated locally
4. Execute SQL queries from `analysis_queries.sql`

## Outcome
Demonstrated ability to model relational data, write analytical SQL queries, and translate business questions into insights.
