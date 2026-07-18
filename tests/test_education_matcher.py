from modules.education_matcher import match_education


def test_bachelor_matches_requirement():
    result = match_education(
        "Bachelor's degree in Computer Science",
        "B.Tech in Computer Science",
    )

    assert result["percentage"] == 100
    assert result["detected_level"] == "bachelor"


def test_master_meets_bachelor_requirement():
    result = match_education(
        "Bachelor's degree",
        "MCA from Delhi University",
    )

    assert result["percentage"] == 100
    assert result["detected_level"] == "master"


def test_missing_education():
    result = match_education("Bachelor's degree", "Python developer")

    assert result["percentage"] == 0
    assert result["status"] == "Education not detected"


def test_no_education_requirement():
    result = match_education("", "Python developer")

    assert result["percentage"] == 100
