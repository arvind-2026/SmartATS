from modules.csv_exporter import create_candidate_export


def test_create_candidate_export():
    candidate = {
        "rank": 1,
        "candidate_id": "CAN001",
        "job_id": "JOB001",
        "candidate_name": "Jane Doe",
        "candidate_email": "jane@example.com",
        "candidate_phone": "+91 98765 43210",
        "file_name": "jane.pdf",
        "semantic_score": 80,
        "skill_score": 75,
        "project_score": 70,
        "experience_score": 100,
        "education_score": 100,
        "overall_score": 80,
        "matched_skills": ["Python", "SQL"],
        "missing_skills": ["Docker"],
        "extraction_quality": "High",
        "review_status": "Shortlisted",
        "hr_notes": "Review project evidence",
    }

    result = create_candidate_export([candidate])

    assert "candidate_email" in result
    assert "jane@example.com" in result
    assert "Python; SQL" in result

