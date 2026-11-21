
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Sale, Product

router = APIRouter(
    prefix="/analytics",
    tags=["Sales Analytics"]
)


# 1. GET Total Revenue
@router.get("/total-revenue")
def get_total_revenue(
    db: Session = Depends(get_db)
):
    total_revenue = db.query(
        func.sum(Sale.revenue)
    ).scalar()

    return {
        "total_revenue": round(total_revenue or 0, 2)
    }


# 2. GET Total Orders
@router.get("/total-orders")
def get_total_orders(
    db: Session = Depends(get_db)
):
    total_orders = db.query(
        func.count(func.distinct(Sale.invoice_no))
    ).scalar()

    return {
        "total_orders": total_orders or 0
    }


# 3. GET Top 10 Best-Selling Products
@router.get("/top-products")
def get_top_products(
    db: Session = Depends(get_db)
):
    top_products = (
        db.query(
            Product.product_id,
            Product.description,
            func.sum(Sale.quantity).label("total_quantity")
        )
        .join(
            Sale,
            Sale.product_id == Product.product_id
        )
        .group_by(
            Product.product_id,
            Product.description
        )
        .order_by(
            func.sum(Sale.quantity).desc()
        )
        .limit(10)
        .all()
    )

    return [
        {
            "product_id": product_id,
            "product_name": description,
            "total_quantity_sold": int(total_quantity)
        }
        for product_id, description, total_quantity in top_products
    ]

# 4. GET Monthly Revenue
@router.get("/monthly-revenue")
def get_monthly_revenue(
    db: Session = Depends(get_db)
):
    monthly_revenue = (
        db.query(
            func.to_char(
                Sale.invoice_date, "YYYY-MM"
            ).label("month"),
            func.sum(Sale.revenue).label("total_revenue")
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    return [
        {
            "month": month,
            "total_revenue": round(float(total_revenue or 0), 2)
        }
        for month, total_revenue in monthly_revenue
    ]

# 5. GET Country-wise Sales
@router.get("/country-sales")
def get_country_sales(
    db: Session = Depends(get_db)
):
    country_sales = (
        db.query(
            Sale.country,
            func.sum(Sale.revenue).label("total_revenue"),
            func.count(
                func.distinct(Sale.invoice_no)
            ).label("total_orders")
        )
        .group_by(Sale.country)
        .order_by(func.sum(Sale.revenue).desc())
        .all()
    )

    return [
        {
            "country": country,
            "total_revenue": round(float(revenue or 0), 2),
            "total_orders": orders
        }
        for country, revenue, orders in country_sales
    ]

# 6. GET Top 10 Customers
@router.get("/top-customers")
def get_top_customers(
    db: Session = Depends(get_db)
):
    top_customers = (
        db.query(
            Sale.customer_id,
            func.sum(Sale.revenue).label("total_revenue"),
            func.count(func.distinct(Sale.invoice_no)).label("total_orders")
        )
        .filter(Sale.customer_id.isnot(None))
        .group_by(Sale.customer_id)
        .order_by(func.sum(Sale.revenue).desc())
        .limit(10)
        .all()
    )

    return [
        {
            "customer_id": customer_id,
            "total_revenue": round(float(total_revenue), 2),
            "total_orders": total_orders
        }
        for customer_id, total_revenue, total_orders in top_customers
    ]

# 7. GET Monthly Orders
@router.get("/monthly-orders")
def get_monthly_orders(
    db: Session = Depends(get_db)
):
    monthly_orders = (
        db.query(
            func.to_char(Sale.invoice_date, "YYYY-MM").label("month"),
            func.count(func.distinct(Sale.invoice_no)).label("total_orders")
        )
        .group_by(
            func.to_char(Sale.invoice_date, "YYYY-MM")
        )
        .order_by(
            func.to_char(Sale.invoice_date, "YYYY-MM")
        )
        .all()
    )

    return [
        {
            "month": month,
            "total_orders": total_orders
        }
        for month, total_orders in monthly_orders
    ]

# 8. GET Average Order Value
@router.get("/average-order-value")
def get_average_order_value(
    db: Session = Depends(get_db)
):
    total_revenue = db.query(
        func.sum(Sale.revenue)
    ).scalar() or 0

    total_orders = db.query(
        func.count(func.distinct(Sale.invoice_no))
    ).scalar() or 0

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0 else 0
    )

    return {
        "average_order_value": round(float(average_order_value), 2)
    }

# 9. GET Year-wise Revenue
@router.get("/yearly-revenue")
def get_yearly_revenue(
    db: Session = Depends(get_db)
):
    yearly_revenue = (
        db.query(
            func.to_char(
                Sale.invoice_date, "YYYY"
            ).label("year"),
            func.sum(Sale.revenue).label("total_revenue")
        )
        .group_by("year")
        .order_by("year")
        .all()
    )

    return [
        {
            "year": year,
            "total_revenue": round(float(revenue or 0), 2)
        }
        for year, revenue in yearly_revenue
    ]

# 10. GET Monthly Sales Growth
@router.get("/sales-growth")
def get_sales_growth(
    db: Session = Depends(get_db)
):
    monthly_revenue = (
        db.query(
            func.to_char(
                Sale.invoice_date, "YYYY-MM"
            ).label("month"),
            func.sum(Sale.revenue).label("total_revenue")
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    results = []

    for i, (month, revenue) in enumerate(monthly_revenue):
        revenue = float(revenue or 0)

        if i == 0:
            growth = None
        else:
            previous_revenue = float(
                monthly_revenue[i - 1][1] or 0
            )

            growth = (
                ((revenue - previous_revenue) / previous_revenue) * 100
                if previous_revenue != 0 else None
            )

        results.append({
            "month": month,
            "total_revenue": round(revenue, 2),
            "growth_percentage": (
                round(growth, 2) if growth is not None else None
            )
        })

    return results
