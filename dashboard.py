import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Gym Member Dashboard", layout="wide")

# Handle File Loading for Local VS Code vs Colab
def load_data():
    # 1. Coba path lokal (folder yang sama dengan script)
    local_path = 'gym_members_exercise_tracking.csv'
    # 2. Coba path Colab
    colab_path = '/content/gym_members_exercise_tracking.csv'
    
    if os.path.exists(local_path):
        return pd.read_csv(local_path)
    elif os.path.exists(colab_path):
        return pd.read_csv(colab_path)
    else:
        st.error(f"File CSV tidak ditemukan! Pastikan file '{local_path}' ada di folder yang sama dengan script ini.")
        st.info("Silakan upload file secara manual di bawah ini:")
        uploaded_file = st.file_uploader("Pilih file CSV", type="csv")
        if uploaded_file is not None:
            return pd.read_csv(uploaded_file)
        st.stop()

df = load_data()

st.title("📊 Gym Experience Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
gender_filter = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
workout_filter = st.sidebar.multiselect("Select Workout Type", options=df['Workout_Type'].unique(), default=df['Workout_Type'].unique())

filtered_df = df[(df['Gender'].isin(gender_filter)) & (df['Workout_Type'].isin(workout_filter))]

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Members", len(filtered_df))
col2.metric("Avg Age", f"{filtered_df['Age'].mean():.1f}")
col3.metric("Avg Session", f"{filtered_df['Session_Duration (hours)'].mean():.2f}h")
col4.metric("Avg Fat %", f"{filtered_df['Fat_Percentage'].mean():.1f}%")

# Visualization Row 1
st.subheader("Member Distributions")
c1, c2 = st.columns(2)
with c1:
    fig_exp = px.pie(filtered_df, names='Experience_Level', title="Experience Level Distribution", 
                 labels={'1':'Beginner', '2':'Intermediate', '3':'Expert'}, hole=0.4)
    st.plotly_chart(fig_exp, use_container_width=True)
with c2:
    fig_freq = px.histogram(filtered_df, x='Workout_Frequency (days/week)', color='Experience_Level', 
                         title="Workout Frequency by Experience", barmode='group')
    st.plotly_chart(fig_freq, use_container_width=True)

# Visualization Row 2
st.subheader("Performance Correlates")
c3, c4 = st.columns(2)
with c3:
    fig_scatter = px.scatter(filtered_df, x='Session_Duration (hours)', y='Fat_Percentage', 
                          color='Experience_Level', title="Session Duration vs Fat Percentage")
    st.plotly_chart(fig_scatter, use_container_width=True)
with c4:
    corr = filtered_df.select_dtypes(include=['number']).corr()
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", title="Feature Correlation Matrix", color_continuous_scale='RdBu_r')
    st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("--- ")
st.info("Dashboard ini memberikan wawasan tentang demografi anggota gym dan hubungannya dengan tingkat pengalaman latihan.")