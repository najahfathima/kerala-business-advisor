def check_nsfdc_eligibility(
    is_sc: bool,
    annual_family_income: float,
    project_cost: float
):
    eligible = True
    reasons = []

    if not is_sc:
        eligible = False
        reasons.append("Applicant must belong to the Scheduled Caste community.")

    if annual_family_income > 500000:
        eligible = False
        reasons.append("Annual family income exceeds the current ₹5 lakh limit.")

    if project_cost <= 0:
        eligible = False
        reasons.append("Project cost must be greater than zero.")

    if eligible:
        return {
            "scheme": "NSFDC",
            "eligible": True,
            "status": "Eligible",
            "reasons": [
                "Applicant satisfies the basic NSFDC eligibility conditions."
            ],
            "verification_required": True
        }

    return {
        "scheme": "NSFDC",
        "eligible": False,
        "status": "Not Eligible",
        "reasons": reasons,
        "verification_required": True
    }