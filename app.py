import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

st.set_page_config(layout="wide")
st.title("🍽️ Zomato – Top Restaurants Cost Analysis")

# Load dataset
df = pd.read_csv("Zomato_Live.csv")

# Dropdown for location
locations = sorted(df.location.dropna().unique())
h = st.selectbox("Select Location:", locations)

# Correct slider (fix: min_value, max_value)
top_n = st.slider("Select Top N Restaurants", min_value=5, max_value=20, value=10)

# Filter data
lo = df[df.location == h]

# Group and take top N
gr = lo.groupby('name')['approx_cost'].mean().nlargest(top_n)

# Display information
st.subheader(f"Top {top_n} Most Expensive Restaurants in **{h}**")

# Plot
fig = plt.figure(figsize=(18, 7))
sb.barplot(x=gr.index, y=gr.values, palette='summer')
plt.xticks(rotation=90)
plt.ylabel("Average Cost (₹)")
plt.xlabel("Restaurants")

st.pyplot(fig)

# Optional: show raw data
if st.checkbox("Show Raw Data for Selected Location"):
    st.dataframe(lo)
