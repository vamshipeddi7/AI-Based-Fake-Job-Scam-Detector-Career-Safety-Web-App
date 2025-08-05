# 📈 1_Trends_and_WordCloud.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
from datetime import datetime
import os

st.set_page_config(page_title="Scam Trends & WordCloud", layout="wide")

st.markdown("""
    <h1 style='text-align:center; color:#00C6FF;'>📊 Scam Trends & WordCloud</h1>
    <p style='text-align:center;'>Visualize scam job descriptions and track trends</p>
    <hr style='border:1px solid #00C6FF;'>
""", unsafe_allow_html=True)

# Load data from verified_scams.csv
verified_path = "data/verified_scams.csv"
if not os.path.exists(verified_path):
    st.warning("No verified scam reports available yet.")
    st.stop()

try:
    df = pd.read_csv(verified_path)
except Exception as e:
    st.error(f"Failed to read data: {e}")
    st.stop()

if df.empty or "description" not in df.columns:
    st.warning("No verified scam reports available yet.")
    st.stop()

# ------ WordCloud ------
st.subheader("☁️ Word Cloud of Reported Scam Descriptions")
df.dropna(subset=["description"], inplace=True)

if not df.empty:
    all_text = " ".join(df["description"].astype(str))
    wordcloud = WordCloud(width=1200, height=500, background_color="black", colormap='cool').generate(all_text)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
else:
    st.info("No scam descriptions available to generate Word Cloud.")

# ------ Trends by Month ------
st.subheader("📅 Monthly Scam Reports Trend")

if "Timestamp" in df.columns:
    df['Month'] = pd.to_datetime(df['Timestamp'], errors='coerce').dt.to_period("M")
    trend_data = df.groupby('Month').size().reset_index(name='Reports')
    trend_data['Month'] = trend_data['Month'].astype(str)

    if not trend_data.empty:
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=trend_data, x='Month', y='Reports', marker='o', ax=ax2)
        ax2.set_title("Monthly Volume of Scam Reports")
        ax2.set_ylabel("Number of Reports")
        ax2.set_xlabel("Month")
        ax2.tick_params(axis='x', rotation=45)
        st.pyplot(fig2)
    else:
        st.info("No timestamped data to display trends.")
else:
    st.info("Timestamps not found in data. Add 'Timestamp' column to track trends.")

# Footer
st.markdown("""
    <hr>
    <div style='text-align:center; font-size: 14px; padding-top:10px; color:gray'>
        <b>Trusted Safety Team</b> | scam trends powered by real reports 📊
    </div>
""", unsafe_allow_html=True)
