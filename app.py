
import streamlit as st
import pandas as pd

# Load cleaned dataset
df = pd.read_csv("ecommerce_sales_cleaned.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

# Title
st.title("🛒 E-commerce Sales & Customer Insights Dashboard")

st.write("Sales, customer, category, regional and delivery performance analysis.")

# KPIs
total_revenue = df["revenue"].sum()
total_orders = df["order_id"].nunique()
total_customers = df["customer_id"].nunique()
aov = total_revenue / total_orders

customer_orders = df.groupby("customer_id")["order_id"].nunique()
repeat_customers = (customer_orders > 1).sum()
repeat_rate = repeat_customers / total_customers * 100

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Customers", f"{total_customers:,}")
col4.metric("Average Order Value", f"₹{aov:,.2f}")
col5.metric("Repeat Customer Rate", f"{repeat_rate:.2f}%")

st.divider()

# Monthly Revenue
st.subheader("📈 Monthly Revenue Trend")

monthly_revenue = df.groupby(
    df["order_date"].dt.to_period("M")
)["revenue"].sum()

monthly_revenue.index = monthly_revenue.index.astype(str)

st.line_chart(monthly_revenue)

# Category Performance
st.subheader("🛍️ Revenue by Product Category")

category_revenue = df.groupby("product_category")["revenue"].sum()

st.bar_chart(category_revenue)

# Regional Performance
st.subheader("🌍 Revenue by Region")

region_revenue = df.groupby("region")["revenue"].sum()

st.bar_chart(region_revenue)

# Customer Segmentation
st.subheader("👥 Customer Segmentation")

customer_analysis = df.groupby("customer_id").agg(
    Orders=("order_id", "nunique"),
    Total_Revenue=("revenue", "sum")
)

q25 = customer_analysis["Total_Revenue"].quantile(0.25)
q75 = customer_analysis["Total_Revenue"].quantile(0.75)

def segment_customer(revenue):
    if revenue <= q25:
        return "Low Value"
    elif revenue <= q75:
        return "Medium Value"
    else:
        return "High Value"

customer_analysis["Customer_Segment"] = (
    customer_analysis["Total_Revenue"].apply(segment_customer)
)

segment_counts = customer_analysis["Customer_Segment"].value_counts()

st.bar_chart(segment_counts)

# Delivery Performance
st.subheader("🚚 Delivery Days vs Customer Rating")

delivery_rating = df.groupby("delivery_days")["customer_rating"].mean()

st.line_chart(delivery_rating)
