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

