import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Zomato Restaurant Dashboard",
    layout="wide",
    page_icon="🍽️"
)

st.title("🍽️ Zomato Restaurant Cost Analytics")
st.markdown("Explore top restaurants and analyze cost trends interactively.")

# -----------------------------
# LOAD DATA SAFELY
# -----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Zomato_Live.csv")
        return df
    except Exception as e:
        st.error(f"❌ Error loading dataset: {e}")
        st.stop()

df = load_data()

# -----------------------------
# DATA CLEANING
# -----------------------------
# Rename columns to safe format
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Fix cost column if needed
if "approx_cost(for_two_people)" in df.columns:
    df.rename(columns={"approx_cost(for_two_people)": "approx_cost"}, inplace=True)

if "approx_cost" in df.columns:
    df["approx_cost"] = (
        df["approx_cost"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["approx_cost"] = pd.to_numeric(df["approx_cost"], errors="coerce")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filter Options")

locations = sorted(df["location"].dropna().unique())
selected_location = st.sidebar.selectbox("Select Location", locations)

top_n = st.sidebar.slider("Select Top N Restaurants", 5, 20, 10)

# Filter data
filtered_df = df[df["location"] == selected_location]

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Key Insights")

col1, col2, col3 = st.columns(3)

col1.metric("Total Restaurants", filtered_df["name"].nunique())
col2.metric("Average Cost", f"₹ {int(filtered_df['approx_cost'].mean())}")
col3.metric("Max Cost", f"₹ {int(filtered_df['approx_cost'].max())}")

st.markdown("---")

# -----------------------------
# TOP EXPENSIVE RESTAURANTS
# -----------------------------
st.header(f"💎 Top {top_n} Most Expensive Restaurants in {selected_location}")

top_restaurants = (
    filtered_df.groupby("name")["approx_cost"]
    .mean()
    .nlargest(top_n)
)

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=top_restaurants.values,
    y=top_restaurants.index,
    palette="viridis",
    ax=ax1
)
ax1.set_xlabel("Average Cost (₹)")
ax1.set_ylabel("Restaurant Name")

st.pyplot(fig1)

st.markdown("---")

# -----------------------------
# COST DISTRIBUTION
# -----------------------------
st.header("📈 Cost Distribution")

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_df["approx_cost"], bins=20, kde=True, ax=ax2)
ax2.set_xlabel("Cost (₹)")

st.pyplot(fig2)

st.markdown("---")

# -----------------------------
# RAW DATA OPTION
# -----------------------------
if st.checkbox("📄 Show Raw Data"):
    st.dataframe(filtered_df)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("✨ Built with Streamlit | Zomato Cost Analysis Dashboard")
