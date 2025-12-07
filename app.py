import streamlit as st
import pandas as pd
import pickle

# ---------- Model Load ----------
model_path = "aqi_model.pkl"
with open(model_path, "rb") as f:
    model = pickle.load(f)

# ---------- App Title ----------
st.title("AQI Prediction & Health Suggestion 🌿")
st.markdown("""
Enter sensor readings below to predict AQI. 
Suggestions will also be provided based on AQI and age group.
""")

# ---------- User Input ----------
st.header("User Information")
age = st.number_input("Enter Age (years)", min_value=1, max_value=120, value=25)

st.header("Sensor Inputs")
col1, col2, col3 = st.columns(3)

with col1:
    temp = st.number_input("Temperature (°C)", value=25.0)
    humidity = st.number_input("Humidity (%)", value=50.0)
    no2_ppb = st.number_input("NO2 (ppb)", value=10.0)

with col2:
    o3_ppb = st.number_input("O3 (ppb)", value=10.0)
    co_ppm = st.number_input("CO (ppm)", value=0.5)

with col3:
    pm25 = st.number_input("PM2.5 (µg/m³)", value=20.0)
    pm10 = st.number_input("PM10 (µg/m³)", value=30.0)

# ---------- Predict Button ----------
if st.button("Predict AQI"):
    # Create DataFrame matching model's features
    input_df = pd.DataFrame([[
        no2_ppb, o3_ppb, co_ppm, pm25, pm10, temp, humidity
    ]], columns=['NO2 ppb','O3 ppb','CO ppm','PM2.5','PM10','TempC','Humidity'])

    # Prediction
    predicted_aqi = model.predict(input_df)[0]

    # Major Pollutant
    pollutants = {'NO2': no2_ppb, 'O3': o3_ppb, 'CO': co_ppm, 'PM2.5': pm25, 'PM10': pm10}
    major_pollutant = max(pollutants, key=pollutants.get)

    # AQI Category & Base Suggestion
    def aqi_category(aqi):
        if aqi <= 50:
            return "Good", "Air quality is satisfactory. Enjoy outdoor activities."
        elif aqi <= 100:
            return "Moderate", "Air quality is acceptable. Sensitive people should take precautions."
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups", "Sensitive groups should reduce prolonged outdoor exertion."
        elif aqi <= 200:
            return "Unhealthy", "Everyone may experience health effects. Limit outdoor activities."
        elif aqi <= 300:
            return "Very Unhealthy", "Health alert: everyone may experience more serious effects. Avoid outdoor activities."
        else:
            return "Hazardous", "Health warning of emergency conditions. Stay indoors and avoid exposure."

    category, suggestion = aqi_category(predicted_aqi)

    # Age-wise Suggestion
    if age <= 12:
        suggestion += " Children should avoid outdoor play."
    elif age >= 60:
        suggestion += " Elderly should stay indoors and limit exposure."

    # ---------- Output ----------
    st.subheader("Predicted AQI & Suggestions")
    st.write(f"**Predicted AQI:** {predicted_aqi:.2f}")
    st.write(f"**Category:** {category}")
    st.write(f"**Major Pollutant:** {major_pollutant} ({pollutants[major_pollutant]})")
    st.write(f"**Suggestion:** {suggestion}")
