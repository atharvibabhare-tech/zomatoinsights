import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

# Page settings
st.set_page_config(page_title="Zomato Cost Analyzer", layout="wide")
st.title("🍽️ Zomato Dataset — Cost Analysis Dashboard")

# Load dataset
df = pd.read_csv("Zomato_Live.csv")

# Clean dataset
df = df.drop(['url','address','votes','phone','dish_liked','reviews_list',
              'menu_item','listed_in(type)','listed_in(city)'], axis=1)

df = df.rename(columns={'approx_cost(for two people)':'approx_cost'})
df = df.fillna(0)

df["approx_cost"] = df["approx_cost"].replace('[,]', '', regex=True).astype('int64')
df["rate"] = df["rate"].replace('[/5]', '', regex=True)
df["rate"] = df["rate"].replace(['NEW', '-'], 0).astype('float64')

df = df.drop(['online_order'], axis=1)

# Sidebar filters
st.sidebar.header("Filters")
location_list = sorted(df.location.unique())

selected_location = st.sidebar.selectbox("Select Location", location_list)

# Filter data
lo = df[df.location == selected_location]
gr = lo.groupby('name')['approx_cost'].mean().nlargest(10)

st.subheader(f"Top 10 Most Expensive Restaurants in **{selected_location}**")

# Plot
fig, ax = plt.subplots(figsize=(15, 6))
sb.barplot(x=gr.index, y=gr.values, palette='summer', ax=ax)
plt.xticks(rotation=90)
plt.ylabel("Average Cost (₹)")

st.pyplot(fig)

# Show data table if user wants
if st.checkbox("Show Raw Data"):
    st.dataframe(lo)
