import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "master_local_indicators.csv"


def get_local_evidence(location: str):
    df = pd.read_csv(DATA_PATH)

    df["district_normalized"] = (
        df["district"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    district = location.strip().lower()

    result = df[df["district_normalized"] == district]

    if result.empty:
        return None

    row = result.iloc[0]

    livestock_total = (
        row["number_of_non_households_enterprises_and_institutions_having_cattle"]
        + row["number_of_non_households_enterprises_and_institutions_having_buffaloes"]
        + row["number_of_non_households_enterprises_and_institutions_having_goats"]
        + row["number_of_non_households_enterprises_and_institutions_having_sheep"]
        + row["number_of_non_households_enterprises_and_institutions_having_pigs"]
        + row["number_of_non_households_enterprises_and_institutions_having_poultry_farm_&_hatcheries"]
    )

    return {
        "district": str(row["district"]),
        "target_enterprises": int(row["target_enterprises"]),
        "enterprises_formed": int(row["enterprises_formed"]),
        "achievement_percent": float(row["achievement_percent"]),
        "investment_crore": float(row["investment_crore"]),
        "employment_generated": int(row["employment_generated"]),
        "livestock_enterprises": int(livestock_total),
        "economic_activity_score": float(row["economic_activity_score"]),
        "sources": [
            str(row["source_x"]),
            str(row["source_y"])
        ],
        "data_level": str(row["data_level_x"]),
        "last_updated": str(row["last_updated_x"])
    }