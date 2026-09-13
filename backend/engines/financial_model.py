def calculate_financials(
    total_project_cost: float,
    available_capital: float,
    monthly_revenue: float,
    monthly_expenses: float,
    interest_rate: float = 8.0,
    tenure_years: int = 7
):
    # Funding gap calculation (Total project cost minus money in hand)
    loan_required = max(total_project_cost - available_capital, 0)
    
    monthly_interest = interest_rate / 100 / 12
    months = tenure_years * 12
    
    if loan_required > 0:
        emi = (
            loan_required 
            * monthly_interest 
            * (1 + monthly_interest) ** months
        ) / ((1 + monthly_interest) ** months - 1)
    else:
        emi = 0

    monthly_profit = monthly_revenue - monthly_expenses
    remaining_cash = monthly_profit - emi

    return {
        "total_project_cost": total_project_cost,
        "own_capital": available_capital,
        "funding_gap_loan_required": round(loan_required, 2),
        "monthly_revenue": monthly_revenue,
        "monthly_expenses": monthly_expenses,
        "monthly_profit_before_emi": round(monthly_profit, 2),
        "estimated_emi": round(emi, 2),
        "remaining_cash_after_emi": round(remaining_cash, 2)
    }