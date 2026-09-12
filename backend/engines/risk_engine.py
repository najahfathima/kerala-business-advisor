def calculate_risk(
    monthly_revenue: float,
    monthly_expenses: float,
    emi: float,
    revenue_drop_percent: float = 20
):
    stressed_revenue = monthly_revenue * (
        1 - revenue_drop_percent / 100
    )

    stressed_cash = (
        stressed_revenue
        - monthly_expenses
        - emi
    )

    if monthly_revenue <= monthly_expenses:
        risk = "High"
        reason = "The business is not profitable before loan repayment."

    elif stressed_cash >= 0:
        risk = "Low"
        reason = "The business can still cover expenses and EMI under the stress scenario."

    else:
        risk = "High"
        reason = "The business may struggle to cover expenses and EMI if revenue falls."

    return {
        "risk": risk,
        "stress_revenue_drop": f"{revenue_drop_percent}%",
        "stressed_revenue": round(stressed_revenue, 2),
        "stressed_cash_after_emi": round(stressed_cash, 2),
        "emi": round(emi, 2),
        "reason": reason
    }