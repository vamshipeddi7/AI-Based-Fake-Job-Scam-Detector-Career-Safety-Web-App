import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.email_utils import send_user_confirmation, notify_admin

st.set_page_config(page_title="Report a Scam", layout="centered")

st.markdown("<h1 style='text-align:center; color:#FF5733;'>📢 Report a Job Scam</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Help us protect others! Share any suspicious job offer with proof 📄</p>", unsafe_allow_html=True)
st.markdown("---")

# ----------- Report Form -----------
with st.form("report_form"):
    name = st.text_input("👤 Your Name")
    email = st.text_input("📧 Your Email")
    phone = st.text_input("📱 Your Phone Number (10 digits)")
    description = st.text_area("📝 Describe the Scam Job Post", height=200)
    proof = st.file_uploader("📎 Upload Proof (image, PDF, etc)", type=['jpg', 'jpeg', 'png', 'pdf'])

    submit = st.form_submit_button("🚀 Submit Report")

    if submit:
        if not name or not email or not phone or not description:
            st.warning("⚠️ Please fill in all required fields.")
        elif not phone.isdigit() or len(phone) != 10:
            st.warning("📱 Phone number must be 10 digits.")
        elif "@" not in email or "." not in email:
            st.warning("📧 Please enter a valid email address.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save proof
            proof_path = ""
            if proof:
                proof_dir = "data/proofs"
                os.makedirs(proof_dir, exist_ok=True)
                proof_path = os.path.join(proof_dir, proof.name)
                with open(proof_path, "wb") as f:
                    f.write(proof.read())

            # Save report
            data = {
                "Name": [name],
                "Email": [email],
                "Phone": [phone],
                "Description": [description],
                "Proof File": [proof_path],
                "Timestamp": [timestamp]
            }

            df = pd.DataFrame(data)
            file_path = "data/pending_reports.csv"
            if os.path.exists(file_path):
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                df.to_csv(file_path, index=False)

            # 📩 Send email confirmation and notify admin
            send_user_confirmation(name, email)
            notify_admin(name, email, phone, description, proof_path, timestamp)

            st.success("✅ Report submitted successfully! Confirmation email sent.")
            st.info("🔔 Admin has been notified.")
