import csv

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
            if row.get("job_id"):
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
