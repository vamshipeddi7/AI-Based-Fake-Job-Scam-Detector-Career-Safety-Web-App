import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from utils.preprocess import clean_text
from utils.prepare_flagged_data import prepare_flagged_for_training

# Paths
BASE_DATA = "data/fake_job_postings.csv"
APPROVED_SCAMS = "data/approved_scams.csv"
MODEL_PATH = "model/model.pkl"
VECTORIZER_PATH = "model/vectorizer.pkl"
ACCURACY_LOG = "data/accuracy_log.csv"

# Step 1: Append flagged to approved
prepare_flagged_for_training()

# Step 2: Load base + approved scam data
base_df = pd.read_csv(BASE_DATA)
if os.path.exists(APPROVED_SCAMS):
    approved_df = pd.read_csv(APPROVED_SCAMS)
else:
    approved_df = pd.DataFrame(columns=["title", "location", "description", "fraudulent", "timestamp"])

# Combine and clean
combined_df = pd.concat([base_df, approved_df], ignore_index=True)
combined_df.dropna(subset=["description", "fraudulent"], inplace=True)

# Prepare final text
combined_df["text"] = (combined_df["title"].fillna("") + " " + combined_df["description"]).apply(clean_text)
X = combined_df["text"]
y = combined_df["fraudulent"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load old model & vectorizer (if exist)
def get_old_accuracy():
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        with open(MODEL_PATH, "rb") as f:
            old_model = pickle.load(f)
        with open(VECTORIZER_PATH, "rb") as f:
            old_vectorizer = pickle.load(f)
        X_test_vec_old = old_vectorizer.transform(X_test)
        old_preds = old_model.predict(X_test_vec_old)
        return accuracy_score(y_test, old_preds)
    return None

old_accuracy = get_old_accuracy()

# Train new model
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression()
model.fit(X_train_vec, y_train)
new_preds = model.predict(X_test_vec)
new_accuracy = accuracy_score(y_test, new_preds)

# Save model only if improved
improved = False
if old_accuracy is None or new_accuracy > old_accuracy:
    pickle.dump(model, open(MODEL_PATH, "wb"))
    pickle.dump(vectorizer, open(VECTORIZER_PATH, "wb"))
    print(f"✅ Model updated. Accuracy: {new_accuracy:.4f} (old: {old_accuracy or 'N/A'})")
    improved = True
else:
    print(f"⚠️ No update. Accuracy did not improve ({old_accuracy:.4f} → {new_accuracy:.4f})")

# Log accuracy
log_data = {
    "Old_Accuracy": [old_accuracy if old_accuracy else 0],
    "New_Accuracy": [new_accuracy],
    "Improved": [improved],
    "Total_Records": [len(combined_df)]
}
log_df = pd.DataFrame(log_data)

if os.path.exists(ACCURACY_LOG):
    prev_log = pd.read_csv(ACCURACY_LOG)
    updated_log = pd.concat([prev_log, log_df], ignore_index=True)
else:
    updated_log = log_df

updated_log.to_csv(ACCURACY_LOG, index=False)
