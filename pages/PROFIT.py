# ============================================================================
# PROFIT ANALYSIS PAGE - Streamlit Dashboard
# ============================================================================
# This page provides comprehensive profit analysis with visualizations,
# filters, and KPIs for sales data
# ============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# Configure page settings
st.set_page_config(page_title="Profit Analysis", layout="wide")

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
st.title("Profit Analysis")
st.write("This page analyzes profit trends by date, month, year, category, region, and segment.")

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

# Year Filter
with filter_col1:
    if "Year" in df.columns:
        selected_year = st.multiselect(
            "Select Year",
            options=sorted(df["Year"].dropna().unique()),
            default=sorted(df["Year"].dropna().unique())
        )
    else:
        selected_year = []

# Region Filter
with filter_col2:
    if "Region" in df.columns:
        selected_region = st.multiselect(
            "Select Region",
            options=df["Region"].dropna().unique(),
            default=df["Region"].dropna().unique()
        )
    else:
        selected_region = []

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

# Sub-Category Filter
with filter_col5:
    if "Sub-Category" in df.columns:
        selected_sub_category = st.multiselect(
            "Select Sub-Category",
            options=df["Sub-Category"].dropna().unique(),
            default=df["Sub-Category"].dropna().unique()
        )
    else:
        selected_sub_category = []

# ============================================================================
# APPLY FILTERS TO DATAFRAME
# ============================================================================
filtered_df = df.copy()

if "Year" in filtered_df.columns and selected_year:
    filtered_df = filtered_df[filtered_df["Year"].isin(selected_year)]

if "Region" in filtered_df.columns and selected_region:
    filtered_df = filtered_df[filtered_df["Region"].isin(selected_region)]

if "Category" in filtered_df.columns and selected_category:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_category)]

if "Segment" in filtered_df.columns and selected_segment:
    filtered_df = filtered_df[filtered_df["Segment"].isin(selected_segment)]

if "Sub-Category" in filtered_df.columns and selected_sub_category:
    filtered_df = filtered_df[filtered_df["Sub-Category"].isin(selected_sub_category)]

# ============================================================================
# KEY PERFORMANCE INDICATORS (KPIs)
# ============================================================================
st.subheader("Key Metrics")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# Total Profit KPI
with kpi1:
    if "Profit" in filtered_df.columns:
        st.metric("Total Profit", f"{filtered_df['Profit'].sum():,.2f}")

# Profit Margin % KPI
with kpi2:
    if "Sales" in filtered_df.columns and "Profit" in filtered_df.columns:
        profit_margin = (filtered_df['Profit'].sum() / filtered_df['Sales'].sum() * 100) if filtered_df['Sales'].sum() != 0 else 0
        st.metric("Profit Margin %", f"{profit_margin:.2f}%")

# Average Profit KPI
with kpi3:
    if "Profit" in filtered_df.columns:
        avg_profit = filtered_df['Profit'].mean()
        st.metric("Average Profit", f"{avg_profit:,.2f}")

# Total Orders Count KPI
with kpi4:
    if "Profit" in filtered_df.columns:
        st.metric("Total Orders", len(filtered_df))

# ============================================================================
# PROFIT VISUALIZATIONS
# ============================================================================

# Monthly Profit Trend - Line chart
st.subheader("Monthly Profit Trend")

if "Year Month" in filtered_df.columns and "Profit" in filtered_df.columns:
    monthly_profit = filtered_df.groupby("Year Month", as_index=False)["Profit"].sum()

    fig1 = px.line(
        monthly_profit,
        x="Year Month",
        y="Profit",
        markers=True,
        title="Monthly Profit Trend"
    )

    st.plotly_chart(fig1, use_container_width=True)

# Yearly Profit Trend - Bar chart
st.subheader("Yearly Profit Trend")

if "Year" in filtered_df.columns and "Profit" in filtered_df.columns:
    yearly_profit = filtered_df.groupby("Year", as_index=False)["Profit"].sum()

    fig2 = px.bar(
        yearly_profit,
        x="Year",
        y="Profit",
        text_auto=True,
        title="Yearly Profit Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Month Wise Profit Comparison - Bar chart sorted by month
st.subheader("Month Wise Profit Comparison")

if "Month" in filtered_df.columns and "Month Number" in filtered_df.columns and "Profit" in filtered_df.columns:
    month_profit = filtered_df.groupby(
        ["Month Number", "Month"],
        as_index=False
    )["Profit"].sum()

    # Sort by month number to ensure chronological order
    month_profit = month_profit.sort_values("Month Number")

    fig3 = px.bar(
        month_profit,
        x="Month",
        y="Profit",
        text_auto=True,
        title="Month Wise Profit Comparison"
    )

    st.plotly_chart(fig3, use_container_width=True)

# Category Wise Profit - Pie chart for profit distribution
st.subheader("Category Wise Profit")

if "Category" in filtered_df.columns and "Profit" in filtered_df.columns:
    category_profit = filtered_df.groupby("Category", as_index=False)["Profit"].sum()

    fig4 = px.pie(
        category_profit,
        names="Category",
        values="Profit",
        title="Category Wise Profit Distribution"
    )

    st.plotly_chart(fig4, use_container_width=True)

# Region Wise Profit - Bar chart showing profit by region
st.subheader("Region Wise Profit")

if "Region" in filtered_df.columns and "Profit" in filtered_df.columns:
    region_profit = filtered_df.groupby("Region", as_index=False)["Profit"].sum()

    fig5 = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        text_auto=True,
        title="Region Wise Profit"
    )

    st.plotly_chart(fig5, use_container_width=True)

# Segment Wise Profit Trend - Area chart showing profit by segment over time
st.subheader("Segment Wise Profit Trend")

if "Year Month" in filtered_df.columns and "Segment" in filtered_df.columns and "Profit" in filtered_df.columns:
    segment_profit = filtered_df.groupby(
        ["Year Month", "Segment"],
        as_index=False
    )["Profit"].sum()

    fig6 = px.area(
        segment_profit,
        x="Year Month",
        y="Profit",
        color="Segment",
        title="Segment Wise Profit Trend"
    )

    st.plotly_chart(fig6, use_container_width=True)

# Sub-Category Wise Profit - Horizontal bar chart for easy comparison
st.subheader("Profit by Sub-Category")

if "Sub-Category" in filtered_df.columns and "Profit" in filtered_df.columns:
    sub_category_profit = filtered_df.groupby("Sub-Category", as_index=False)["Profit"].sum()
    # Sort in ascending order for better visualization
    sub_category_profit = sub_category_profit.sort_values("Profit", ascending=True)

    fig7 = px.bar(
        sub_category_profit,
        y="Sub-Category",
        x="Profit",
        text_auto=True,
        title="Sub-Category Wise Profit",
        orientation='h'
    )

    st.plotly_chart(fig7, use_container_width=True)

# Sales vs Profit Relationship - Scatter plot to identify correlation
st.subheader("Sales vs Profit Relationship")

if "Sales" in filtered_df.columns and "Profit" in filtered_df.columns:
    fig8 = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        color="Category" if "Category" in filtered_df.columns else None,
        title="Sales vs Profit Relationship"
    )

    st.plotly_chart(fig8, use_container_width=True)

# ============================================================================
# SUMMARY TABLE AND DOWNLOAD
# ============================================================================

# Profit Summary Table - Detailed breakdown by month
st.subheader("Profit Summary Table")

if "Year Month" in filtered_df.columns:
    summary_table = filtered_df.groupby(
        "Year Month",
        as_index=False
    ).agg({
        "Profit": "sum",
        "Sales": "sum"
    })
        # Calculate profit margin percentage    # Calculate profit margin percentage
    summary_table["Profit Margin %"] = (summary_table["Profit"] / summary_table["Sales"] * 100).round(2)

    st.dataframe(summary_table, use_container_width=True)

# Download Button - Export filtered data as CSV
st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Profit Analysis Data",
    data=csv,
    file_name="profit_analysis_filtered_data.csv",
    mime="text/csv"
)
