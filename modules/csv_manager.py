import csv
from datetime import datetime

import config


def convert_list_to_text(items):
    """Convert a Python list into text that can be stored in a CSV cell."""

    return "; ".join(items)


def save_job(job):
    """Add one job dictionary to the jobs CSV file."""

    config.STORAGE_FOLDER.mkdir(exist_ok=True)
    file_has_data = config.JOBS_FILE.exists() and config.JOBS_FILE.stat().st_size > 0

    row = job.copy()
    row["required_skills"] = convert_list_to_text(job["required_skills"])
    row["preferred_skills"] = convert_list_to_text(job["preferred_skills"])

    with open(config.JOBS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=config.JOB_CSV_HEADERS)

        if not file_has_data:
            writer.writeheader()

        writer.writerow(row)


def load_jobs():
    """Load all saved jobs and return them as a list of dictionaries."""

    jobs = []

    if not config.JOBS_FILE.exists():
        return jobs

    with open(config.JOBS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row.get("job_id"):
                continue

            row["required_skills"] = convert_text_to_list(
                row.get("required_skills", "")
            )
            row["preferred_skills"] = convert_text_to_list(
                row.get("preferred_skills", "")
            )

            try:
                row["required_experience"] = float(
                    row.get("required_experience", 0)
                )
            except ValueError:
                row["required_experience"] = 0

            for component in config.SCORE_COMPONENTS:
                weight_key = component["weight_key"]

                try:
                    row[weight_key] = int(float(row.get(weight_key, 0)))
                except ValueError:
                    row[weight_key] = 0

            jobs.append(row)

    return jobs


def append_dictionary(file_path, headers, row):
    """Append one dictionary to a CSV file and create its header if needed."""

    config.STORAGE_FOLDER.mkdir(exist_ok=True)
    file_has_data = file_path.exists() and file_path.stat().st_size > 0

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        if not file_has_data:
            writer.writeheader()

        writer.writerow(row)


def candidate_already_saved(job_id, file_name):
    """Check whether the same file was saved previously for this job."""

    if not config.CANDIDATES_FILE.exists():
        return False

    with open(
        config.CANDIDATES_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row.get("job_id") == job_id and row.get("file_name") == file_name:
                return True

    return False


def ensure_candidate_csv_columns():
    """Upgrade an existing candidate CSV when new columns are introduced."""

    if not config.CANDIDATES_FILE.exists():
        return

    with open(
        config.CANDIDATES_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)
        existing_headers = reader.fieldnames or []
        rows = list(reader)

    if existing_headers == config.CANDIDATE_CSV_HEADERS:
        return

    with open(
        config.CANDIDATES_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=config.CANDIDATE_CSV_HEADERS)
        writer.writeheader()

        for old_row in rows:
            new_row = {}

            for header in config.CANDIDATE_CSV_HEADERS:
                new_row[header] = old_row.get(header, "")

            writer.writerow(new_row)


def save_candidate(candidate):
    """Save one completed candidate screening result."""

    ensure_candidate_csv_columns()
    row = candidate.copy()
    row["matched_skills"] = convert_list_to_text(candidate["matched_skills"])
    row["missing_skills"] = convert_list_to_text(candidate["missing_skills"])

    append_dictionary(
        config.CANDIDATES_FILE,
        config.CANDIDATE_CSV_HEADERS,
        row,
    )


def save_score_details(candidate_id, score_result, explanations):
    """Save every component calculation for later HR review."""

    for index in range(len(score_result["components"])):
        component = score_result["components"][index]
        explanation = explanations[index]
        row = {
            "candidate_id": candidate_id,
            "component": component["label"],
            "match_percentage": component["percentage"],
            "weight": component["weight"],
            "points_awarded": component["points"],
            "calculation": explanation["calculation"],
        }
        append_dictionary(
            config.SCORE_DETAILS_FILE,
            config.SCORE_DETAIL_CSV_HEADERS,
            row,
        )


def save_semantic_evidence(candidate_id, evidence_items):
    """Save requirement-to-resume evidence for explainable review."""

    for evidence in evidence_items:
        row = {
            "candidate_id": candidate_id,
            "job_requirement": evidence["requirement"],
            "resume_evidence": evidence["resume_evidence"],
            "similarity": evidence["similarity"],
        }
        append_dictionary(
            config.SEMANTIC_EVIDENCE_FILE,
            config.SEMANTIC_EVIDENCE_CSV_HEADERS,
            row,
        )


def convert_text_to_list(text):
    """Convert a semicolon-separated CSV cell back into a Python list."""

    if not text:
        return []

    return [item.strip() for item in text.split(";") if item.strip()]


def load_candidates():
    """Load saved candidate results with numeric scores and skill lists."""

    candidates = []

    if not config.CANDIDATES_FILE.exists():
        return candidates

    with open(
        config.CANDIDATES_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row.get("candidate_id"):
                continue

            for score_field in config.DASHBOARD_SCORE_FIELDS:
                try:
                    row[score_field] = float(row.get(score_field, 0))
                except ValueError:
                    row[score_field] = 0

            row["matched_skills"] = convert_text_to_list(
                row.get("matched_skills", "")
            )
            row["missing_skills"] = convert_text_to_list(
                row.get("missing_skills", "")
            )
            candidates.append(row)

    return candidates


def load_candidate_score_details(candidate_id):
    """Load saved component calculations for one candidate."""

    details = []

    if not config.SCORE_DETAILS_FILE.exists():
        return details

    with open(
        config.SCORE_DETAILS_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row.get("candidate_id") == candidate_id:
                details.append(row)

    return details


def load_candidate_semantic_evidence(candidate_id):
    """Load saved semantic evidence for one candidate."""

    evidence_items = []

    if not config.SEMANTIC_EVIDENCE_FILE.exists():
        return evidence_items

    with open(
        config.SEMANTIC_EVIDENCE_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row.get("candidate_id") == candidate_id:
                evidence_items.append(row)

    return evidence_items


def update_candidate_review(candidate_id, review_status, hr_notes):
    """Update a candidate and append a timestamped HR review record."""

    if not config.CANDIDATES_FILE.exists():
        return False

    with open(
        config.CANDIDATES_FILE,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    candidate_found = False

    for row in rows:
        if row.get("candidate_id") == candidate_id:
            row["review_status"] = review_status
            row["hr_notes"] = hr_notes
            candidate_found = True

    if not candidate_found:
        return False

    with open(
        config.CANDIDATES_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=config.CANDIDATE_CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    review_row = {
        "candidate_id": candidate_id,
        "review_status": review_status,
        "hr_notes": hr_notes,
        "reviewed_at": datetime.now().strftime(config.REVIEW_DATETIME_FORMAT),
    }
    append_dictionary(
        config.HR_REVIEWS_FILE,
        config.HR_REVIEW_CSV_HEADERS,
        review_row,
    )

    return True
