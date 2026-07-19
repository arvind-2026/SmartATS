import csv

import config


def create_job_id():
    """Create the next job ID by reading existing jobs from the CSV file."""

    highest_number = 0

    if config.JOBS_FILE.exists():
        with open(config.JOBS_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                job_id = row.get("job_id", "")
                number_text = job_id.replace(config.JOB_ID_PREFIX, "")

                if number_text.isdigit():
                    number = int(number_text)

                    if number > highest_number:
                        highest_number = number

    next_number = highest_number + 1
    number_with_zeros = str(next_number).zfill(config.JOB_ID_DIGITS)

    return config.JOB_ID_PREFIX + number_with_zeros


def create_candidate_id():
    """Create the next candidate ID from the candidate CSV file."""

    highest_number = 0

    if config.CANDIDATES_FILE.exists():
        with open(
            config.CANDIDATES_FILE,
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                candidate_id = row.get("candidate_id", "")
                number_text = candidate_id.replace(
                    config.CANDIDATE_ID_PREFIX,
                    "",
                )

                if number_text.isdigit():
                    number = int(number_text)

                    if number > highest_number:
                        highest_number = number

    next_number = highest_number + 1
    number_with_zeros = str(next_number).zfill(config.CANDIDATE_ID_DIGITS)

    return config.CANDIDATE_ID_PREFIX + number_with_zeros
