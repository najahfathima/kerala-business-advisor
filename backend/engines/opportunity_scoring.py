def calculate_opportunity(local_evidence: dict):
    """
    Calculate opportunity using verified local district indicators.

    This does NOT claim to directly measure competition or demand.
    It uses available economic activity and enterprise formation
    indicators as proxies.
    """

    economic_activity = local_evidence.get("economic_activity_score", 0)
    achievement = local_evidence.get("achievement_percent", 0)
    employment = local_evidence.get("employment_generated", 0)

    # Normalize indicators to a 0-100 scale
    economic_score = min(max(float(economic_activity), 0), 100)
    achievement_score = min(max(float(achievement), 0), 100)

    # Employment is normalized relative to a practical district benchmark.
    employment_score = min((float(employment) / 30000) * 100, 100)

    opportunity_score = (
        economic_score * 0.50
        + achievement_score * 0.30
        + employment_score * 0.20
    )

    if opportunity_score >= 70:
        rating = "High Opportunity"
    elif opportunity_score >= 50:
        rating = "Moderate Opportunity"
    else:
        rating = "Low Opportunity"

    return {
        "score": round(opportunity_score, 2),
        "rating": rating,
        "basis": [
            "Economic activity score",
            "Enterprise formation achievement",
            "Employment generated"
        ],
        "data_status": "VERIFIED / PROXY",
        "note": (
            "Opportunity is estimated from available district-level "
            "economic indicators. Direct competition, demand and "
            "purchasing-power data are not available in the current dataset."
        )
    }