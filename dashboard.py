
import streamlit as st
import requests
import pandas as pd


# -----------------------------------
# 1. Dashboard Configuration
# -----------------------------------

st.set_page_config(
    page_title="Smart Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"


# -----------------------------------
# 2. Dashboard Header
# -----------------------------------

st.title("📊 Smart Retail Sales Intelligence Dashboard")

st.write(
    "Analyze your retail sales performance "
    "and understand business trends."
)

st.divider()


# -----------------------------------
# 3. Fetch Data from FastAPI
# -----------------------------------

def fetch_data(endpoint):

    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:

        st.error(f"Unable to fetch {endpoint}: {error}")

        return None


# -----------------------------------
# 4. CSV Download Helper
# -----------------------------------

def download_csv(dataframe, button_label, file_name):

    csv_data = dataframe.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=button_label,
        data=csv_data,
        file_name=file_name,
        mime="text/csv"
    )


# -----------------------------------
# 5. Fetch Analytics Data
# -----------------------------------

revenue_data = fetch_data("/analytics/total-revenue")

orders_data = fetch_data("/analytics/total-orders")

aov_data = fetch_data("/analytics/average-order-value")

monthly_data = fetch_data("/analytics/monthly-revenue")

growth_data = fetch_data("/analytics/sales-growth")

yearly_data = fetch_data("/analytics/yearly-revenue")

products_data = fetch_data("/analytics/top-products")

country_data = fetch_data("/analytics/country-sales")

customers_data = fetch_data("/analytics/top-customers")


# -----------------------------------
# 6. Business Overview - KPI Cards
# -----------------------------------

st.header("📈 Business Overview")

if all(data is not None for data in [
    revenue_data,
    orders_data,
    aov_data
]):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Revenue",
            value=f"£{revenue_data['total_revenue']:,.2f}"
        )

    with col2:
        st.metric(
            label="Total Orders",
            value=f"{orders_data['total_orders']:,}"
        )

    with col3:
        st.metric(
            label="Average Order Value",
            value=f"£{aov_data['average_order_value']:,.2f}"
        )

else:
    st.warning("Unable to load all business overview metrics.")


st.divider()


# -----------------------------------
# 7. Monthly Revenue Analysis
# -----------------------------------

st.header("📅 Monthly Revenue Analysis")

if monthly_data is not None and len(monthly_data) > 0:

    monthly_df = pd.DataFrame(monthly_data)

    monthly_df["month"] = pd.to_datetime(
        monthly_df["month"]
    )

    monthly_df = monthly_df.sort_values("month")

    monthly_df = monthly_df.set_index("month")

    min_date = monthly_df.index.min().date()
    max_date = monthly_df.index.max().date()

    selected_dates = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:

        start_date, end_date = selected_dates

        filtered_monthly_df = monthly_df.loc[
            (monthly_df.index >= pd.Timestamp(start_date)) &
            (monthly_df.index <= pd.Timestamp(end_date))
        ]

        if not filtered_monthly_df.empty:

            st.line_chart(
                filtered_monthly_df["total_revenue"],
                x_label="Month",
                y_label="Revenue (£)"
            )

            monthly_download_df = filtered_monthly_df.reset_index()

            download_csv(
                monthly_download_df,
                "📥 Download Monthly Revenue Report",
                "monthly_revenue_report.csv"
            )

        else:
            st.info("No revenue data available for this date range.")

    else:
        st.info("Please select both a start date and an end date.")

else:
    st.info("No monthly revenue data available.")


st.divider()


# -----------------------------------
# 8. Monthly Sales Growth Analysis
# -----------------------------------

st.header("📈 Monthly Sales Growth Analysis")

if growth_data is not None and len(growth_data) > 0:

    growth_df = pd.DataFrame(growth_data)

    growth_df = growth_df.dropna(
        subset=["growth_percentage"]
    )

    if not growth_df.empty:

        growth_df["month"] = pd.to_datetime(
            growth_df["month"]
        )

        growth_df = growth_df.sort_values("month")

        growth_chart_df = growth_df.set_index("month")

        st.line_chart(
            growth_chart_df["growth_percentage"],
            x_label="Month",
            y_label="Growth (%)"
        )

        st.subheader("Monthly Growth Details")

        st.dataframe(
            growth_df,
            use_container_width=True,
            hide_index=True
        )

        download_csv(
            growth_df,
            "📥 Download Sales Growth Report",
            "sales_growth_report.csv"
        )

    else:
        st.info("Not enough monthly data to calculate growth.")

else:
    st.info("No sales growth data available.")


st.divider()


# -----------------------------------
# 9. Year-wise Revenue Analysis
# -----------------------------------

st.header("📆 Year-wise Revenue Analysis")

if yearly_data is not None and len(yearly_data) > 0:

    yearly_df = pd.DataFrame(yearly_data)

    yearly_df = yearly_df.sort_values("year")

    yearly_df["year"] = yearly_df["year"].astype(str)

    yearly_chart_df = yearly_df.set_index("year")

    st.bar_chart(
        yearly_chart_df["total_revenue"],
        x_label="Year",
        y_label="Revenue (£)"
    )

    st.subheader("Yearly Revenue Details")

    st.dataframe(
        yearly_df,
        use_container_width=True,
        hide_index=True
    )

    download_csv(
        yearly_df,
        "📥 Download Yearly Revenue Report",
        "yearly_revenue_report.csv"
    )

else:
    st.info("No yearly revenue data available.")


st.divider()


# -----------------------------------
# 10. Top 10 Best-Selling Products
# -----------------------------------

st.header("🏆 Top 10 Best-Selling Products")

if products_data is not None and len(products_data) > 0:

    products_df = pd.DataFrame(products_data)

    products_df = products_df.sort_values(
        "total_quantity_sold",
        ascending=False
    )

    if "product_name" in products_df.columns:
        products_chart_df = products_df.set_index("product_name")
    else:
        products_df["product_id"] = products_df["product_id"].astype(str)
        products_chart_df = products_df.set_index("product_id")

    st.bar_chart(
        products_chart_df["total_quantity_sold"],
        x_label="Product",
        y_label="Quantity Sold"
    )

    st.subheader("Product Sales Details")

    st.dataframe(
        products_df,
        use_container_width=True,
        hide_index=True
    )

    download_csv(
        products_df,
        "📥 Download Product Sales Report",
        "top_products_report.csv"
    )

else:
    st.info("No product data available.")


st.divider()


# -----------------------------------
# 11. Country-wise Sales Analysis
# -----------------------------------

st.header("🌍 Country-wise Sales Analysis")

if country_data is not None and len(country_data) > 0:

    country_df = pd.DataFrame(country_data)

    countries = sorted(
        country_df["country"].dropna().unique().tolist()
    )

    selected_country = st.selectbox(
        "Select a Country",
        ["All Countries"] + countries
    )

    if selected_country == "All Countries":

        filtered_country_df = country_df.copy()

    else:

        filtered_country_df = country_df[
            country_df["country"] == selected_country
        ]

    st.subheader("Revenue by Country")

    country_chart_df = filtered_country_df.sort_values(
        "total_revenue",
        ascending=False
    )

    country_chart_df = country_chart_df.set_index("country")

    st.bar_chart(
        country_chart_df["total_revenue"],
        x_label="Country",
        y_label="Revenue (£)"
    )

    st.subheader("Country Sales Details")

    country_details_df = filtered_country_df.sort_values(
        "total_revenue",
        ascending=False
    )

    st.dataframe(
        country_details_df,
        use_container_width=True,
        hide_index=True
    )

    download_csv(
        country_details_df,
        "📥 Download Country Sales Report",
        "country_sales_report.csv"
    )

else:
    st.info("No country-wise sales data available.")


st.divider()


# -----------------------------------
# 12. Top 10 Customers Analysis
# -----------------------------------

st.header("👥 Top 10 Customers Analysis")

if customers_data is not None and len(customers_data) > 0:

    customers_df = pd.DataFrame(customers_data)

    customers_df = customers_df.sort_values(
        "total_revenue",
        ascending=False
    )

    st.subheader("Customer Revenue Chart")

    customers_chart_df = customers_df.copy()

    customers_chart_df["customer_id"] = (
        customers_chart_df["customer_id"].astype(str)
    )

    customers_chart_df = customers_chart_df.set_index(
        "customer_id"
    )

    st.bar_chart(
        customers_chart_df["total_revenue"],
        x_label="Customer ID",
        y_label="Revenue (£)"
    )

    st.subheader("Customer Sales Details")

    st.dataframe(
        customers_df,
        use_container_width=True,
        hide_index=True
    )

    download_csv(
        customers_df,
        "📥 Download Customer Sales Report",
        "top_customers_report.csv"
    )

else:
    st.info("No customer data available.")


# -----------------------------------
# 13. Dashboard Footer
# -----------------------------------

st.divider()

st.caption(
    "Smart Retail Sales Intelligence API | "
    "Built using Python, FastAPI, PostgreSQL and Streamlit"
)
