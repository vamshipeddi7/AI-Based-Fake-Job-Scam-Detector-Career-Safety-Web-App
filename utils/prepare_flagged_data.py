# utils/prepare_flagged_data.py

import pandas as pd
import os

def prepare_flagged_for_training():
    flagged_path = "data/flagged_scams.csv"
    approved_path = "data/approved_scams.csv"

    if not os.path.exists(flagged_path):
        print("⚠️ No flagged scams found.")
        return

    flagged_df = pd.read_csv(flagged_path)
    flagged_df.dropna(subset=["description"], inplace=True)

    if flagged_df.empty:
        print("⚠️ Flagged file is empty after cleaning.")
        return

    # Add mandatory columns for model training
    flagged_df["fraudulent"] = 1
    flagged_df["title"] = "Flagged"
    flagged_df["location"] = "User Input"
    flagged_df["timestamp"] = pd.Timestamp.now()

    # Remove duplicates based on 'description'
    flagged_df.drop_duplicates(subset=["description"], inplace=True)

    # Merge with approved scams
    if os.path.exists(approved_path):
        approved_df = pd.read_csv(approved_path)
        combined = pd.concat([approved_df, flagged_df], ignore_index=True)
        combined.drop_duplicates(subset=["description"], inplace=True)  # De-dup total
    else:
        combined = flagged_df

    # Save updated approved scams
    combined.to_csv(approved_path, index=False)

    # Optional: Clear flagged file after processing
    try:
        os.remove(flagged_path)
        print("🧹 Cleared flagged_scams.csv after merging.")
    except Exception as e:
        print(f"⚠️ Could not delete flagged_scams.csv: {e}")

    print(f"✅ {len(flagged_df)} flagged scam(s) added to approved_scams.csv (Total now: {len(combined)})")
