import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

st.title("Zomato – Top 10 Costliest Restaurants by Location")

# Load dataset
df = pd.read_csv("Zomato_Live.csv")

# Show locations
locations = sorted(df.location.unique())
st.write("Available Locations:")
st.write(locations)

# Streamlit input (replaces input())
h = st.selectbox("Enter / Select Location Name:", locations)

# Filter data
lo = df[df.location == h]
gr = lo.groupby('name')['approx_cost'].mean().nlargest(10)

# Plot
fig = plt.figure(figsize=(20, 8))
sb.barplot(x=gr.index, y=gr.values, palette='summer')
plt.xticks(rotation=90)

st.pyplot(fig)
