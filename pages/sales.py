import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Trend Analysis", layout="wide")

@st.cache_data
def read_excel(file):
    df = pd.read_excel(file)
    return df

df = read_excel("data/sales.xls")
df.columns = df.columns.str.strip()

st.title("Sales Trend Analysis")
st.write("This page analyzes sales trend by date, month, year, category, region, and segment.")

if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()
    df["Month Number"] = df["Order Date"].dt.month
    df["Year Month"] = df["Order Date"].dt.to_period("M").astype(str)

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rows", df.shape[0])

with col2:
    st.metric("Total Columns", df.shape[1])

with col3:
    st.metric("Total Records", len(df))

st.dataframe(df.head(), use_container_width=True)

st.subheader("Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    if "Year" in df.columns:
        selected_year = st.multiselect(
            "Select Year",
            options=sorted(df["Year"].dropna().unique()),
            default=sorted(df["Year"].dropna().unique())
        )
    else:
        selected_year = []

with filter_col2:
    if "Region" in df.columns:
        selected_region = st.multiselect(
            "Select Region",
            options=df["Region"].dropna().unique(),
            default=df["Region"].dropna().unique()
        )
    else:
        selected_region = []

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

with filter_col4:
    if "Segment" in df.columns:
        selected_segment = st.multiselect(
            "Select Segment",
            options=df["Segment"].dropna().unique(),
            default=df["Segment"].dropna().unique()
        )
    else:
        selected_segment = []

with filter_col5:
    if "Ship Mode" in df.columns:
        selected_ship_mode = st.multiselect(
            "Select Ship Mode",
            options=df["Ship Mode"].dropna().unique(),
            default=df["Ship Mode"].dropna().unique()
        )
    else:
        selected_ship_mode = []

filtered_df = df.copy()

if "Year" in filtered_df.columns and selected_year:
    filtered_df = filtered_df[filtered_df["Year"].isin(selected_year)]

if "Region" in filtered_df.columns and selected_region:
    filtered_df = filtered_df[filtered_df["Region"].isin(selected_region)]

if "Category" in filtered_df.columns and selected_category:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_category)]

if "Segment" in filtered_df.columns and selected_segment:
    filtered_df = filtered_df[filtered_df["Segment"].isin(selected_segment)]

if "Ship Mode" in filtered_df.columns and selected_ship_mode:
    filtered_df = filtered_df[filtered_df["Ship Mode"].isin(selected_ship_mode)]

st.subheader("Key Metrics")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    if "Sales" in filtered_df.columns:
        st.metric("Total Sales", f"{filtered_df['Sales'].sum():,.2f}")

with kpi2:
    if "Profit" in filtered_df.columns:
        st.metric("Total Profit", f"{filtered_df['Profit'].sum():,.2f}")

with kpi3:
    if "Quantity" in filtered_df.columns:
        st.metric("Total Quantity", int(filtered_df["Quantity"].sum()))

with kpi4:
    if "Order ID" in filtered_df.columns:
        st.metric("Total Orders", filtered_df["Order ID"].nunique())

st.subheader("Monthly Sales Trend")

if "Year Month" in filtered_df.columns and "Sales" in filtered_df.columns:
    monthly_sales = filtered_df.groupby("Year Month", as_index=False)["Sales"].sum()

    fig1 = px.line(
        monthly_sales,
        x="Year Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig1, use_container_width=True)

st.subheader("Yearly Sales Trend")

if "Year" in filtered_df.columns and "Sales" in filtered_df.columns:
    yearly_sales = filtered_df.groupby("Year", as_index=False)["Sales"].sum()

    fig2 = px.bar(
        yearly_sales,
        x="Year",
        y="Sales",
        text_auto=True,
        title="Yearly Sales Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Month Wise Sales Comparison")

if "Month" in filtered_df.columns and "Month Number" in filtered_df.columns and "Sales" in filtered_df.columns:
    month_sales = filtered_df.groupby(
        ["Month Number", "Month"],
        as_index=False
    )["Sales"].sum()

    month_sales = month_sales.sort_values("Month Number")

    fig3 = px.bar(
        month_sales,
        x="Month",
        y="Sales",
        text_auto=True,
        title="Month Wise Sales Comparison"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Category Wise Sales Trend")

if "Year Month" in filtered_df.columns and "Category" in filtered_df.columns and "Sales" in filtered_df.columns:
    category_trend = filtered_df.groupby(
        ["Year Month", "Category"],
        as_index=False
    )["Sales"].sum()

    fig4 = px.line(
        category_trend,
        x="Year Month",
        y="Sales",
        color="Category",
        markers=True,
        title="Category Wise Sales Trend"
    )

    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Region Wise Sales Trend")

if "Year Month" in filtered_df.columns and "Region" in filtered_df.columns and "Sales" in filtered_df.columns:
    region_trend = filtered_df.groupby(
        ["Year Month", "Region"],
        as_index=False
    )["Sales"].sum()

    fig5 = px.line(
        region_trend,
        x="Year Month",
        y="Sales",
        color="Region",
        markers=True,
        title="Region Wise Sales Trend"
    )

    st.plotly_chart(fig5, use_container_width=True)

st.subheader("Segment Wise Sales Trend")

if "Year Month" in filtered_df.columns and "Segment" in filtered_df.columns and "Sales" in filtered_df.columns:
    segment_trend = filtered_df.groupby(
        ["Year Month", "Segment"],
        as_index=False
    )["Sales"].sum()

    fig6 = px.area(
        segment_trend,
        x="Year Month",
        y="Sales",
        color="Segment",
        title="Segment Wise Sales Trend"
    )

    st.plotly_chart(fig6, use_container_width=True)

st.subheader("Sales and Profit Trend")

if "Year Month" in filtered_df.columns and "Sales" in filtered_df.columns and "Profit" in filtered_df.columns:
    sales_profit_trend = filtered_df.groupby(
        "Year Month",
        as_index=False
    )[["Sales", "Profit"]].sum()

    fig7 = px.line(
        sales_profit_trend,
        x="Year Month",
        y=["Sales", "Profit"],
        markers=True,
        title="Sales and Profit Trend"
    )

    st.plotly_chart(fig7, use_container_width=True)

st.subheader("Sales Trend Summary Table")

if "Year Month" in filtered_df.columns:
    summary_table = filtered_df.groupby(
        "Year Month",
        as_index=False
    ).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Order ID": "nunique"
    })

    summary_table = summary_table.rename(columns={"Order ID": "Total Orders"})

    st.dataframe(summary_table, use_container_width=True)

st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Sales Trend Data",
    data=csv,
    file_name="sales_trend_filtered_data.csv",
    mime="text/csv"
)