#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import neccessary Libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# # Data Loading and Inspection

# In[5]:


# Load the dataset

superstore_data = pd.read_csv('C:/Users/DELL/OneDrive/Desktop/Brainwave_Intern/Superstore.csv', encoding='ISO-8859-1')
pd.set_option('display.max_columns', None)   # To display total columns
superstore_data


# In[7]:


# Basic Insepction

superstore_data.info()
print('-------------------------------------------------------------------------')
superstore_data.describe()


# # Data Cleaning and Transformation

# In[10]:


# Check for missing values

superstore_data.isnull().sum()


# # Preprocess Data

# In[13]:


superstore_data['Order Date'] = pd.to_datetime(superstore_data['Order Date'])
superstore_data['Month-Year'] = superstore_data['Order Date'].dt.to_period('M').astype(str)
superstore_data.head()


# # Streamlit setup

# In[16]:


st.title('Superstore Sales Dashboard')
st.sidebar.header('Dashboard Filters')


# In[18]:


# Sidebar filters

category_filter = st.sidebar.multiselect('Select Category', superstore_data['Category'].unique(),superstore_data['Category'].unique())
segment_filter = st.sidebar.multiselect('Select Segment', superstore_data['Segment'].unique(),superstore_data['Segment'].unique())
shipmode_filter = st.sidebar.multiselect('Select Ship Mode',superstore_data['Ship Mode'].unique(),superstore_data['Ship Mode'].unique())
country_filter = st.sidebar.multiselect('Select Country',superstore_data['Country'].unique(),superstore_data['Country'].unique())


# In[20]:


# Filter data

filtered_data = superstore_data[(superstore_data['Category'].isin(category_filter)) & (superstore_data['Segment'].isin(segment_filter))
& (superstore_data['Ship Mode'].isin(shipmode_filter)) & (superstore_data['Country'].isin(country_filter))]


# # KPI metrics

# In[23]:


# Total Sales

total_sales = filtered_data['Sales'].sum()
print(f'Sales: ${total_sales:,.2f}')


# In[25]:


# Total Profit

total_profit = filtered_data['Profit'].sum()
print(f'Profit: ${total_profit:,.2f}')


# In[27]:


# Total Orders

total_orders = filtered_data['Order ID'].nunique()
print(f'Order ID:{total_orders:,.2f}')


# In[29]:


# Add KPI metrics values to metrics labels

st.metric(label='Total Sales', value=f'${total_sales:,.2f}')
st.metric(label='Total Profit',value=f'${total_profit:,.2f}')
st.metric(label='Total Orders',value=total_orders)


# # Sales & Profit by category

# In[32]:


st.subheader('Sales & Profit by Category')
category_data = filtered_data.groupby('Category')[['Sales','Profit']].sum().reset_index()
fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(data=category_data.melt(id_vars='Category'), x='Category', y='value', hue='variable', palette='pastel', ax=ax)
st.pyplot(fig)
#plt.show()


# # Top 10 states by sales

# In[39]:


st.subheader('Top 10 States by Sales')
state_sales = filtered_data.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(x=state_sales.values, y=state_sales.index, palette='viridis', ax=ax)
ax.set_xlabel('Sales ($)')
ax.set_ylabel('State')
st.pyplot(fig)
plt.show()


# # Monthly sales trend

# In[42]:


st.subheader('Monthly Sales Trend')
monthly_sales = filtered_data.groupby('Month-Year')['Sales'].sum().reset_index()
fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(data=monthly_sales, x='Month-Year', y='Sales', marker='o', color='royalblue', ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)
plt.show()


# # Profit by category & sub-category

# In[45]:


st.subheader('Profit by Category & Sub-Category')
profit_pivot = filtered_data.pivot_table(values='Profit', index='Category',columns='Sub-Category',aggfunc='sum')
fig, ax = plt.subplots(figsize=(15,10))
sns.heatmap(profit_pivot,annot=True, fmt='.0f', cmap='RdYlGn', linewidths=0.5, ax=ax)
st.pyplot(fig)
plt.show()


# In[ ]:




