#  E-Commerce Data Pipeline: Brazil 2016–2018

This is a production-grade data pipeline I developed for a Latin American e-commerce company. The goal was to build a robust and maintainable ETL system to extract actionable insights from internal operational data and external public APIs. The pipeline integrates multiple sources, performs analytical transformations, and generates structured reports focused on revenue and delivery performance.

---

##  Business Objective

The company needed a historical analysis of performance from 2016 to 2018, focusing on:

- **Revenue**: Yearly trends, product category performance, and state-level breakdowns.
- **Delivery Performance**: Analysis of delivery delays, fulfillment lead times, and correlation with public holidays.

These outputs support business intelligence reporting and operational planning.

---

##  Data Sources

### 1. Internal Data (CSV)

Anonymized transactional records (~100K orders) exported from internal systems, including:

- `orders.csv`
- `order_items.csv`
- `customers.csv`
- `products.csv`
- `payments.csv`
- `order_reviews.csv`

The database schema is visualized in `images/data_schema.png`.
Plots available ['here'](https://sleippnir.github.io/ELT-Brazil/)

### 2. External API: Brazilian Public Holidays

Integrated with [`date.nager.at`](https://date.nager.at) to fetch national holiday data, used to enrich delivery metrics and correlate holidays with performance drops.

---

##  Pipeline Architecture & Tech Stack

This is a full Python-based ELT pipeline, built with the following tools:

- **Python**: Orchestration and core logic
- **Pandas**: Ingestion, transformation, and data cleansing
- **SQLite**: Analytical data warehouse
- **SQL**: Data aggregation and slicing
- **Requests**: External API integration
- **Matplotlib / Seaborn**: Visualization and report generation
- **Jupyter Notebooks**: Interactive exploration and reproducibility

The pipeline is modular and can be scheduled for recurring execution (e.g., monthly or annually).

---

## ⚙️ Setup & Tooling

Install dependencies with:

```bash
pip install -r requirements.txt
