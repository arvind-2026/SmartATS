import csv

import config
from modules.csv_manager import load_candidate_score_details
from modules.csv_manager import load_candidate_semantic_evidence
from modules.csv_manager import update_candidate_review


def test_load_candidate_details(tmp_path, monkeypatch):
    score_file = tmp_path / "score_details.csv"
    evidence_file = tmp_path / "semantic_evidence.csv"
    monkeypatch.setattr(config, "SCORE_DETAILS_FILE", score_file)
    monkeypatch.setattr(config, "SEMANTIC_EVIDENCE_FILE", evidence_file)

    score_file.write_text(
        "candidate_id,component\nCAN001,Required skills\n",
        encoding="utf-8",
    )
    evidence_file.write_text(
        "candidate_id,job_requirement,resume_evidence,similarity\n"
        "CAN001,Build APIs,Created Flask APIs,80\n",
        encoding="utf-8",
    )

    assert len(load_candidate_score_details("CAN001")) == 1
    assert len(load_candidate_semantic_evidence("CAN001")) == 1


def test_update_candidate_review(tmp_path, monkeypatch):
    candidate_file = tmp_path / "candidates.csv"
    review_file = tmp_path / "hr_reviews.csv"
    monkeypatch.setattr(config, "CANDIDATES_FILE", candidate_file)
    monkeypatch.setattr(config, "HR_REVIEWS_FILE", review_file)
    monkeypatch.setattr(config, "STORAGE_FOLDER", tmp_path)

    row = dict.fromkeys(config.CANDIDATE_CSV_HEADERS, "")
    row["candidate_id"] = "CAN001"
    row["review_status"] = "Not reviewed"

    with open(candidate_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=config.CANDIDATE_CSV_HEADERS)
        writer.writeheader()
        writer.writerow(row)

    saved = update_candidate_review(
        "CAN001",
        "Shortlisted",
        "Strong project evidence",
    )

    assert saved is True

    with open(candidate_file, "r", newline="", encoding="utf-8") as file:
        updated_row = next(csv.DictReader(file))

    assert updated_row["review_status"] == "Shortlisted"
    assert updated_row["hr_notes"] == "Strong project evidence"
    assert review_file.exists()

