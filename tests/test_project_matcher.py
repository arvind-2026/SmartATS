import torch

from modules.project_matcher import calculate_project_percentage
from modules.project_matcher import calculate_project_relevance
from modules.project_matcher import create_project_chunks


def test_create_project_chunks():
    project_text = (
        "Created an AI resume screening system using Python and SBERT. "
        "Built a Streamlit dashboard for HR users."
    )

    chunks = create_project_chunks(project_text)

    assert len(chunks) == 2


def test_select_best_two_project_chunks():
    chunks = ["Project one", "Project two", "Project three"]
    similarities = torch.tensor([0.80, 0.60, 0.20])

    result = calculate_project_relevance(chunks, similarities)

    assert len(result["evidence"]) == 2
    assert result["percentage"] == 70


def test_project_similarity_below_limit_adds_no_score():
    result = calculate_project_relevance(
        ["Unrelated project"],
        torch.tensor([0.20]),
    )

    assert result["percentage"] == 0


def test_combine_project_scores():
    result = calculate_project_percentage(80, 60)

    assert result == 73.33


def test_empty_project_text():
    assert create_project_chunks("") == []

