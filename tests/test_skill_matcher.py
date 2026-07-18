from modules.skill_matcher import match_job_skills
from modules.skill_matcher import text_contains_skill


def test_match_required_skills():
    resume_text = "Built Python applications and used SQL databases with Git."
    result = match_job_skills(
        ["Python", "SQL", "Git", "Docker"],
        [],
        resume_text,
    )

    assert result["required"]["matched_skills"] == ["Python", "SQL", "Git"]
    assert result["required"]["missing_skills"] == ["Docker"]
    assert result["required"]["percentage"] == 75


def test_match_skill_alias():
    resume_text = "Created an ML model for document classification."
    result = match_job_skills(["Machine Learning"], [], resume_text)

    assert result["required"]["matched_skills"] == ["Machine Learning"]


def test_skill_match_is_case_insensitive():
    result = match_job_skills(["Python"], [], "PYTHON developer")

    assert result["required"]["percentage"] == 100


def test_partial_word_is_not_a_skill_match():
    assert text_contains_skill("JavaScript developer", "Java") is False


def test_preserve_cpp_skill_symbols():
    assert text_contains_skill("Developed software using C++", "c++") is True


def test_empty_required_skills():
    result = match_job_skills([], [], "Python developer")

    assert result["required"]["percentage"] == 0

