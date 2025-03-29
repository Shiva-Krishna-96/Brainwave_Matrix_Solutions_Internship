import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Setup ---
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

# --- Load Data ---
data = pd.read_csv('Task1/Superstore.csv',encoding='ISO-8859-1')
data['Order Date'] = pd.to_datetime(data['Order Date'])
data['Month'] = data['Order Date'].dt.to_period('M')

# --- Dashboard Title ---
st.title("📊 Superstore Sales Interactive Dashboard")

# --- Inline Filters (Top Row) ---
col_filter1, col_filter2, col_filter3 = st.columns(3)

region = col_filter1.multiselect("Select Region:", options=data['Region'].unique(), default=data['Region'].unique())
category = col_filter2.multiselect("Select Category:", options=data['Category'].unique(), default=data['Category'].unique())
segment = col_filter3.multiselect("Select Segment:", options=data['Segment'].unique(), default=data['Segment'].unique())

# --- Apply Filters ---
filtered_data = data[
    (data['Region'].isin(region)) &
    (data['Category'].isin(category)) &
    (data['Segment'].isin(segment))
]

# --- KPIs in One Row ---
col1, col2, col3 = st.columns(3)

total_sales = filtered_data['Sales'].sum()
total_profit = filtered_data['Profit'].sum()
total_orders = filtered_data['Order ID'].nunique()

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("📦 Total Orders", total_orders)

# --- Dashboard Layout (2x2 Grid of Charts) ---
col_chart1, col_chart2, col_chart3, col_chart4 = st.columns(4)

# Sales by Category Chart
with col_chart1:
    fig1, ax1 = plt.subplots(figsize=(4, 2))
    sns.barplot(data=filtered_data.groupby('Category')['Sales'].sum().reset_index(),
                x='Category', y='Sales', palette='viridis', ax=ax1)
    plt.title("Sales by Category")
    st.pyplot(fig1)

# Profit by Region Chart
with col_chart2:
    fig2, ax2 = plt.subplots(figsize=(4, 2))
    sns.barplot(data=filtered_data.groupby('Region')['Profit'].sum().reset_index(),
                x='Region', y='Profit', palette='coolwarm', ax=ax2)
    plt.title("Profit by Region")
    st.pyplot(fig2)

# Monthly Sales Trend
with col_chart3:
    monthly_sales = filtered_data.groupby('Month')['Sales'].sum()
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    monthly_sales.plot(marker='o', color='orange', ax=ax3)
    plt.title('Monthly Sales Trend')
    plt.ylabel('Sales ($)')
    plt.grid()
    st.pyplot(fig3)

# Top Customers by Sales
with col_chart4:
    top_customers = (
        filtered_data.groupby('Customer Name')
        .agg({'Sales': 'sum',})
        .sort_values(by='Sales', ascending=False)
        .head(10)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=top_customers, x='Customer Name', y='Sales', color='skyblue', ax=ax)
    plt.xticks(rotation=45)
    plt.title("Top 10 Customers by Sales")
    st.pyplot(fig)

col_chart5, col_chart6, col_chart7, col_chart8 = st.columns(4)
# Top Customers by Profit
with col_chart5:
    top_customers = (
        filtered_data.groupby('Customer Name')
        .agg({'Profit': 'sum'})
        .sort_values(by='Profit', ascending=False)
        .head(10)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=top_customers, x='Customer Name', y='Profit', color='skyblue', ax=ax)
    plt.xticks(rotation=45)
    plt.title("Top 10 Customers by Profit")
    st.pyplot(fig)

# Profit Margin by Category
with col_chart6:
    filtered_data['Profit Margin (%)'] = (filtered_data['Profit'] / filtered_data['Sales']) * 100
    category_margin = (
        filtered_data.groupby('Category')['Profit Margin (%)']
        .mean()
        .reset_index()
        .sort_values(by='Profit Margin (%)', ascending=False)
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=category_margin, x='Category', y='Profit Margin (%)', palette='RdYlGn', ax=ax)
    plt.title("Average Profit Margin by Category")
    st.pyplot(fig)

# Profit Margin by Region
with col_chart7:
    filtered_data['Profit Margin (%)'] = (filtered_data['Profit'] / filtered_data['Sales']) * 100
    region_margin = (
        filtered_data.groupby('Region')['Profit Margin (%)']
        .mean()
        .reset_index()
        .sort_values(by='Profit Margin (%)', ascending=False)
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=region_margin, x='Region', y='Profit Margin (%)', palette='RdYlGn', ax=ax)
    plt.title("Average Profit Margin by Region")
    st.pyplot(fig)

# Shipping Mode Analysis
with col_chart8:
    shipping_profit = filtered_data.groupby('Ship Mode')['Profit'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=shipping_profit, x='Ship Mode', y='Profit', palette='coolwarm', ax=ax)
    plt.title("Profit by Shipping Mode")
    st.pyplot(fig)


# Top 10 Profitable Products
st.subheader("Top 5 Profitable Products")
top_products = filtered_data.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(5).reset_index()
st.dataframe(top_products)

# --- Data Insights Section ---
st.write("### 🔥 Business Insights")
st.write(
    "- **Focus on top-performing regions** to maximize profits.\n"
    "- **Identify low-profit regions** for improvements.\n"
    "- **Track monthly trends** to predict future sales.\n"
    "- **Optimize high-profit products** and phase out low-margin items."
)

