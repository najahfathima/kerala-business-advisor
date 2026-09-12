import pandas as pd
MASTER_DATA_PATH = "../data/processed/master_local_indicators.csv"

master_data = pd.read_csv(MASTER_DATA_PATH)
master_data["district"] = master_data["district"].str.strip().str.lower()
from fastapi import FastAPI
from pydantic import BaseModel

from engines.financial_model import calculate_financials
from engines.opportunity_scoring import calculate_opportunity
from engines.risk_engine import calculate_risk
from engines.whatif import run_what_if
from engines.confidence import calculate_confidence
from engines.scheme_engine import check_nsfdc_eligibility


app = FastAPI(title="RuralBiz AI")


class Entrepreneur(BaseModel):
    location: str
    available_capital: float
    business_category: str


class BusinessAnalysis(BaseModel):
    location: str
    business_category: str
    competition: str
    demand: str
    purchasing_power: str


class FinancialInput(BaseModel):
    available_capital: float
    project_cost: float
    monthly_revenue: float
    monthly_expenses: float
    interest_rate: float = 8.0
    tenure_years: int = 7


class WhatIfInput(BaseModel):
    revenue: float
    expenses: float
    emi: float


class SchemeEligibilityInput(BaseModel):
    is_sc: bool
    annual_family_income: float
    project_cost: float

class AdvisoryReportInput(BaseModel):
    location: str
    business_category: str

    competition: str
    demand: str
    purchasing_power: str

    available_capital: float
    project_cost: float
    monthly_revenue: float
    monthly_expenses: float

    interest_rate: float = 8.0
    tenure_years: int = 7

    is_sc: bool
    annual_family_income: float


@app.get("/")
def home():
    return {
        "message": "RuralBiz AI Backend is running"
    }


@app.post("/entrepreneur")
def create_entrepreneur(entrepreneur: Entrepreneur):
    return {
        "message": "Entrepreneur profile received",
        "data": entrepreneur
    }


@app.post("/analyze-business")
def analyze_business(data: BusinessAnalysis):

    opportunity = calculate_opportunity(
        data.competition,
        data.demand,
        data.purchasing_power
    )

    confidence = calculate_confidence(True)

    return {
        "location": data.location,
        "business": data.business_category,
        "competition": data.competition,
        "demand": data.demand,
        "purchasing_power": data.purchasing_power,
        "opportunity": opportunity,
        "confidence": confidence
    }


@app.post("/financial-analysis")
def financial_analysis(data: FinancialInput):

    result = calculate_financials(
        data.available_capital,
        data.project_cost,
        data.monthly_revenue,
        data.monthly_expenses,
        data.interest_rate,
        data.tenure_years
    )

    risk = calculate_risk(
    data.monthly_revenue,
    data.monthly_expenses,
    result["estimated_emi"]
)

    return {
        "financial_analysis": result,
        "risk_analysis": risk
    }


@app.post("/stress-test")
def stress_test(data: WhatIfInput):

    return run_what_if(
        data.revenue,
        data.expenses,
        data.emi
    )


@app.post("/recommendation")
def recommendation(data: FinancialInput):

    result = calculate_financials(
        data.available_capital,
        data.project_cost,
        data.monthly_revenue,
        data.monthly_expenses,
        data.interest_rate,
        data.tenure_years
    )

    cash_after_emi = result["remaining_cash_after_emi"]

    if cash_after_emi > 10000:
        decision = "GO"
        reason = "Projected cash flow provides a reasonable repayment buffer."
    elif cash_after_emi >= 0:
        decision = "MODIFY"
        reason = "The business may survive, but the financing structure is tight."
    else:
        decision = "DON'T PROCEED"
        reason = "Projected cash flow cannot comfortably support the repayment."

    return {
        "decision": decision,
        "reason": reason,
        "recommended_financing": result
    }
@app.post("/scheme-eligibility")
def scheme_eligibility(data: SchemeEligibilityInput):

    return check_nsfdc_eligibility(
        data.is_sc,
        data.annual_family_income,
        data.project_cost
    )
@app.post("/advisory-report")
def advisory_report(data: AdvisoryReportInput):

    district_data = master_data[
        master_data["district"] == data.location.strip().lower()
    ]

    # 1. Business opportunity
    opportunity = calculate_opportunity(
        data.competition,
        data.demand,
        data.purchasing_power
    )