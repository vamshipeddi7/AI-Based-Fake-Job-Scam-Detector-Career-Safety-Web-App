import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Gmail Credentials
SENDER_EMAIL = "trustedsafetyteam@gmail.com"
APP_PASSWORD = "zvhy qpjs camq uxjt"  # App Password

# ✅ 1. Send confirmation email to user
def send_user_confirmation(name, email):
    subject = "✅ Report Submitted Successfully - Fake Job Scam Detector"
    body = f"""
Hi {name},

Thank you for reporting a suspicious job posting. Your input helps protect others from fraud.

Our team will review your report and take appropriate action soon.

Stay safe!  
— Trusted Safety Team (VST)
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print("✅ Confirmation sent to user.")
    except Exception as e:
        print("❌ Failed to send user confirmation:", e)

# ✅ 2. Alert Admin with details + optional attachment
def notify_admin(name, email, phone, description, proof_path, timestamp):
    subject = "🚨 New Scam Report Submitted"
    body = f"""
🔔 New Job Scam Report Received

👤 Name: {name}
📧 Email: {email}
📱 Phone: {phone}
📝 Description:
{description}

📎 Proof File: {'Attached' if proof_path else 'None'}
🕒 Timestamp: {timestamp}

Please verify and take action via Admin Dashboard.
"""
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = SENDER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach file if proof is provided
    if proof_path and os.path.exists(proof_path):
        try:
            with open(proof_path, "rb") as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(proof_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(proof_path)}"'
                msg.attach(part)
        except Exception as e:
            print("⚠️ Failed to attach proof file:", e)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print("✅ Admin notified successfully.")
    except Exception as e:
        print("❌ Failed to send admin alert:", e)

# ✅ 3. Notify user on approval
def notify_user_on_approval(name, email):
    subject = "✅ Your Scam Report Has Been Approved"
    body = f"""
Hi {name},

Thank you again for reporting a suspicious job post.

✅ Your report has been approved by our admin team and is now being used to improve our scam detection model.

Stay safe,  
— Trusted Safety Team (VST)
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print("✅ Approval email sent.")
    except Exception as e:
        print("❌ Failed to send approval email:", e)

# ✅ 4. Notify user on rejection
def notify_user_on_rejection(name, email):
    subject = "❌ Your Scam Report Was Rejected"
    body = f"""
Hi {name},

Thank you for submitting your report.

After a careful review, our team has decided not to approve the report due to insufficient evidence or lack of clarity.

You can still help by submitting other scam posts with more details or better proof.

Thanks again,  
— Trusted Safety Team (VST)
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print("✅ Rejection email sent.")
    except Exception as e:
        print("❌ Failed to send rejection email:", e)
