import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def notify_admin(user_name, user_email, user_phone, description):
    admin_email = "trustedsafetyteam@gmail.com"
    admin_subject = "🚨 New Scam Report Submitted"
    admin_body = f"""
    🔔 New Job Scam Report Submitted

    👤 Name: {user_name}
    📧 Email: {user_email}
    📱 Phone: {user_phone}
    📝 Description:
    {description}

    📬 Please verify and take action from Admin Dashboard.
    """

    message = MIMEMultipart()
    message["From"] = admin_email
    message["To"] = admin_email
    message["Subject"] = admin_subject
    message.attach(MIMEText(admin_body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(admin_email, "zvhy qpjs camq uxjt")  # your app password
        server.send_message(message)
        server.quit()
        return True
    except Exception as e:
        print("Failed to send admin alert:", e)
        return False
