import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------
df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
df["Order Date"] = pd.to_datetime(df["Order Date"])

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.title("🔍 Dashboard Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category))
]

# -----------------------------------
# TITLE
# -----------------------------------
st.title("📊 Sales & Revenue Analysis Dashboard")

st.write(
    "Interactive dashboard for analyzing sales performance, revenue trends, "
    "profitability, top-performing products, categories, and regional sales."
)

st.markdown("---")

# -----------------------------------
# KPI CARDS
# -----------------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Sales", f"${total_sales:,.0f}")

with col2:
    st.metric("📈 Total Profit", f"${total_profit:,.0f}")

with col3:
    st.metric("📦 Quantity Sold", f"{total_quantity:,}")

st.markdown("---")

# -----------------------------------
# MONTHLY REVENUE TREND
# -----------------------------------
monthly_sales = (
    filtered_df.groupby(
        filtered_df["Order Date"].dt.to_period("M")
    )["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

fig1 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    title="📈 Monthly Revenue Trend",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------
# TOP PRODUCTS & CATEGORY SALES
# -----------------------------------
left, right = st.columns(2)

with left:

    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="🏆 Top 10 Products by Revenue"
    )

    st.plotly_chart(fig2, use_container_width=True)

with right:

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="📊 Sales by Category"
    )

    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------
# REGION SALES
# -----------------------------------
region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="🌎 Sales by Region"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------
# KEY INSIGHTS
# -----------------------------------
st.subheader("📌 Key Insights")

top_product = top_products.iloc[0]["Product Name"]

st.write(f"🏆 Highest Revenue Product: **{top_product}**")
st.write(f"💰 Total Revenue Generated: **${total_sales:,.0f}**")
st.write(f"📈 Total Profit Earned: **${total_profit:,.0f}**")
st.write(f"📦 Total Quantity Sold: **{total_quantity:,} units**")

# -----------------------------------
# DATASET PREVIEW
# -----------------------------------
with st.expander("📄 View Dataset"):
    st.dataframe(filtered_df)