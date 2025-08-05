# model/train_model.py

import pandas as pd
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from utils.preprocess import clean_text

def retrain_model():
    try:
        base_file = "data/fake_job_postings.csv"
        verified_file = "data/verified_scams.csv"
        log_path = "model/model_metrics_log.csv"

        if not os.path.exists(base_file):
            print("❌ Base dataset not found.")
            return

        base_df = pd.read_csv(base_file)

        # Load verified user-reported scams
        if os.path.exists(verified_file):
            verified_df = pd.read_csv(verified_file)
            verified_df["fraudulent"] = 1
        else:
            verified_df = pd.DataFrame(columns=["description", "fraudulent"])

        # Combine both datasets
        full_df = pd.concat([
            base_df[["description", "fraudulent"]],
            verified_df[["description", "fraudulent"]]
        ], ignore_index=True)

        # Clean text
        full_df.dropna(subset=["description"], inplace=True)
        full_df["clean"] = full_df["description"].apply(clean_text)

        # Feature extraction
        vectorizer = TfidfVectorizer(max_features=5000)
        X = vectorizer.fit_transform(full_df["clean"])
        y = full_df["fraudulent"]

        # Load old model and check accuracy before retrain (if exists)
        old_acc = None
        if os.path.exists("model/model.pkl") and os.path.exists("model/vectorizer.pkl"):
            old_model = pickle.load(open("model/model.pkl", "rb"))
            old_vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

            # Evaluate old model accuracy on full cleaned data
            X_old = old_vectorizer.transform(full_df["clean"])
            y_pred_old = old_model.predict(X_old)
            old_acc = accuracy_score(y, y_pred_old)

        # Train new model
        new_model = LogisticRegression()
        new_model.fit(X, y)

        # Evaluate new model accuracy
        y_pred_new = new_model.predict(X)
        new_acc = accuracy_score(y, y_pred_new)

        # Save model and vectorizer
        os.makedirs("model", exist_ok=True)
        pickle.dump(new_model, open("model/model.pkl", "wb"))
        pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))

        # Log accuracy improvement
        log_exists = os.path.exists(log_path)
        with open(log_path, "a") as log_file:
            if not log_exists:
                log_file.write("Old_Accuracy,New_Accuracy,Total_Records\n")
            log_file.write(f"{old_acc if old_acc else ''},{new_acc:.4f},{len(full_df)}\n")

        print("✅ Model retrained successfully!")
        print(f"📈 Old Accuracy: {old_acc:.4f}" if old_acc else "⚠️ Old model not found.")
        print(f"✅ New Accuracy: {new_acc:.4f}")
        print(f"📊 Records Used: {len(full_df)}")

    except Exception as e:
        print("❌ Failed to retrain model:", e)
