import streamlit as st
from utils.preprocess import clean_text
import pickle
import numpy as np

# Load model and vectorizer
model = pickle.load(open("model/model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

# Set page config
st.set_page_config(
    page_title="Fake Job Scam Detector - VST",
    layout="wide",
    page_icon="🛡️"
)

# Apply dark mode gradient styles
st.markdown("""
    <style>
        html, body, .stApp {
            background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%) !important;
            color: white !important;
        }

        .stApp { padding: 2rem; }

        textarea, input, .stButton > button, .stTextInput > div > div > input {
            background-color: #2a2f4a !important;
            color: white !important;
            border: 1px solid #5fa3ff !important;
        }

        .stTextArea textarea {
            font-size: 16px;
            color: white !important;
        }

        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p,
        label, .css-1d391kg, .css-1n76uvr {
            color: #f1f1f1 !important;
        }

        .stDownloadButton, .stDownloadButton button {
            background-color: #2a2f4a !important;
            color: white !important;
        }

        .stAlert {
            background-color: #33415c !important;
            color: white !important;
        }

        .stDataFrame, .stTable {
            background-color: #1e1e2f !important;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <h1 style='color:#A9D6FF; margin-bottom:0;'>🛡️ Fake Job Scam Detector</h1>
    <p style='font-size:18px;'>Run by <b>Trusted Safety Team - VST</b></p>
""", unsafe_allow_html=True)

# Input section
st.markdown("---")
st.markdown("<h4>📋 Paste the Job Description Below:</h4>", unsafe_allow_html=True)
job_text = st.text_area("", height=250)

# 🚨 Keyword Scam Filter
SCAM_KEYWORDS = [
    "telegram", "upi", "earn ₹", "earn rs", "whatsapp", "dm us", "instantly paid",
    "make money from home", "click here", "bot job", "gift card", "easy money", "google reviews",
    "promote app", "limited seats", "only 5 spots", "no resume", "no interview"
]

if st.button("🧠 Detect Now"):
    if not job_text.strip():
        st.warning("⚠️ Please enter a job description to analyze.")
    elif len(job_text.strip().split()) < 10:
        st.warning("⚠️ Job description is too short. Please provide more detailed information.")
    elif any(word in job_text.lower() for word in SCAM_KEYWORDS):
        st.error("🚨 Suspicious content detected! This job post contains high-risk scam keywords.")
        st.markdown("""
            ### ⚠️ Scam Red Flags:
            - Mentions Telegram, WhatsApp, or UPI
            - Promises of quick money or easy jobs
            - Asking to contact bots or unknown handles

            ### 🛡️ Safety Advice:
            - Never apply to jobs promising instant cash
            - Avoid apps/bots asking for personal info or money
            - Legit companies post on verified platforms
        """)
    else:
        # ML Prediction
        cleaned = clean_text(job_text)
        vectorized = vectorizer.transform([cleaned])

        probability = model.predict_proba(vectorized)[0]
        prediction = np.argmax(probability)
        confidence = np.max(probability)

        st.markdown(f"### 🔍 Confidence Score: {confidence * 100:.2f}%")

        if prediction == 1:
            st.error("❌ This job post looks like a SCAM! Be careful.")
            st.markdown("""
                ### ⚠️ Safety Tips:
                - Never send money for job offers.
                - Don’t share OTPs, IDs or bank info.
                - Verify company websites and email domains.
                - Real jobs rarely use WhatsApp/Telegram for hiring.
            """)
        else:
            st.success("✅ This appears to be a legitimate job post.")
            st.markdown("""
                ### ✅ Tips:
                - Always research about the company.
                - Apply through official career pages.
                - Don’t trust unbelievable salaries with zero effort.
            """)

# Footer
st.markdown("""
    <hr>
    <p style='text-align:center; color:#999; font-size:14px;'>
        © 2025 | Developed by <b style='color:#FF5733;'>Vamshi</b> | AI-Based Fake Job Scam Detector 💼🔍
    </p>
""", unsafe_allow_html=True)

