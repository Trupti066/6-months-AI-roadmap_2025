import streamlit as st
import numpy as np
import pickle
import pandas as pd
import os

# --- Load model and tools safely using os ---
current_dir = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(current_dir, "avocado_model.pkl")
scaler_path = os.path.join(current_dir, "scaler.pkl")
regions_path = os.path.join(current_dir, "regions.pkl")
columns_path = os.path.join(current_dir, "columns.pkl")  # Optional if you saved column names

# Load files
with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(scaler_path, "rb") as f:
    scaler = pickle.load(f)

with open(regions_path, "rb") as f:
    region_columns = pickle.load(f)

with open(columns_path, "rb") as f:
    column_names = pickle.load(f)

# --- Streamlit UI ---
st.title("🥑 Avocado Price Predictor")

# --- Inputs ---
year = st.selectbox("Year", [2015, 2016, 2017, 2018])

# Month dropdown with names
month_map = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}
month_name = st.selectbox("Month", list(month_map.keys()))
month = month_map[month_name]

# Numeric features
total_volume = st.number_input("Total Volume", min_value=0.0)
total_bags = st.number_input("Total Bags", min_value=0.0)
small_bags = st.number_input("Small Bags", min_value=0.0)
large_bags = st.number_input("Large Bags", min_value=0.0)
xlarge_bags = st.number_input("XLarge Bags", min_value=0.0)
type_input = st.radio("Avocado Type", ["conventional", "organic"])
region = st.selectbox("Region", region_columns)

# Encode type
type_encoded = 0 if type_input == "conventional" else 1

# --- Prepare input ---
numerical_input = [[
    year, month, total_volume, total_bags,
    small_bags, large_bags, xlarge_bags,
    type_encoded
]]

# Use correct column names for scaler
numerical_df = pd.DataFrame(numerical_input, columns=column_names)
numerical_scaled = scaler.transform(numerical_df)

# One-hot encode region
region_vector = [1 if r == region else 0 for r in region_columns]
region_vector = np.array(region_vector).reshape(1, -1)

# Final input
input_data = np.concatenate([numerical_scaled, region_vector], axis=1)

# --- Predict ---
if st.button("Predict"):
    prediction = model.predict(input_data)
    st.success(f"💰 Predicted Avocado Price: ${round(prediction[0], 2)}")
