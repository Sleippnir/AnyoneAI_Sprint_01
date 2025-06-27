# Gemini Project Guide: Olist E-commerce Analysis

This file provides project-specific context and instructions for Gemini. Use this as a template for other projects.

---

## 1. Project Overview & Goals

This project is a data pipeline and analysis tool for the Olist e-commerce dataset. The primary goal is to build an ELT pipeline that extracts data from CSVs and a public API, loads it into an SQLite database, and then runs SQL queries to generate analytical reports and plots.

**Current Task:** The main focus is on analyzing revenue and delivery performance metrics from 2016-2018.

---

## 2. Technology Stack

- **Language:** Python 3.9
- **Data Manipulation:** pandas, SQLAlchemy
- **Database:** SQLite
- **Plotting:** Matplotlib, Seaborn, Plotly
- **API Interaction:** requests
- **Testing:** pytest
- **Code Formatting:** black

---

## 3. Key Commands

Use these exact commands to perform common development tasks.

- **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
- **Run Linter/Formatter:**
  ```bash
  black --line-length=88 .
  ```
- **Run Tests:**
  ```bash
  pytest tests/
  ```
- **Run the main pipeline (example):**
  ```bash
  python main.py # Assuming a main.py entrypoint exists
  ```

---

## 4. Coding Conventions & Style

- **SQL Files:** All SQL-based transformations must be in `.sql` files within the `queries/` directory.
- **Pandas Transformations:** Complex, non-SQL transformations should be implemented in `src/transform.py`.
- **Function Design:** Functions should be small and have a single responsibility. Avoid monolithic functions.
- **Plotting Functions:** All plotting functions must accept an `output_path` argument to save the generated figure. They should not display the plot using `plt.show()` if `output_path` is provided.
- **Error Handling:** Use try-except blocks for network requests and database operations.
- **Docstrings:** Use Google-style docstrings for all functions.

---

## 5. Important File Locations

- **Raw Data:** `dataset/`
- **SQL Queries:** `queries/`
- **Core ETL Logic:** `src/`
  - `src/extract.py`: Data extraction from sources.
  - `src/transform.py`: Data transformation and querying.
  - `src/load.py`: Loading data into the database.
- **Generated Outputs:**
  - `outputs/data/`: Parquet files from queries.
  - `outputs/plots/`: Image files of plots.
- **Tests:** `tests/`

---

## 6. General Instructions

- **Proactive Refactoring:** When editing a file, if you spot opportunities to refactor repetitive code (like the query functions in `transform.py`), please suggest it.
- **Tool Preference:** Prefer `plotly.express` for new plots due to its interactivity and concise syntax. Use Matplotlib/Seaborn only when modifying existing plots.
- **Commit Messages:** When asked to commit, follow the conventional commit format (e.g., `feat: add new plot for revenue`).
