"""
Streamlit Website: Sea Surface Temperature Trends
Revised, beginner-safe version for school projects
Run with: streamlit run app.py
"""


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
page_title="Sea Surface Temperature Trends",
layout="centered"
)


# -------------------------
# TITLE & DESCRIPTION
# -------------------------
st.title("Analyzing Sea Surface Temperatures and Global Warming")


st.markdown("""
**Topic:** Sea Surface Temperatures and their impact on coral reefs and global warming
**Audience:** Marine biologists and climate researchers
**Goal:** Analyze temperature trends in U.S. waters using structured data
""")


# -------------------------
# SAMPLE STRUCTURED DATASET
# -------------------------
data = {
"Year": [2018, 2019, 2020, 2021, 2022, 2023],
"Average Sea Surface Temperature (°C)": [18.1, 18.3, 18.6, 18.9, 19.2, 19.6]
}


df = pd.DataFrame(data)
df["Percent Increase (%)"] = df["Average Sea Surface Temperature (°C)"].pct_change() * 100


# -------------------------
# DISPLAY DATA TABLE
# -------------------------
st.subheader("Sea Surface Temperature Data")
st.dataframe(df)


# -------------------------
# VISUALIZATION
# -------------------------
st.subheader("Temperature Trend Over Time")


fig, ax = plt.subplots()
ax.plot(df["Year"], df["Average Sea Surface Temperature (°C)"])
ax.set_xlabel("Year")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Rising Sea Surface Temperatures in U.S. Waters")


st.pyplot(fig)


# -------------------------
# ANALYSIS SECTION
# -------------------------
st.subheader("Analysis & Findings")
st.markdown("""
- Sea surface temperatures show a steady increase over time.
- Rising ocean temperatures contribute to coral bleaching and ecosystem stress.
- The percent increase highlights accelerating warming trends.
- This data supports broader evidence of global climate change.
""")


# -------------------------
# SAFE END GOAL CONFIRMATION
# -------------------------
st.success("Safe End Goal Achieved: Data successfully compared using a table and graph.")


# -------------------------
# REACH GOAL (FUTURE WORK)
# -------------------------

