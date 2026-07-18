import re
from datetime import datetime

import config


def find_explicit_years(text):
    """Find statements such as '3 years of experience'."""

    pattern = r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)"
    matches = re.finditer(pattern, text, re.IGNORECASE)
    results = []

    for match in matches:
        results.append({
            "years": float(match.group(1)),
            "evidence": match.group(0),
        })

    return results


def month_number(month_name):
    """Convert a written month into its number."""

    return config.MONTH_NAMES.get(month_name.lower(), 1)


def find_date_ranges(text):
    """Find common employment date ranges and calculate their durations."""

    month_words = "|".join(config.MONTH_NAMES.keys())
    pattern = (
        r"(?:((?:" + month_words + r"))\s+)?(\d{4})\s*"
        r"(?:-|–|—|to)\s*"
        r"(?:(?:((?:" + month_words + r"))\s+)?(\d{4})|present|current)"
    )
    matches = re.finditer(pattern, text, re.IGNORECASE)
    current_date = datetime.now()
    results = []

    for match in matches:
        start_month = month_number(match.group(1)) if match.group(1) else 1
        start_year = int(match.group(2))

        if match.group(4):
            end_month = month_number(match.group(3)) if match.group(3) else 12
            end_year = int(match.group(4))
        else:
            end_month = current_date.month
            end_year = current_date.year

        start_value = start_year * config.MONTHS_PER_YEAR + start_month
        end_value = end_year * config.MONTHS_PER_YEAR + end_month

        if end_value >= start_value:
            duration_months = end_value - start_value + 1
            duration_years = duration_months / config.MONTHS_PER_YEAR
            results.append({
                "years": duration_years,
                "evidence": match.group(0),
            })

    return results


def detect_experience_years(text):
    """Use the clearest available evidence to estimate experience."""

    explicit_results = find_explicit_years(text)
    date_results = find_date_ranges(text)
    detected_years = 0
    evidence = []

    if date_results:
        detected_years = sum(item["years"] for item in date_results)
        evidence = [item["evidence"] for item in date_results]

    for item in explicit_results:
        if item["years"] > detected_years:
            detected_years = item["years"]
            evidence = [item["evidence"]]

    return round(detected_years, config.ROUND_SCORE_DIGITS), evidence


def match_experience(required_years, resume_text):
    """Compare detected experience with the job requirement."""

    detected_years, evidence = detect_experience_years(resume_text)

    if required_years == 0:
        percentage = config.PERCENT_DIVISOR
        message = "The job has no minimum experience requirement."
    elif detected_years == 0:
        percentage = 0
        message = "Experience duration was not detected. Manual verification is required."
    else:
        percentage = detected_years / required_years * config.PERCENT_DIVISOR
        percentage = min(percentage, config.PERCENT_DIVISOR)
        message = (
            str(detected_years)
            + " detected years / "
            + str(required_years)
            + " required years"
        )

    return {
        "required_years": required_years,
        "detected_years": detected_years,
        "percentage": round(percentage, config.ROUND_SCORE_DIGITS),
        "evidence": evidence,
        "message": message,
    }

