from modules.experience_matcher import detect_experience_years
from modules.experience_matcher import match_experience


def test_detect_explicit_experience():
    years, evidence = detect_experience_years("More than 3 years of experience")

    assert years == 3
    assert evidence == ["3 years"]


def test_detect_year_date_range():
    years, evidence = detect_experience_years("2020 - 2022")

    assert years == 3
    assert evidence == ["2020 - 2022"]


def test_experience_meets_requirement():
    result = match_experience(2, "3 years of software development experience")

    assert result["percentage"] == 100


def test_experience_below_requirement():
    result = match_experience(4, "2 years of software development experience")

    assert result["percentage"] == 50


def test_experience_not_detected():
    result = match_experience(2, "Worked as a Python developer")

    assert result["percentage"] == 0

