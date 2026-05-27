import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visualization & Statistics", layout="wide")

@st.cache_data
def read_excel(file):
    return pd.read_excel(file)

df = read_excel("data/sales.xls")
df.columns = df.columns.str.strip()

st.title("Visualization and Descriptive Statistics")
st.write("Select analysis type, chart type, and columns from dropdowns to generate results.")

# Date conversion
if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()
    df["Year Month"] = df["Order Date"].dt.to_period("M").astype(str)

# Column types
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
all_cols = df.columns.tolist()

# Main dropdown
analysis_type = st.selectbox(
    "Select Analysis Type",
    [
        "Dataset Overview",
        "Descriptive Statistics",
        "Univariate Analysis",
        "Bivariate Analysis",
        "Correlation Analysis",
        "Missing Value Analysis"
    ]
)

# Dataset Overview
if analysis_type == "Dataset Overview":
    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Rows", df.shape[0])

    with col2:
        st.metric("Total Columns", df.shape[1])

    with col3:
        st.metric("Duplicate Rows", df.duplicated().sum())

    st.dataframe(df.head(), use_container_width=True)

# Descriptive Statistics
elif analysis_type == "Descriptive Statistics":
    st.subheader("Descriptive Statistics")

    stat_type = st.selectbox(
        "Select Statistics Type",
        ["Numeric Summary", "Categorical Summary", "Complete Summary"]
    )

    if stat_type == "Numeric Summary":
        st.dataframe(df[numeric_cols].describe(), use_container_width=True)

    elif stat_type == "Categorical Summary":
        st.dataframe(df[categorical_cols].describe(), use_container_width=True)

    elif stat_type == "Complete Summary":
        st.dataframe(df.describe(include="all"), use_container_width=True)

# Univariate Analysis
elif analysis_type == "Univariate Analysis":
    st.subheader("Univariate Analysis")

    column = st.selectbox("Select Column", all_cols)

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Histogram",
            "Box Plot",
            "Bar Chart",
            "Pie Chart",
            "Value Counts Table"
        ]
    )

    if chart_type == "Histogram":
        if column in numeric_cols:
            fig = px.histogram(df, x=column, nbins=30, title=f"Histogram of {column}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Histogram works best with numeric columns.")

    elif chart_type == "Box Plot":
        if column in numeric_cols:
            fig = px.box(df, y=column, title=f"Box Plot of {column}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Box plot works only with numeric columns.")

    elif chart_type == "Bar Chart":
        value_count = df[column].value_counts().reset_index()
        value_count.columns = [column, "Count"]

        fig = px.bar(
            value_count.head(20),
            x=column,
            y="Count",
            text_auto=True,
            title=f"Bar Chart of {column}"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pie Chart":
        value_count = df[column].value_counts().reset_index()
        value_count.columns = [column, "Count"]

        fig = px.pie(
            value_count.head(10),
            names=column,
            values="Count",
            title=f"Pie Chart of {column}"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Value Counts Table":
        value_count = df[column].value_counts().reset_index()
        value_count.columns = [column, "Count"]
        st.dataframe(value_count, use_container_width=True)

# Bivariate Analysis
elif analysis_type == "Bivariate Analysis":
    st.subheader("Bivariate Analysis")

    x_col = st.selectbox("Select X Column", all_cols)
    y_col = st.selectbox("Select Y Column", all_cols)

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Scatter Plot",
            "Line Chart",
            "Bar Chart",
            "Box Plot",
            "Grouped Bar Chart"
        ]
    )

    if chart_type == "Scatter Plot":
        if x_col in numeric_cols and y_col in numeric_cols:
            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                title=f"{x_col} vs {y_col}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Scatter plot requires both X and Y columns to be numeric.")

    elif chart_type == "Line Chart":
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            title=f"Line Chart: {x_col} vs {y_col}"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar Chart":
        grouped_data = df.groupby(x_col, as_index=False)[y_col].sum()

        fig = px.bar(
            grouped_data.head(30),
            x=x_col,
            y=y_col,
            text_auto=True,
            title=f"{x_col} wise {y_col}"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box Plot":
        if y_col in numeric_cols:
            fig = px.box(
                df,
                x=x_col,
                y=y_col,
                title=f"{y_col} Distribution by {x_col}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Y column must be numeric for box plot.")

    elif chart_type == "Grouped Bar Chart":
        color_col = st.selectbox("Select Group Column", categorical_cols)

        if y_col in numeric_cols:
            grouped_data = df.groupby(
                [x_col, color_col],
                as_index=False
            )[y_col].sum()

            fig = px.bar(
                grouped_data,
                x=x_col,
                y=y_col,
                color=color_col,
                barmode="group",
                title=f"{x_col} wise {y_col} grouped by {color_col}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Y column must be numeric.")

# Correlation Analysis
elif analysis_type == "Correlation Analysis":
    st.subheader("Correlation Analysis")

    corr = df[numeric_cols].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Heatmap"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(corr, use_container_width=True)

# Missing Value Analysis
elif analysis_type == "Missing Value Analysis":
    st.subheader("Missing Value Analysis")

    missing_df = df.isnull().sum().reset_index()
    missing_df.columns = ["Column", "Missing Values"]
    missing_df = missing_df[missing_df["Missing Values"] > 0]

    if missing_df.empty:
        st.success("No missing values found in the dataset.")
    else:
        fig = px.bar(
            missing_df,
            x="Column",
            y="Missing Values",
            text_auto=True,
            title="Missing Values by Column"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(missing_df, use_container_width=True)