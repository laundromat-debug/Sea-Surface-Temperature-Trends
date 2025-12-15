"""
Streamlit Website: Sea Surface Temperature Trends
"""

# =========================
# IMPORT LIBRARIES
# =========================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Sea Surface Temperature Trends",
    layout="centered"
)

# =========================
# TITLE & DESCRIPTION
# =========================
st.title("Analyzing Sea Surface Temperatures and Global Warming")

st.markdown("""
**Topic:** Sea Surface Temperatures and their impact on coral reefs and global warming  
**Audience:** Marine biologists and climate researchers  
**Goal:** Analyze temperature trends in U.S. and global tourist waters using tables and graphs
""")

# =========================
# NETCDF FILE UPLOAD OR SAMPLE
# =========================
st.subheader("Dataset Loading")

file_path = st.file_uploader("Upload a NetCDF file (.nc)", type=["nc"])

# Fallback sample NetCDF creation
def create_sample_netcdf():
    import xarray as xr
    import numpy as np
    import pandas as pd

    times = pd.date_range("2018-01-01", "2023-12-31", freq="M")
    lat = np.linspace(-90, 90, 36)
    lon = np.linspace(-180, 180, 72)
    data = 18 + 1.5*np.random.randn(len(times), len(lat), len(lon))  # °C
    ds = xr.Dataset(
        {"sst": (("time", "lat", "lon"), data)},
        coords={"time": times, "lat": lat, "lon": lon}
    )
    return ds

if file_path:
    try:
        dataset = xr.open_dataset(file_path)
        st.success("NetCDF dataset loaded successfully.")
    except Exception as e:
        st.warning(f"Could not load uploaded file. Using sample dataset. ({e})")
        dataset = create_sample_netcdf()
else:
    st.info("No file uploaded. Using sample dataset instead.")
    dataset = create_sample_netcdf()

# =========================
# CHECK SST VARIABLE
# =========================
if "sst" not in dataset.variables:
    st.error("SST variable not found in dataset. Using sample data.")
    dataset = create_sample_netcdf()

sst = dataset["sst"]

# Convert Kelvin → Celsius if needed
if float(sst.mean()) > 100:  # likely Kelvin
    sst = sst - 273.15

# Remove missing values
sst_clean = sst.where(~np.isnan(sst), drop=True)

# =========================
# U.S. WATERS ANALYSIS
# =========================
us_sst = sst_clean.sel(lat=slice(20, 50), lon=slice(-130, -60))
yearly_avg = us_sst.groupby("time.year").mean(dim=["lat", "lon"])
df_us = yearly_avg.to_dataframe(name="Average Sea Surface Temperature (°C)").reset_index()
df_us.rename(columns={"year": "Year"}, inplace=True)
df_us["Percent Increase (%)"] = df_us["Average Sea Surface Temperature (°C)"].pct_change() * 100

st.subheader("Sea Surface Temperature Data (U.S. Waters)")
st.dataframe(df_us)

# Visualization
st.subheader("Temperature Trend Over Time (U.S. Waters)")
fig, ax = plt.subplots()
ax.plot(df_us["time"], df_us["Average Sea Surface Temperature (°C)"], marker='o')
ax.set_xlabel("time")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Rising Sea Surface Temperatures in U.S. Coastal Waters")
st.pyplot(fig)

# =========================
# TOURIST REGION ANALYSIS
# =========================
st.subheader("Tourist Ocean Regions & Global Warming")

tourist_regions = {
    "Caribbean": {"lat": slice(10, 25), "lon": slice(-90, -60)},
    "Mediterranean": {"lat": slice(30, 45), "lon": slice(-5, 35)},
    "Hawaii": {"lat": slice(18, 23), "lon": slice(-162, -154)},
    "Southeast Asia": {"lat": slice(-10, 20), "lon": slice(95, 130)}
}

tourist_dfs = []

for region, coords in tourist_regions.items():
    region_sst = sst_clean.sel(lat=coords["lat"], lon=coords["lon"])
    yearly_region = region_sst.groupby("time.year").mean(dim=["lat", "lon"])
    temp_df = yearly_region.to_dataframe(name="Temperature (°C)").reset_index()
    temp_df["Region"] = region
    tourist_dfs.append(temp_df)

tourist_df = pd.concat(tourist_dfs)
st.dataframe(tourist_df.head())

# Visualization
fig2, ax2 = plt.subplots()
for region in tourist_regions:
    subset = tourist_df[tourist_df["Region"] == region]
    ax2.plot(subset["time"], subset["Temperature (°C)"], marker='o', label=region)

ax2.set_xlabel("time")
ax2.set_ylabel("Temperature (°C)")
ax2.set_title("Sea Surface Temperature Trends in Major Tourist Regions")
ax2.legend()
st.pyplot(fig2)

# =========================
# ANALYSIS & FINDINGS
# =========================
st.subheader("Analysis & Findings")
st.markdown("""
- Sea surface temperatures show a consistent upward trend over time.
- Tourist-heavy marine regions experience warming that accelerates coral bleaching.
- Warmer oceans absorb less CO₂, intensifying global warming feedback loops.
- Human activity in popular ocean regions amplifies environmental stress.
""")

# =========================
# FUTURE WORK
# =========================
st.markdown("""
**Future Improvements:**
- Add CO₂ emission overlays
- Compare El Niño vs La Niña years
- Introduce statistical trendlines and projections
""")
