import torch

from modules.semantic_matcher import calculate_semantic_result
from modules.semantic_matcher import create_job_requirements
from modules.semantic_matcher import create_resume_chunks
from modules.semantic_matcher import get_match_label


def test_create_job_requirements():
    description = (
        "Build Python backend applications. "
        "Work closely with product and engineering teams."
    )

    requirements = create_job_requirements(description)

    assert len(requirements) == 2
    assert requirements[0] == "Build Python backend applications"


def test_exclude_project_section_from_general_semantic_match():
    sections = {
        "experience": "Developed Python web applications",
        "projects": "Created an AI resume screening project",
    }

    chunks = create_resume_chunks(sections, "")

    assert "Developed Python web applications" in chunks
    assert "Created an AI resume screening project" not in chunks


def test_calculate_semantic_result():
    requirements = ["Build backend applications", "Work with SQL databases"]
    resume_chunks = ["Created backend services", "Used SQL for reporting"]
    similarity_matrix = torch.tensor([
        [0.80, 0.20],
        [0.30, 0.70],
    ])

    result = calculate_semantic_result(
        requirements,
        resume_chunks,
        similarity_matrix,
    )

    assert result["percentage"] == 75
    assert result["evidence"][0]["resume_evidence"] == "Created backend services"


def test_similarity_below_limit_adds_no_score():
    result = calculate_semantic_result(
        ["Manage cloud infrastructure"],
        ["Created a sales report"],
        torch.tensor([[0.20]]),
    )

    assert result["percentage"] == 0
    assert result["evidence"][0]["label"] == "No useful match"


def test_semantic_match_labels():
    assert get_match_label(0.80) == "Strong"
    assert get_match_label(0.65) == "Moderate"
    assert get_match_label(0.45) == "Weak"
    assert get_match_label(0.20) == "No useful match"

