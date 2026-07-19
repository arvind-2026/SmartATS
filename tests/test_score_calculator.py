import config
from modules.score_calculator import calculate_final_score
from modules.score_calculator import get_score_category
from modules.score_calculator import validate_job_weights


def create_test_job():
    return {
        "semantic_weight": 35,
        "skill_weight": 35,
        "project_weight": 15,
        "experience_weight": 10,
        "education_weight": 5,
    }


def test_calculate_weighted_score():
    percentages = {
        "semantic": 80,
        "skills": 60,
        "projects": 70,
        "experience": 50,
        "education": 100,
    }

    result = calculate_final_score(percentages, create_test_job())

    assert result["success"] is True
    assert result["overall_score"] == 69.5
    assert result["category"] == config.GOOD_SCORE_LABEL


def test_every_component_at_one_hundred():
    percentages = {
        "semantic": 100,
        "skills": 100,
        "projects": 100,
        "experience": 100,
        "education": 100,
    }

    result = calculate_final_score(percentages, create_test_job())

    assert result["overall_score"] == 100


def test_invalid_weights_stop_scoring():
    job = create_test_job()
    job["semantic_weight"] = 30

    result = calculate_final_score({}, job)

    assert result["success"] is False
    assert result["overall_score"] == 0


def test_validate_default_weights():
    result, total = validate_job_weights(create_test_job())

    assert result is True
    assert total == config.TOTAL_SCORE_WEIGHT


def test_score_categories():
    assert get_score_category(85) == config.STRONG_SCORE_LABEL
    assert get_score_category(70) == config.GOOD_SCORE_LABEL
    assert get_score_category(55) == config.PARTIAL_SCORE_LABEL
    assert get_score_category(30) == config.LOW_SCORE_LABEL

