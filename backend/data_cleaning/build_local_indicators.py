import pandas as pd
import os

def build_master_indicators():
    print("Building GramGrow AI Local Indicators Master Dataset...")

    # 1. Load Processed Datasets
    livestock_path = "data/processed/livestock_enterprises_clean.csv"
    enterprises_path = "data/processed/year_of_enterprises_clean.csv"

    if not os.path.exists(livestock_path) or not os.path.exists(enterprises_path):
        print("Error: Processed datasets not found. Please ensure both clean CSVs are in data/processed/")
        return

    df_livestock = pd.read_csv(livestock_path)
    df_enterprises = pd.read_csv(enterprises_path)

    # 2. Standardize district column formatting
    df_livestock['district'] = df_livestock['district'].astype(str).str.strip().str.title()
    df_enterprises['district'] = df_enterprises['district'].astype(str).str.strip().str.title()

    # 3. Merge Datasets on District (Outer join to capture all 14 Kerala districts)
    df_master = pd.merge(df_enterprises, df_livestock, on='district', how='outer')

    # 4. Compute Composite Advisory Indicators
    if 'achievement_percent' in df_master.columns and 'investment_crore' in df_master.columns:
        df_master['economic_activity_score'] = (
            df_master['achievement_percent'].fillna(100) * 0.5 + 
            (df_master['investment_crore'] / df_master['investment_crore'].max() * 100) * 0.5
        )

    # 5. Save Master Dataset
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "master_local_indicators.csv")
    
    df_master.to_csv(output_path, index=False)
    print(f"Success! Master indicator dataset created at: {output_path}")
    print(f"Total districts compiled: {len(df_master)}")
    print(df_master[['district', 'achievement_percent', 'investment_crore']].head())

if __name__ == "__main__":
    build_master_indicators()
    