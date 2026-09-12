def calculate_confidence(data_available: bool):
    if data_available:
        return {
            "confidence": "Medium",
            "score": 0.70,
            "label": "Based on available structured indicators."
        }

    return {
        "confidence": "Low",
        "score": 0.35,
        "label": "Limited local evidence available."
    }