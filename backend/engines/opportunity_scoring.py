def calculate_opportunity(
    competition: str,
    demand: str,
    purchasing_power: str
):
    scores = {
        "low": 1,
        "moderate": 2,
        "high": 3
    }

    competition_score = scores.get(competition.lower(), 2)
    demand_score = scores.get(demand.lower(), 2)
    purchasing_score = scores.get(purchasing_power.lower(), 2)

    opportunity_score = (
        demand_score * 0.4
        + purchasing_score * 0.3
        + (4 - competition_score) * 0.3
    )

    if opportunity_score >= 2.5:
        rating = "High Opportunity"
    elif opportunity_score >= 1.8:
        rating = "Moderate Opportunity"
    else:
        rating = "Low Opportunity"

    return {
        "score": round(opportunity_score, 2),
        "rating": rating
    }