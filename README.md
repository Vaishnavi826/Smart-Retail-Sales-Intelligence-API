# Smart Retail Sales Intelligence API

## Project Overview

The **Smart Retail Sales Intelligence API** is a data analytics project developed to analyze retail sales data and generate meaningful business insights.

The project uses Python, FastAPI, PostgreSQL, and Streamlit to process retail sales data, provide REST APIs, and display interactive visualizations through a dashboard.

## Objectives

- Analyze retail sales performance.
- Identify top-selling products.
- Understand monthly and yearly revenue trends.
- Analyze country-wise sales performance.
- Identify high-value customers.
- Calculate average order value and sales growth.
- Generate downloadable CSV reports.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Pandas | Data cleaning and analysis |
| FastAPI | REST API development |
| PostgreSQL | Database management |
| SQLAlchemy | Database interaction |
| Streamlit | Interactive dashboard |
| Jupyter Notebook | Exploratory Data Analysis |
| Git & GitHub | Version control |

## Dataset

**Dataset:** UCI Online Retail Dataset

The cleaned dataset contains 524,878 records and 10 columns.

Data preparation included:
- Removing duplicate records.
- Removing cancelled invoices.
- Handling missing descriptions.
- Filtering invalid quantities and unit prices.
- Calculating revenue using Quantity × UnitPrice.

## Project Structure

```text
Smart_Retail_Sales_API/
│
├── app/
│   ├── analytics.py
│   ├── database.py
│   ├── import_data.py
│   ├── init_db.py
│   ├── main.py
│   ├── models.py
│   ├── products.py
│   └── schemas.py
│
├── dataset/
├── notebooks/
│   └── 01_retail_sales_EDA.ipynb
│
├── dashboard.py
├── requirements.txt
├── .gitignore
└── README.md
```

## API Features

### Product CRUD Operations

- Create products
- Retrieve all products
- Retrieve a product by ID
- Update product details
- Delete products

### Sales Analytics Endpoints

| Endpoint | Description |
|---|---|
| `/analytics/total-revenue` | Total sales revenue |
| `/analytics/total-orders` | Total unique orders |
| `/analytics/top-products` | Top-selling products |
| `/analytics/monthly-revenue` | Monthly revenue |
| `/analytics/country-sales` | Country-wise sales |
| `/analytics/top-customers` | Top customers |
| `/analytics/monthly-orders` | Monthly order count |
| `/analytics/average-order-value` | Average order value |
| `/analytics/yearly-revenue` | Yearly revenue |
| `/analytics/sales-growth` | Monthly sales growth |

## Dashboard Features

- Key Performance Indicators (KPIs)
- Monthly revenue visualization
- Monthly sales growth analysis
- Yearly revenue comparison
- Top products analysis
- Country-wise sales analysis
- Top customers analysis
- CSV report downloads

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vaishnavi826/Smart-Retail-Sales-Intelligence-API.git
```

### 2. Navigate to the project folder

```bash
cd Smart-Retail-Sales-Intelligence-API
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure PostgreSQL

Create a PostgreSQL database and configure your local `.env` file with:

```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_db
```

Keep your `.env` file private. Never upload it to GitHub.

### 7. Run the FastAPI application

```bash
python -m uvicorn app.main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

### 8. Run the Streamlit dashboard

Open another terminal and run:

```bash
python -m streamlit run dashboard.py
```

## Project Outcomes

The project provides an interactive platform for analyzing retail sales data, monitoring revenue trends, identifying important products and customers, and generating business insights.

## Author

**Vaishnavi**

GitHub: [Vaishnavi826](https://github.com/Vaishnavi826)

## Repository

[Smart Retail Sales Intelligence API](https://github.com/Vaishnavi826/Smart-Retail-Sales-Intelligence-API)
