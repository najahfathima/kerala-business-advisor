def run_what_if(
    revenue: float,
    expenses: float,
    emi: float
):
    scenarios = {}

    for drop in [10, 20, 30]:
        stressed_revenue = revenue * (1 - drop / 100)
        cash_after_emi = stressed_revenue - expenses - emi

        if cash_after_emi >= 0:
            status = "Sustainable"
        else:
            status = "At Risk"

        scenarios[f"revenue_minus_{drop}_percent"] = {
            "revenue": round(stressed_revenue, 2),
            "cash_after_emi": round(cash_after_emi, 2),
            "status": status
        }

    return scenarios