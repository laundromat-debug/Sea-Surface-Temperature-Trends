"""
Project Title:
Analyzing Sea Surface Temperatures and How They Affect Global Warming

Author: [Saanvi Singh]
Description:
This program analyzes sea surface temperature (SST) data from NOAA/NASA
NetCDF (.nc) files to identify temperature trends in U.S. coastal regions
and visualize their contribution to global warming.
"""

# =========================
# 1. IMPORT LIBRARIES
# =========================
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =========================
# 2. LOAD DATASET
# =========================
# Replace with your actual NetCDF file path
file_path = "sea_surface_temperature.nc"

# Open NetCDF dataset
dataset = xr.open_dataset(file_path)

# Display dataset structure (useful for exploration)
print(dataset)

# =========================
# 3. SELECT & CLEAN DATA
# =========================
# Example variable name commonly used for SST
# (May be 'sst', 'sea_surface_temperature', etc.)
sst = dataset["sst"]

# Convert temperature from Kelvin to Celsius if needed
sst_celsius = sst - 273.15

# Remove missing values
sst_clean = sst_celsius.where(~np.isnan(sst_celsius), drop=True)

# =========================
# 4. FOCUS ON U.S. REGIONS
# =========================
# Example coordinates for U.S. coastal waters
us_sst = sst_clean.sel(
    lat=slice(20, 50),    # Latitude range
    lon=slice(-130, -60) # Longitude range
)

# =========================
# 5. TIME TREND ANALYSIS
# =========================
# Calculate yearly average temperature
yearly_avg = us_sst.groupby("time.year").mean(dim=["lat", "lon"])

# Convert to Pandas DataFrame
df = yearly_avg.to_dataframe(name="Avg_Temperature_C").reset_index()

# =========================
# 6. PERCENT CHANGE CALCULATION
# =========================
df["Percent_Change"] = df["Avg_Temperature_C"].pct_change() * 100

# =========================
# 7. DATA TABLE OUTPUT
# =========================
print("\nSea Surface Temperature Trends (U.S. Waters):")
print(df.head())

# =========================
# 8. VISUALIZATION
# =========================

# Line graph of temperature trend
plt.figure()
plt.plot(df["year"], df["Avg_Temperature_C"])
plt.xlabel("Year")
plt.ylabel("Average Sea Surface Temperature (°C)")
plt.title("Sea Surface Temperature Trends in U.S. Coastal Waters")
plt.show()

# Percent change visualization
plt.figure()
plt.bar(df["year"], df["Percent_Change"])
plt.xlabel("Year")
plt.ylabel("Percent Temperature Increase (%)")
plt.title("Yearly Percentage Increase in Sea Surface Temperature")
plt.show()

# =========================
# 9. INTERPRETATION SUPPORT
# =========================

"""
This analysis helps marine biologists:
- Identify warming trends in ocean regions
- Measure how quickly temperatures are rising
- Understand impacts on coral reefs and marine ecosystems
- Compare data side-by-side using tables and graphs 
"""
