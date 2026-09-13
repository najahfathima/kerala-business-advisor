def calculate_confidence(local_evidence: dict):
    if local_evidence is None:
        return {
            "confidence": "Low",
            "score": 0.35,
            "label": "No verified district-level evidence is available."
        }

    sources = local_evidence.get("sources", [])
    data_level = local_evidence.get("data_level", "unknown")

    if len(sources) >= 2 and data_level == "district":
        return {
            "confidence": "High",
            "score": 0.90,
            "label": "Based on multiple verified district-level data sources."
        }

    return {
        "confidence": "Medium",
        "score": 0.70,
        "label": "Based on available structured local indicators."
    }