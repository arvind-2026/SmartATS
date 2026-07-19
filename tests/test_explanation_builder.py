from modules.explanation_builder import build_component_calculation
from modules.explanation_builder import build_score_explanation


def test_build_component_calculation():
    component = {
        "percentage": 80,
        "weight": 35,
        "points": 28,
    }

    result = build_component_calculation(component)

    assert result == "80% × 35 / 100 = 28 points"


def test_build_score_explanation():
    score_result = {
        "components": [
            {
                "label": "Required skills",
                "percentage": 80,
                "weight": 35,
                "points": 28,
            }
        ]
    }

    result = build_score_explanation(score_result)

    assert result[0]["label"] == "Required skills"
    assert result[0]["calculation"] == "80% × 35 / 100 = 28 points"

