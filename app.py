import streamlit as st
import pandas as pd
import joblib

# --- BAGIAN 1: LOAD MODEL ---
# Pastikan file .pkl sudah diunduh dan diletakkan di folder yang sama
try:
    model = joblib.load('gym_experience_model.pkl')
    preprocessor = joblib.load('gym_preprocessor.pkl')
except FileNotFoundError:
    st.error("File model (.pkl) tidak ditemukan! Pastikan file sudah diunduh dari Colab ke folder VS Code Anda.")
    st.stop()

# --- BAGIAN 2: ANTARMUKA (UI) ---
st.set_page_config(page_title="Gym Experience Predictor", layout="wide")
st.title("🏋️ Gym Member Experience Level Predictor")
st.markdown("--- ")

with st.sidebar:
    st.header("Input Profil Anggota")
    age = st.number_input("Usia", 10, 80, 25)
    gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])
    weight = st.number_input("Berat Badan (kg)", 30.0, 150.0, 70.0)
    height = st.number_input("Tinggi Badan (m)", 1.0, 2.2, 1.7)
    workout_type = st.selectbox("Jenis Latihan", ["Yoga", "HIIT", "Cardio", "Strength"])

col1, col2 = st.columns(2)
with col1:
    max_bpm = st.number_input("Max BPM", 60, 220, 180)
    avg_bpm = st.number_input("Avg BPM", 40, 200, 140)
    resting_bpm = st.number_input("Resting BPM", 30, 120, 60)
with col2:
    session_duration = st.number_input("Durasi Sesi (jam)", 0.5, 3.0, 1.0)
    fat_percentage = st.number_input("Persentase Lemak", 5.0, 50.0, 20.0)
    water_intake = st.number_input("Asupan Air (liter)", 0.5, 5.0, 2.0)
    workout_freq = st.slider("Frekuensi Latihan (hari/minggu)", 1, 7, 3)

# --- BAGIAN 3: PREDIKSI ---
if st.button("Prediksi Sekarang"):
    input_data = pd.DataFrame({
        'Age': [age], 'Gender': [gender], 'Weight (kg)': [weight], 'Height (m)': [height],
        'Max_BPM': [max_bpm], 'Avg_BPM': [avg_bpm], 'Resting_BPM': [resting_bpm],
        'Session_Duration (hours)': [session_duration], 'Fat_Percentage': [fat_percentage],
        'Water_Intake (liters)': [water_intake], 'Workout_Frequency (days/week)': [workout_freq],
        'Workout_Type': [workout_type]
    })
    
    # Transformasi dan Prediksi
    processed = preprocessor.transform(input_data)
    pred = model.predict(processed)[0]
    
    res_map = {1: "Beginner 🟢", 2: "Intermediate 🟡", 3: "Expert 🔴"}
    st.success(f"Hasil Prediksi: {res_map[pred]}")