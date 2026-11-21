
import pandas as pd
from sqlalchemy import select
from app.database import engine
from app.models import Product, Customer, Sale, Base

# 1. Load cleaned dataset
df = pd.read_csv(
    "dataset/cleaned_retail_sales.csv",
    dtype={
        "InvoiceNo": str,
        "StockCode": str
    },
    low_memory=False
)

print("Dataset loaded:", len(df))

# 2. Prepare data types
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)

df["CustomerID"] = pd.to_numeric(
    df["CustomerID"], errors="coerce"
).astype("Int64")

# Check invalid dates
if df["InvoiceDate"].isna().any():
    raise ValueError("Some invoice dates are invalid. Check the dataset.")

# 3. Prepare unique products
products_df = df[["StockCode", "Description"]].drop_duplicates(
    subset=["StockCode"]
)

# 4. Prepare unique customers
customers_df = df.loc[
    df["CustomerID"].notna(),
    ["CustomerID", "Country"]
].drop_duplicates(subset=["CustomerID"])

# 5. Prepare and insert data
with engine.begin() as connection:

    # Insert products
    product_records = [
        {
            "stock_code": row.StockCode,
            "description": row.Description
        }
        for row in products_df.itertuples(index=False)
    ]

    connection.execute(
        Product.__table__.insert(),
        product_records
    )

    print("Products inserted:", len(product_records))

    # Insert customers
    customer_records = [
        {
            "customer_id": int(row.CustomerID),
            "country": row.Country
        }
        for row in customers_df.itertuples(index=False)
    ]

    connection.execute(
        Customer.__table__.insert(),
        customer_records
    )

    print("Customers inserted:", len(customer_records))

    # Get product IDs
    product_map = dict(
        connection.execute(
            select(Product.stock_code, Product.product_id)
        ).all()
    )

    # Insert sales in batches
    batch_size = 10000
    total_sales = 0

    for start in range(0, len(df), batch_size):

        batch = df.iloc[start:start + batch_size].copy()

        batch["product_id"] = batch["StockCode"].map(product_map)

        if batch["product_id"].isna().any():
            raise ValueError("Some products have no matching product ID.")

        sales_records = []

        for row in batch.itertuples(index=False):
            customer_id = (
                int(row.CustomerID)
                if pd.notna(row.CustomerID)
                else None
            )

            sales_records.append({
                "invoice_no": row.InvoiceNo,
                "product_id": int(row.product_id),
                "customer_id": customer_id,
                "invoice_date": row.InvoiceDate.to_pydatetime(),
                "quantity": int(row.Quantity),
                "unit_price": float(row.UnitPrice),
                "revenue": float(row.Revenue),
                "country": row.Country
            })

        connection.execute(
            Sale.__table__.insert(),
            sales_records
        )

        total_sales += len(sales_records)

        print("Sales imported:", total_sales)

print("\nAll data imported successfully!")
