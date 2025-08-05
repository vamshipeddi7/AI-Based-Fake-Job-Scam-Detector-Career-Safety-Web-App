import pandas as pd
from utils.preprocess import clean_text

# Load dataset
df = pd.read_csv("data/fake_job_postings.csv")

# Apply cleaning to 'description' column
df["cleaned_description"] = df["description"].apply(clean_text)

# Show sample cleaned data
print("\n🔍 Cleaned Descriptions:")
print(df[["description", "cleaned_description"]].head(3))

# Save to new file for later use
df.to_csv("data/cleaned_job_postings.csv", index=False)
print("\n✅ Cleaned data saved to 'data/cleaned_job_postings.csv'")
