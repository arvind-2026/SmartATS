import csv
from io import StringIO

import config


def prepare_export_row(candidate):
    """Prepare one candidate dictionary for CSV export."""

    row = candidate.copy()
    row["matched_skills"] = "; ".join(candidate["matched_skills"])
    row["missing_skills"] = "; ".join(candidate["missing_skills"])

    return row


def create_candidate_export(candidates):
    """Return candidate results as downloadable CSV text."""

    output = StringIO()
    export_headers = ["rank"] + config.CANDIDATE_CSV_HEADERS
    writer = csv.DictWriter(
        output,
        fieldnames=export_headers,
        extrasaction="ignore",
    )
    writer.writeheader()

    for candidate in candidates:
        writer.writerow(prepare_export_row(candidate))

    return output.getvalue()

