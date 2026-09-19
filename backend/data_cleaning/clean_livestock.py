import pandas as pd

# Load the raw file
df = pd.read_csv("data/raw/kerala_livestock_enterprises.csv")

# Inspect it first
print(df.columns)
print(df.head())

# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Remove the "Total" summary row, keep only real districts
df = df[df['district'] != 'Total']

# Add metadata columns
df['source'] = 'Kerala Livestock Enterprises Data'
df['data_level'] = 'district'
df['last_updated'] = '2026-09-12'

# Save cleaned output
df.to_csv("data/processed/livestock_enterprises_clean.csv", index=False)
print("Saved:", df.shape)