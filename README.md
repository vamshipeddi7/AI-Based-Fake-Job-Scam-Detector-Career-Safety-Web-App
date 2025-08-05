# 🤖 AI-Based Fake Job Scam Detector - Career Safety Web App

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Streamlit](https://img.shields.io/badge/built_with-Streamlit-orange)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

## 🚀 Project Overview

**AI-Based Fake Job Scam Detector** is a smart, user-friendly web application designed to protect job seekers from falling into fake job traps. Built using **Machine Learning** and **Streamlit**, the app allows users to:
- 🔍 Analyze job posts for scam likelihood.
- 📤 Report suspicious job posts with proof.
- 🛡️ Help others stay safe through real-time community feedback.
- 📊 Admins can verify and retrain the model with user reports.

## 📦 Features

- ✅ Real-time scam detection using Logistic Regression + TF-IDF.
- 🧠 Self-improving model (retrained with user-verified scams).
- 📎 File proof submission support (images, PDFs).
- 📧 Email notifications to users and admins.
- 📈 Accuracy trend visualization after each retraining.
- 🔐 Secure admin dashboard with approval/rejection.
- 🌙 Clean, modern, dark-themed UI.

## 🗂️ Project Structure

```
fake_job_scam_detector/
│
├── data/
│   ├── fake_job_postings.csv
│   ├── approved_scams.csv
│   ├── flagged_scams.csv
│   ├── pending_reports.csv
│   └── proofs/                # Uploaded files
│
├── model/
│   ├── model.pkl
│   ├── vectorizer.pkl
│   └── model_metrics_log.csv
│
├── pages/
│   ├── 1_Report_a_Scam.py
│   └── 2_Admin_Dashboard.py
│
├── utils/
│   ├── email_utils.py
│   ├── preprocess.py
│   └── prepare_flagged_data.py
│
├── app.py
├── retrain_model.py
├── requirements.txt
└── README.md
```

## 🛠️ How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/vamshipeddi7/AI-Based-Fake-Job-Scam-Detector-Career-Safety-Web-App.git
cd AI-Based-Fake-Job-Scam-Detector-Career-Safety-Web-App
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv
# Activate:
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the app
```bash
streamlit run app.py
```

---

## 🔐 Admin Login

- **Username**: `VST123`
- **Password**: `VST@123`

## 🙋‍♂️ Created By

**Vamshi Peddi**  
B.Tech Final Year | CSE-AIML Student  
GitHub: [@vamshipeddi7](https://github.com/vamshipeddi7)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📅 Last Updated
August 05, 2025
