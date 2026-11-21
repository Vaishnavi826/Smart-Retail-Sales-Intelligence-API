
from sqlalchemy import (
    Column, Integer, String, Float,
    DateTime, ForeignKey
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Products table
class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    stock_code = Column(String(50), unique=True, nullable=False)
    description = Column(String(500))


# Customers table
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    country = Column(String(100))


# Sales table
class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    invoice_no = Column(String(30), nullable=False)

    product_id = Column(
        Integer, ForeignKey("products.product_id"), nullable=False
    )

    customer_id = Column(
        Integer, ForeignKey("customers.customer_id"), nullable=True
    )

    invoice_date = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)
    country = Column(String(100))

