import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from model.train_model import retrain_model
from utils.email_utils import notify_user_on_approval, notify_user_on_rejection

# ---- Config ----
st.set_page_config(page_title="Admin Dashboard", layout="wide")

# ---- Paths ----
pending_path = "data/pending_reports.csv"
approved_path = "data/approved_scams.csv"
rejected_path = "data/rejected_reports.csv"
log_path = "model/model_metrics_log.csv"

# ---- Styling ----
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: white;
        }
        .stButton>button {
            background-color: #00C6FF;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#00C6FF;'>🔐 Admin Dashboard - Fake Job Scam Reports</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Review, Approve, Reject, and Retrain the model with real user-reported scams</p>", unsafe_allow_html=True)
st.markdown("---")

# ---- Login ----
with st.sidebar:
    st.markdown("### 🔑 Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login = st.button("Login")

# ---- Main Section ----
if login:
    if username == "VST123" and password == "VST@123":
        st.success("✅ Logged in successfully!")

        # Load pending reports
        if not os.path.exists(pending_path):
            st.info("📂 No pending reports found.")
            st.stop()

        pending_df = pd.read_csv(pending_path)
        pending_df.columns = pending_df.columns.str.strip().str.title()

        if pending_df.empty:
            st.info("✅ No new user reports to review.")
            st.stop()

        # Load approved
        if os.path.exists(approved_path):
            approved_df = pd.read_csv(approved_path)
            approved_df.columns = approved_df.columns.str.lower()
        else:
            approved_df = pd.DataFrame(columns=["title", "location", "description", "fraudulent", "timestamp"])

        # Filter new
        if "description" in approved_df.columns:
            new_reports = pending_df[~pending_df["Description"].isin(approved_df["description"])]
        else:
            st.warning("⚠️ 'description' column missing in approved. Showing all.")
            new_reports = pending_df

        if new_reports.empty:
            st.success("✅ All reports already reviewed.")
            st.stop()

        # Show first unreviewed report
        row = new_reports.iloc[0]
        index = new_reports.index[0]
        st.markdown("### 🚨 Pending User Report")
        st.markdown(f"📌 <b>#{index + 1}</b> by <b>{row['Name'].upper()}</b> at <code>{row['Timestamp']}</code>", unsafe_allow_html=True)
        st.write(f"📧 Email: [{row['Email']}](mailto:{row['Email']}) | 📱 Phone: {row['Phone']}")
        st.markdown("**📜 Description:**")
        st.code(row["Description"])

        # Proof
        if pd.notna(row["Proof File"]) and os.path.exists(row["Proof File"]):
            if row["Proof File"].endswith(('.jpg', '.jpeg', '.png')):
                st.image(row["Proof File"], width=300)
            else:
                with open(row["Proof File"], "rb") as f:
                    st.download_button("📥 Download Proof", data=f, file_name=os.path.basename(row["Proof File"]))

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Approve", key=f"approve_{index}"):
                new_entry = pd.DataFrame({
                    "title": [row["Description"][:40] + "..."],
                    "location": ["Reported"],
                    "description": [row["Description"]],
                    "fraudulent": [1],
                    "timestamp": [row["Timestamp"]]
                })
                new_entry.to_csv(approved_path, mode='a', header=not os.path.exists(approved_path), index=False)

                pending_df = pending_df[pending_df["Description"] != row["Description"]]
                pending_df.to_csv(pending_path, index=False)

                retrain_model()
                notify_user_on_approval(row["Name"], row["Email"])

                st.success("✅ Report approved, model retrained, and user notified.")
                st.experimental_rerun()

        with col2:
            if st.button("❌ Reject", key=f"reject_{index}"):
                if os.path.exists(rejected_path):
                    rejected_df = pd.read_csv(rejected_path)
                else:
                    rejected_df = pd.DataFrame(columns=pending_df.columns)

                rejected_df = pd.concat([rejected_df, pd.DataFrame([row])], ignore_index=True)
                rejected_df.to_csv(rejected_path, index=False)

                pending_df = pending_df[pending_df["Description"] != row["Description"]]
                pending_df.to_csv(pending_path, index=False)

                notify_user_on_rejection(row["Name"], row["Email"])
                st.info("🗑️ Report rejected and user notified.")
                st.experimental_rerun()

        # Accuracy Trend
        if os.path.exists(log_path):
            df = pd.read_csv(log_path)
            df['Old_Accuracy'] = pd.to_numeric(df['Old_Accuracy'], errors='coerce')
            df['New_Accuracy'] = pd.to_numeric(df['New_Accuracy'], errors='coerce')
            df.dropna(subset=['Old_Accuracy', 'New_Accuracy'], inplace=True)
            df['Run'] = range(1, len(df) + 1)

            st.markdown("## 📈 Model Accuracy Trend")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df['Run'], df['Old_Accuracy'], marker='o', linestyle='--', label='Old Accuracy', color='red')
            ax.plot(df['Run'], df['New_Accuracy'], marker='o', label='New Accuracy', color='green')
            ax.fill_between(df['Run'], df['Old_Accuracy'], df['New_Accuracy'], color='lightgreen', alpha=0.3)

            ax.set_xlabel('Retrain Run Number')
            ax.set_ylabel('Accuracy')
            ax.set_title('Model Accuracy Before vs After Retrain')
            ax.set_xticks(df['Run'])
            ax.set_ylim(0.8, 1.0)
            ax.legend()
            ax.grid(True)

            st.pyplot(fig)
        else:
            st.info("📂 No accuracy log yet. Approve a report to trigger retraining.")
    else:
        st.error("❌ Invalid credentials.")
