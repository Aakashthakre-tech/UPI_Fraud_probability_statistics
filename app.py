import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.title("💳 UPI Fraud Detection System")

st.write("Enter transaction details:")

# Inputs
amount = st.number_input("Amount (INR)", min_value=0.0)
hour = st.slider("Hour", 0, 23)
day = st.slider("Day", 1, 31)
month = st.slider("Month", 1, 12)

day_of_week = st.selectbox(
    "Day of Week",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

age_mismatch = st.selectbox("Age Group Mismatch", [0, 1])
different_bank = st.selectbox("Different Bank", [0, 1])
is_wifi = st.selectbox("Using WiFi", [0, 1])
device = st.selectbox("Device Type", ["Android", "iOS"])

transaction_type = st.selectbox("Transaction Type", ["P2P", "P2M"])

# 🔧 Derived features
hour_of_day = hour
is_weekend = 1 if day_of_week in ["Saturday", "Sunday"] else 0
is_night = 1 if hour < 6 else 0
is_business_hours = 1 if 9 <= hour <= 18 else 0
weekend_night = 1 if (is_weekend == 1 and is_night == 1) else 0

is_android = 1 if device == "Android" else 0
is_ios = 1 if device == "iOS" else 0

is_P2P = 1 if transaction_type == "P2P" else 0
is_P2M = 1 if transaction_type == "P2M" else 0

if st.button("Predict"):
    try:
        input_data = pd.DataFrame({
            'amount (inr)': [amount],
            'hour_of_day': [hour_of_day],
            'day_of_week': [day_of_week],
            'is_weekend': [is_weekend],
            'hour': [hour],
            'day': [day],
            'month': [month],
            'is_night': [is_night],
            'is_business_hours': [is_business_hours],
            'age_group_mismatch': [age_mismatch],
            'different_bank': [different_bank],
            'is_wifi': [is_wifi],
            'is_android': [is_android],
            'is_ios': [is_ios],
            'weekend_night': [weekend_night],
            'is_P2P': [is_P2P],
            'is_P2M': [is_P2M]
        })

        prediction = model.predict(input_data)

        if prediction[0] == 1:
            st.error("⚠️ Fraud Transaction")
        else:
            st.success("✅ Legit Transaction")

    except Exception as e:
        st.error(f"Error: {e}")