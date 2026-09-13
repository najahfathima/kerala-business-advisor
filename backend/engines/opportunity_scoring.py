import pandas as pd
import os

def calculate_opportunity(district: str, business_type: str, df_master=None):
    """
    Analyzes local competition/saturation using real district data
    and suggests alternatives if the market is crowded.
    """
    enterprise_density = "Moderate"
    alternative_suggestion = f"Favorable conditions for launching {business_type}."
    
    if df_master is None:
        paths = ["master_local_indicators.csv", "../data/processed/master_local_indicators.csv", "data/processed/master_local_indicators.csv"]
        for p in paths:
            if os.path.exists(p):
                df_master = pd.read_csv(p)
                break
                
    if df_master is not None:
        district_row = df_master[df_master['district'].str.lower() == district.lower()]
        if not district_row.empty:
            ach = district_row.iloc[0].get('achievement_percent', 100)
            if ach > 110:
                enterprise_density = "High (Saturated Market)"
                alternative_suggestion = (
                    f"High saturation for {business_type} in {district}. "
                    f"Recommended Alternative: Focus on a specialized sub-segment, "
                    f"value-added packaging, or digital direct-to-consumer delivery."
                )
            else:
                enterprise_density = "Low-to-Moderate (Growth Opportunity)"
                alternative_suggestion = f"Good growth potential for {business_type} in {district}."

    return {
        "district": district,
        "business_type": business_type,
        "market_competition": enterprise_density,
        "alternative_suggestion": alternative_suggestion
    }