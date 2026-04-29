import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Zomato Restaurant Dashboard",
    layout="wide",
    page_icon="🍽️"
)

# -----------------------------
# CUSTOM CSS — Dark Luxury Theme
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

/* Root variables */
:root {
    --red:       #E8272A;
    --red-dim:   #9B1A1C;
    --gold:      #F5C842;
    --bg:        #0F0F0F;
    --surface:   #1A1A1A;
    --surface2:  #242424;
    --border:    #2E2E2E;
    --text:      #F0EDE8;
    --muted:     #888580;
}

/* Global reset */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem !important; max-width: 1400px; }

/* ---- HERO HEADER ---- */
.hero {
    background: linear-gradient(135deg, #1a0000 0%, #0F0F0F 60%, #1a0a00 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 3rem 3.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "🍽️";
    position: absolute;
    right: 3rem; top: 50%;
    transform: translateY(-50%);
    font-size: 9rem;
    opacity: 0.07;
}
.hero-tag {
    display: inline-block;
    background: var(--red);
    color: #fff;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 100px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 3.2rem !important;
    font-weight: 900 !important;
    line-height: 1.1 !important;
    margin: 0 0 0.75rem 0 !important;
    color: var(--text) !important;
}
.hero h1 span { color: var(--red); }
.hero p {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    margin: 0;
}

/* ---- METRIC CARDS ---- */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.2rem;
    margin-bottom: 2.5rem;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: var(--red-dim); }
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, var(--red), var(--gold));
    border-radius: 0 0 16px 16px;
}
.metric-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}
.metric-sub {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 0.4rem;
}

/* ---- SECTION HEADERS ---- */
.section-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2.5rem 0 1.2rem 0;
}
.section-dot {
    width: 10px; height: 10px;
    background: var(--red);
    border-radius: 50%;
    flex-shrink: 0;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text);
    margin: 0;
}
.section-line {
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ---- SIDEBAR ---- */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .sidebar-brand {
    background: var(--red);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: 0.03em;
}
section[data-testid="stSidebar"] label {
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stSlider {
    border-color: var(--border) !important;
    background: var(--surface2) !important;
}

/* ---- CHART PANELS ---- */
.chart-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
}

/* ---- DATA TABLE ---- */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ---- DIVIDER ---- */
hr { border-color: var(--border) !important; }

/* ---- FOOTER ---- */
.footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}
.footer span { color: var(--red); }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# MATPLOTLIB DARK THEME
# --------------------------------------------------
BG      = "#1A1A1A"
SURFACE = "#242424"
RED     = "#E8272A"
GOLD    = "#F5C842"
MUTED   = "#888580"
TEXT    = "#F0EDE8"

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    SURFACE,
    "axes.edgecolor":    "#2E2E2E",
    "axes.labelcolor":   MUTED,
    "xtick.color":       MUTED,
    "ytick.color":       MUTED,
    "text.color":        TEXT,
    "grid.color":        "#2E2E2E",
    "grid.linewidth":    0.6,
    "font.family":       "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

# --------------------------------------------------
# HERO BANNER
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-tag">Analytics Dashboard</div>
    <h1>Zomato <span>Restaurant</span><br>Cost Analytics</h1>
    <p>Explore top restaurants and analyze cost trends interactively across Bangalore.</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Zomato_Live.csv")
        return df
    except Exception as e:
        st.error(f"❌ Error loading dataset: {e}")
        st.stop()

df = load_data()

# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

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

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🍽️ Zomato Analytics</div>', unsafe_allow_html=True)

    locations = sorted(df["location"].dropna().unique())
    selected_location = st.selectbox("📍 Location", locations)
    top_n = st.slider("🏆 Top N Restaurants", 5, 20, 10)

    st.markdown("---")
    # Extra: cuisine type filter if column exists
    if "cuisines" in df.columns:
        all_cuisines = df["cuisines"].dropna().str.split(",").explode().str.strip().unique()
        cuisine_filter = st.multiselect(
            "🍜 Filter by Cuisine",
            sorted(all_cuisines),
            default=[]
        )
    else:
        cuisine_filter = []

    st.markdown("---")
    show_raw = st.checkbox("📄 Show Raw Data", value=False)

# --------------------------------------------------
# FILTER
# --------------------------------------------------
filtered_df = df[df["location"] == selected_location].copy()

if cuisine_filter and "cuisines" in df.columns:
    mask = filtered_df["cuisines"].fillna("").apply(
        lambda x: any(c in x for c in cuisine_filter)
    )
    filtered_df = filtered_df[mask]

# --------------------------------------------------
# METRIC CARDS
# --------------------------------------------------
total  = filtered_df["name"].nunique() if "name" in filtered_df.columns else len(filtered_df)
avg_c  = filtered_df["approx_cost"].mean()
max_c  = filtered_df["approx_cost"].max()
min_c  = filtered_df["approx_cost"].min()

avg_str = f"₹ {int(avg_c):,}" if not np.isnan(avg_c) else "N/A"
max_str = f"₹ {int(max_c):,}" if not np.isnan(max_c) else "N/A"
min_str = f"₹ {int(min_c):,}" if not np.isnan(min_c) else "N/A"

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Total Restaurants</div>
        <div class="metric-value">{total}</div>
        <div class="metric-sub">in {selected_location}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Average Cost (2 People)</div>
        <div class="metric-value">{avg_str}</div>
        <div class="metric-sub">across all listings</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Cost Range</div>
        <div class="metric-value">{min_str}</div>
        <div class="metric-sub">min &nbsp;·&nbsp; max {max_str}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CHART 1 — TOP N EXPENSIVE RESTAURANTS (Horizontal Bar)
# --------------------------------------------------
st.markdown(f"""
<div class="section-header">
    <div class="section-dot"></div>
    <p class="section-title">Top {top_n} Most Expensive Restaurants — {selected_location}</p>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

name_col = "name" if "name" in filtered_df.columns else filtered_df.columns[0]
top_restaurants = (
    filtered_df.groupby(name_col)["approx_cost"]
    .mean()
    .nlargest(top_n)
    .sort_values()
)

with st.container():
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    fig1, ax1 = plt.subplots(figsize=(13, max(5, top_n * 0.55)))

    n = len(top_restaurants)
    colors = [plt.cm.YlOrRd(0.4 + 0.55 * (i / max(n - 1, 1))) for i in range(n)]

    bars = ax1.barh(top_restaurants.index, top_restaurants.values,
                    color=colors, height=0.65, zorder=3)

    # Value labels
    for bar, val in zip(bars, top_restaurants.values):
        ax1.text(val + max(top_restaurants.values) * 0.01,
                 bar.get_y() + bar.get_height() / 2,
                 f"₹{int(val):,}", va="center", ha="left",
                 color=TEXT, fontsize=9, fontweight="bold")

    ax1.set_xlabel("Average Cost for Two (₹)", labelpad=10, fontsize=10)
    ax1.set_xlim(0, top_restaurants.values.max() * 1.18)
    ax1.tick_params(axis="y", labelsize=9)
    ax1.tick_params(axis="x", labelsize=9)
    ax1.grid(axis="x", zorder=0)
    fig1.tight_layout()
    st.pyplot(fig1)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# CHART 2 — COST DISTRIBUTION
# --------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <p class="section-title">Cost Distribution</p>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    data_clean = filtered_df["approx_cost"].dropna()

    ax2.hist(data_clean, bins=25, color=RED, alpha=0.75, zorder=3, edgecolor=BG)
    try:
        # Manual Gaussian KDE using numpy only
        kde_x = np.linspace(data_clean.min(), data_clean.max(), 300)
        bw = 1.06 * data_clean.std() * len(data_clean) ** -0.2
        kde_y = np.array([
            np.mean(np.exp(-0.5 * ((kde_x[i] - data_clean.values) / bw) ** 2) / (bw * np.sqrt(2 * np.pi)))
            for i in range(len(kde_x))
        ])
        kde_y_scaled = kde_y * len(data_clean) * (data_clean.max() - data_clean.min()) / 25
        ax2.plot(kde_x, kde_y_scaled, color=GOLD, lw=2.5, zorder=4)
    except Exception:
        pass

    ax2.axvline(data_clean.mean(), color=GOLD, lw=1.5, linestyle="--", alpha=0.9, zorder=5)
    ax2.text(data_clean.mean(), ax2.get_ylim()[1] * 0.95,
             f"  avg ₹{int(data_clean.mean()):,}", color=GOLD, fontsize=8.5, va="top")

    ax2.set_xlabel("Cost for Two (₹)", labelpad=8)
    ax2.set_ylabel("Count", labelpad=8)
    ax2.grid(axis="y", zorder=0)
    fig2.tight_layout()
    st.pyplot(fig2)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# CHART 3 — RATING vs COST SCATTER (if rating col exists)
# --------------------------------------------------
with col_right:
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <p class="section-title">Rating vs Cost</p>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    rating_col = None
    for c in ["rate", "rating", "aggregate_rating"]:
        if c in filtered_df.columns:
            rating_col = c
            break

    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)

    if rating_col:
        scatter_df = filtered_df[[rating_col, "approx_cost"]].copy()
        scatter_df[rating_col] = (
            scatter_df[rating_col]
            .astype(str)
            .str.replace("/5", "", regex=False)
            .str.strip()
        )
        scatter_df[rating_col] = pd.to_numeric(scatter_df[rating_col], errors="coerce")
        scatter_df = scatter_df.dropna()

        fig3, ax3 = plt.subplots(figsize=(7, 4))
        sc = ax3.scatter(scatter_df[rating_col], scatter_df["approx_cost"],
                         c=scatter_df["approx_cost"], cmap="YlOrRd",
                         alpha=0.55, s=30, zorder=3, linewidths=0)

        # Trend line
        if len(scatter_df) > 5:
            z = np.polyfit(scatter_df[rating_col], scatter_df["approx_cost"], 1)
            p = np.poly1d(z)
            xs = np.linspace(scatter_df[rating_col].min(), scatter_df[rating_col].max(), 100)
            ax3.plot(xs, p(xs), color=GOLD, lw=2, linestyle="--", zorder=4, alpha=0.85)

        ax3.set_xlabel("Rating", labelpad=8)
        ax3.set_ylabel("Cost for Two (₹)", labelpad=8)
        ax3.grid(zorder=0)
        fig3.tight_layout()
        st.pyplot(fig3)
    else:
        # Fallback: cost by rating bucket
        cost_buckets = pd.cut(filtered_df["approx_cost"].dropna(),
                               bins=[0, 300, 600, 900, 1200, 99999],
                               labels=["<300", "300–600", "600–900", "900–1200", "1200+"])
        bucket_counts = cost_buckets.value_counts().sort_index()

        fig3, ax3 = plt.subplots(figsize=(7, 4))
        bars3 = ax3.bar(bucket_counts.index.astype(str), bucket_counts.values,
                        color=[RED, "#C94042", "#A05558", GOLD, "#D4A800"],
                        zorder=3, width=0.65)
        for b in bars3:
            ax3.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.5,
                     str(int(b.get_height())), ha="center", va="bottom",
                     fontsize=9, color=TEXT)
        ax3.set_xlabel("Cost Bucket (₹)", labelpad=8)
        ax3.set_ylabel("Count", labelpad=8)
        ax3.grid(axis="y", zorder=0)
        fig3.tight_layout()
        st.pyplot(fig3)

    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# CHART 4 — TOP LOCATIONS BY AVG COST
# --------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <p class="section-title">Location-wise Average Cost Comparison</p>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

loc_avg = (
    df.groupby("location")["approx_cost"]
    .mean()
    .dropna()
    .nlargest(15)
    .sort_values(ascending=True)
)

st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
fig4, ax4 = plt.subplots(figsize=(13, 5))
n4 = len(loc_avg)
bar_colors = [RED if loc == selected_location else "#3A3A3A" for loc in loc_avg.index]
border_colors = [GOLD if loc == selected_location else "none" for loc in loc_avg.index]

bars4 = ax4.barh(loc_avg.index, loc_avg.values, color=bar_colors,
                  height=0.65, zorder=3)

for bar, val, ec in zip(bars4, loc_avg.values, border_colors):
    ax4.text(val + loc_avg.values.max() * 0.01,
             bar.get_y() + bar.get_height() / 2,
             f"₹{int(val):,}", va="center", fontsize=8.5, color=TEXT)

ax4.set_xlabel("Average Cost for Two (₹)", labelpad=8)
ax4.set_xlim(0, loc_avg.values.max() * 1.18)
ax4.grid(axis="x", zorder=0)

legend_patch = mpatches.Patch(color=RED, label=f"Selected: {selected_location}")
ax4.legend(handles=[legend_patch], loc="lower right",
           facecolor=SURFACE, edgecolor="#2E2E2E", labelcolor=TEXT, fontsize=9)
fig4.tight_layout()
st.pyplot(fig4)
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# RAW DATA
# --------------------------------------------------
if show_raw:
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <p class="section-title">Raw Data</p>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(
        filtered_df.style.highlight_max(subset=["approx_cost"], color="#3A1212"),
        use_container_width=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div class="footer">
    Built with <span>♥</span> using Streamlit &nbsp;·&nbsp; Zomato Cost Analytics Dashboard
</div>
""", unsafe_allow_html=True)
