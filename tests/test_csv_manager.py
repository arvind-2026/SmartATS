import csv

import config
from modules.csv_manager import candidate_already_saved
from modules.csv_manager import convert_list_to_text
from modules.csv_manager import save_candidate


def test_convert_list_to_text():
    skills = ["Python", "SQL", "Git"]

    result = convert_list_to_text(skills)

    assert result == "Python; SQL; Git"


def test_convert_empty_list_to_text():
    result = convert_list_to_text([])

    assert result == ""


def test_save_and_find_candidate(tmp_path, monkeypatch):
    candidate_file = tmp_path / "candidates.csv"
    monkeypatch.setattr(config, "CANDIDATES_FILE", candidate_file)
    monkeypatch.setattr(config, "STORAGE_FOLDER", tmp_path)

    candidate = {
        "candidate_id": "CAN001",
        "job_id": "JOB001",
        "candidate_name": "Candidate A",
        "candidate_email": "candidate@example.com",
        "candidate_phone": "+91 98765 43210",
        "file_name": "candidate_a.pdf",
        "semantic_score": 80,
        "skill_score": 75,
        "project_score": 70,
        "experience_score": 100,
        "education_score": 100,
        "overall_score": 80,
        "matched_skills": ["Python", "SQL"],
        "missing_skills": ["Docker"],
        "extraction_quality": "High",
        "review_status": "Not reviewed",
        "hr_notes": "",
    }

    save_candidate(candidate)

    assert candidate_already_saved("JOB001", "candidate_a.pdf") is True

    with open(candidate_file, "r", newline="", encoding="utf-8") as file:
        row = next(csv.DictReader(file))

    assert row["matched_skills"] == "Python; SQL"


def test_candidate_duplicate_is_job_specific(tmp_path, monkeypatch):
    candidate_file = tmp_path / "candidates.csv"
    monkeypatch.setattr(config, "CANDIDATES_FILE", candidate_file)
    candidate_file.write_text(
        "candidate_id,job_id,file_name\nCAN001,JOB001,resume.pdf\n",
        encoding="utf-8",
    )

    assert candidate_already_saved("JOB002", "resume.pdf") is False
