import csv

import config
from modules.skill_matcher import text_contains_skill


def load_education_terms():
    """Load education terms and standard levels from CSV."""

    terms = []

    if not config.EDUCATION_TERMS_FILE.exists():
        return terms

    with open(
        config.EDUCATION_TERMS_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            term = row.get("term", "").strip()
            level = row.get("education_level", "").strip().lower()

            if term and level:
                terms.append({"term": term, "level": level})

    return terms


def detect_education(text, terms):
    """Find education levels and evidence in text."""

    detected = []

    for item in terms:
        if text_contains_skill(text, item["term"]):
            if item["level"] not in [result["level"] for result in detected]:
                detected.append(item)

    return detected


def highest_education_level(detected):
    """Return the highest configured education level found."""

    highest_level = ""
    highest_position = -1

    for item in detected:
        if item["level"] in config.EDUCATION_LEVELS:
            position = config.EDUCATION_LEVELS.index(item["level"])

            if position > highest_position:
                highest_position = position
                highest_level = item["level"]

    return highest_level


def match_education(required_education, resume_text):
    """Compare the required education level with resume evidence."""

    terms = load_education_terms()
    required_detected = detect_education(required_education, terms)
    resume_detected = detect_education(resume_text, terms)
    required_level = highest_education_level(required_detected)
    resume_level = highest_education_level(resume_detected)

    if not required_education.strip():
        percentage = config.PERCENT_DIVISOR
        status = "No education requirement"
    elif not required_level:
        percentage = 0
        status = "Requirement needs manual verification"
    elif not resume_level:
        percentage = 0
        status = "Education not detected"
    else:
        required_position = config.EDUCATION_LEVELS.index(required_level)
        resume_position = config.EDUCATION_LEVELS.index(resume_level)

        if resume_position >= required_position:
            percentage = config.PERCENT_DIVISOR
            status = "Education level matched"
        else:
            percentage = 0
            status = "Required education level not detected"

    return {
        "required_level": required_level,
        "detected_level": resume_level,
        "percentage": percentage,
        "status": status,
        "evidence": [item["term"] for item in resume_detected],
    }

