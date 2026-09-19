import pandas as pd
MASTER_DATA_PATH = "../data/processed/master_local_indicators.csv"

master_data = pd.read_csv(MASTER_DATA_PATH)
master_data["district"] = master_data["district"].str.strip().str.lower()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from engines.financial_model import calculate_financials
from engines.opportunity_scoring import calculate_opportunity
from engines.risk_engine import calculate_risk
from engines.whatif import run_what_if
from engines.confidence import calculate_confidence
from engines.scheme_engine import check_nsfdc_eligibility


app = FastAPI(title="RuralBiz AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    # Get verified local district evidence
    from engines.local_evidence import get_local_evidence

    local_evidence = get_local_evidence(data.location)

    if local_evidence is None:
        return {
            "status": "data_gap",
            "location": data.location,
            "business": data.business_category,
            "message": "No verified district-level evidence is available for this location.",
            "recommendation": "MODIFY"
        }

  
     # Opportunity calculation using verified local evidence
    opportunity = calculate_opportunity(local_evidence)

    # Financial analysis
    financial = calculate_financials(
        data.available_capital,
        data.project_cost,
        data.monthly_revenue,
        data.monthly_expenses,
        data.interest_rate,
        data.tenure_years
    )

    # Risk analysis
    risk = calculate_risk(
        data.monthly_revenue,
        data.monthly_expenses,
        financial["estimated_emi"]
    )

    # Stress testing
    stress_test = run_what_if(
        data.monthly_revenue,
        data.monthly_expenses,
        financial["estimated_emi"]
    )

    # Scheme eligibility
    scheme = check_nsfdc_eligibility(
        data.is_sc,
        data.annual_family_income,
        data.project_cost
    )

     # Evidence confidence
    confidence = calculate_confidence(local_evidence)

        # Final decision using financial health + stress test
    cash_after_emi = financial["remaining_cash_after_emi"]

    stress_20 = stress_test["revenue_minus_20_percent"]["cash_after_emi"]
    stress_30 = stress_test["revenue_minus_30_percent"]["cash_after_emi"]

    if cash_after_emi < 0:
        decision = "DON'T PROCEED"
        reason = "The projected business cash flow cannot cover the EMI."

    elif stress_20 < 0:
        decision = "MODIFY"
        reason = "The business is profitable at the projected revenue, but a 20% revenue decline makes repayment difficult."

    elif stress_30 < 0:
        decision = "MODIFY"
        reason = "The business can withstand a 20% revenue decline, but a 30% decline creates repayment risk. Consider reducing the loan or increasing own contribution."

    else:
        decision = "GO"
        reason = "The business covers the EMI under the projected revenue and remains sustainable even under a 30% revenue decline."

    return {
        "status": "success",
        "location": data.location,
        "business": data.business_category,

        "local_evidence": local_evidence,

        "opportunity_analysis": opportunity,

        "financial_analysis": financial,

        "risk_analysis": risk,

        "stress_test": stress_test,

        "scheme_eligibility": scheme,

        "confidence": confidence,

        "recommendation": {
            "decision": decision,
            "reason": reason
        },

        "disclaimer": (
            "RuralBiz AI provides pre-loan business decision support. "
            "It does not approve or reject loans."
        )
    }