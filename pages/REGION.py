# ============================================================================
# REGION ANALYSIS PAGE - Streamlit Dashboard
# ============================================================================
# This page provides comprehensive regional analysis with visualizations,
# filters, and performance metrics for sales data by region
# ============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# Configure page settings
st.set_page_config(page_title="Region Analysis", layout="wide")

# ============================================================================
# DATA LOADING AND PREPARATION
# ============================================================================

@st.cache_data
def read_excel(file):
    """Load Excel file and cache it for performance optimization"""
    df = pd.read_excel(file)
    return df

# Load sales data
df = read_excel("data/sales.xls")
# Remove leading/trailing whitespace from column names
df.columns = df.columns.str.strip()

# Page title and description
st.title("Region Analysis")
st.write("This page analyzes regional sales and profit trends by date, month, year, category, and segment.")

# Parse and create date-related features
if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Year"] = df["Order Date"].dt.year  # Extract year
    df["Month"] = df["Order Date"].dt.month_name()  # Extract month name
    df["Month Number"] = df["Order Date"].dt.month  # Extract month number
    df["Year Month"] = df["Order Date"].dt.to_period("M").astype(str)  # Create year-month period

# ============================================================================
# DATASET OVERVIEW - Display summary statistics
# ============================================================================
st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rows", df.shape[0])

with col2:
    st.metric("Total Columns", df.shape[1])

with col3:
    st.metric("Total Records", len(df))

# Display first 5 rows of dataset
st.dataframe(df.head(), use_container_width=True)

# ============================================================================
# INTERACTIVE FILTERS - Allow users to filter data by multiple criteria
# ============================================================================
st.subheader("Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

# Region Filter (primary filter for this page)
with filter_col1:
    if "Region" in df.columns:
        selected_region = st.multiselect(
            "Select Region",
            options=df["Region"].dropna().unique(),
            default=df["Region"].dropna().unique()
        )
    else:
        selected_region = []

# Year Filter
with filter_col2:
    if "Year" in df.columns:
        selected_year = st.multiselect(
            "Select Year",
            options=sorted(df["Year"].dropna().unique()),
            default=sorted(df["Year"].dropna().unique())
        )
    else:
        selected_year = []

# Category Filter
with filter_col3:
    if "Category" in df.columns:
        selected_category = st.multiselect(
            "Select Category",
            options=df["Category"].dropna().unique(),
            default=df["Category"].dropna().unique()
        )
    else:
        selected_category = []

filter_col4, filter_col5 = st.columns(2)

# Segment Filter
with filter_col4:
    if "Segment" in df.columns:
        selected_segment = st.multiselect(
            "Select Segment",
            options=df["Segment"].dropna().unique(),
            default=df["Segment"].dropna().unique()
        )
    else:
        selected_segment = []

# Ship Mode Filter
with filter_col5:
    if "Ship Mode" in df.columns:
        selected_ship_mode = st.multiselect(
            "Select Ship Mode",
            options=df["Ship Mode"].dropna().unique(),
            default=df["Ship Mode"].dropna().unique()
        )
    else:
        selected_ship_mode = []

# ============================================================================
# APPLY FILTERS TO DATAFRAME
# ============================================================================
filtered_df = df.copy()

if "Region" in filtered_df.columns and selected_region:
    filtered_df = filtered_df[filtered_df["Region"].isin(selected_region)]

if "Year" in filtered_df.columns and selected_year:
    filtered_df = filtered_df[filtered_df["Year"].isin(selected_year)]

if "Category" in filtered_df.columns and selected_category:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_category)]

if "Segment" in filtered_df.columns and selected_segment:
    filtered_df = filtered_df[filtered_df["Segment"].isin(selected_segment)]

if "Ship Mode" in filtered_df.columns and selected_ship_mode:
    filtered_df = filtered_df[filtered_df["Ship Mode"].isin(selected_ship_mode)]

# ============================================================================
# KEY PERFORMANCE INDICATORS (KPIs)
# ============================================================================
st.subheader("Key Metrics")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# Total Sales KPI
with kpi1:
    if "Sales" in filtered_df.columns:
        st.metric("Total Sales", f"{filtered_df['Sales'].sum():,.2f}")

# Total Profit KPI
with kpi2:
    if "Profit" in filtered_df.columns:
        st.metric("Total Profit", f"{filtered_df['Profit'].sum():,.2f}")

# Total Quantity KPI
with kpi3:
    if "Quantity" in filtered_df.columns:
        st.metric("Total Quantity", int(filtered_df["Quantity"].sum()))

# Number of Regions KPI
with kpi4:
    if "Region" in filtered_df.columns:
        st.metric("Total Regions", filtered_df["Region"].nunique())

# ============================================================================
# REGIONAL PERFORMANCE VISUALIZATIONS
# ============================================================================

# Region Wise Sales - Bar chart
st.subheader("Region Wise Sales")

if "Region" in filtered_df.columns and "Sales" in filtered_df.columns:
    region_sales = filtered_df.groupby("Region", as_index=False)["Sales"].sum()

    fig1 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        text_auto=True,
        title="Region Wise Sales"
    )

    st.plotly_chart(fig1, use_container_width=True)

# Region Wise Profit - Pie chart showing profit distribution
st.subheader("Region Wise Profit")

if "Region" in filtered_df.columns and "Profit" in filtered_df.columns:
    region_profit = filtered_df.groupby("Region", as_index=False)["Profit"].sum()

    fig2 = px.pie(
        region_profit,
        names="Region",
        values="Profit",
        title="Region Wise Profit Share"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Region Wise Sales and Profit - Grouped bar chart for comparison
st.subheader("Region Wise Sales and Profit")

if "Region" in filtered_df.columns and "Sales" in filtered_df.columns and "Profit" in filtered_df.columns:
    region_comparison = filtered_df.groupby("Region", as_index=False).agg({
        "Sales": "sum",
        "Profit": "sum"
    })

    fig3 = px.bar(
        region_comparison,
        x="Region",
        y=["Sales", "Profit"],
        barmode="group",
        title="Region Wise Sales and Profit Comparison"
    )

    st.plotly_chart(fig3, use_container_width=True)

# Region Monthly Sales Trend - Line chart showing sales trends over time
st.subheader("Region Monthly Sales Trend")

if "Year Month" in filtered_df.columns and "Region" in filtered_df.columns and "Sales" in filtered_df.columns:
    region_monthly_trend = filtered_df.groupby(
        ["Year Month", "Region"],
        as_index=False
    )["Sales"].sum()

    fig4 = px.line(
        region_monthly_trend,
        x="Year Month",
        y="Sales",
        color="Region",
        markers=True,
        title="Region Monthly Sales Trend"
    )

    st.plotly_chart(fig4, use_container_width=True)

# Region Monthly Profit Trend - Line chart showing profit trends over time
st.subheader("Region Monthly Profit Trend")

if "Year Month" in filtered_df.columns and "Region" in filtered_df.columns and "Profit" in filtered_df.columns:
    region_monthly_profit = filtered_df.groupby(
        ["Year Month", "Region"],
        as_index=False
    )["Profit"].sum()

    fig5 = px.line(
        region_monthly_profit,
        x="Year Month",
        y="Profit",
        color="Region",
        markers=True,
        title="Region Monthly Profit Trend"
    )

    st.plotly_chart(fig5, use_container_width=True)

# Category Performance by Region - Stacked bar chart
st.subheader("Category Performance by Region")

if "Region" in filtered_df.columns and "Category" in filtered_df.columns and "Sales" in filtered_df.columns:
    category_by_region = filtered_df.groupby(
        ["Region", "Category"],
        as_index=False
    )["Sales"].sum()

    fig6 = px.bar(
        category_by_region,
        x="Region",
        y="Sales",
        color="Category",
        barmode="stack",
        title="Category Performance by Region"
    )

    st.plotly_chart(fig6, use_container_width=True)

# Segment Performance by Region - Stacked bar chart
st.subheader("Segment Performance by Region")

if "Region" in filtered_df.columns and "Segment" in filtered_df.columns and "Sales" in filtered_df.columns:
    segment_by_region = filtered_df.groupby(
        ["Region", "Segment"],
        as_index=False
    )["Sales"].sum()

    fig7 = px.bar(
        segment_by_region,
        x="Region",
        y="Sales",
        color="Segment",
        barmode="stack",
        title="Segment Performance by Region"
    )

    st.plotly_chart(fig7, use_container_width=True)

# Region Quantity Analysis - Bar chart showing quantity sold by region
st.subheader("Region Quantity Analysis")

if "Region" in filtered_df.columns and "Quantity" in filtered_df.columns:
    region_quantity = filtered_df.groupby("Region", as_index=False)["Quantity"].sum()

    fig8 = px.bar(
        region_quantity,
        x="Region",
        y="Quantity",
        text_auto=True,
        title="Region Wise Quantity Sold"
    )

    st.plotly_chart(fig8, use_container_width=True)

# ============================================================================
# SUMMARY TABLE AND DOWNLOAD
# ============================================================================

# Region Performance Summary - Comprehensive metrics by region
st.subheader("Region Performance Summary")

if "Region" in filtered_df.columns:
    region_summary = filtered_df.groupby("Region", as_index=False).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Order ID": "nunique"
    })

    # Calculate profit margin percentage
    region_summary["Profit Margin %"] = (region_summary["Profit"] / region_summary["Sales"] * 100).round(2)
    # Rename for clarity
    region_summary = region_summary.rename(columns={"Order ID": "Total Orders"})

    st.dataframe(region_summary, use_container_width=True)

# Download Button - Export filtered data as CSV
st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Region Analysis Data",
    data=csv,
    file_name="region_analysis_filtered_data.csv",
    mime="text/csv"
)
