from modules.chart_maker import create_candidate_score_chart
from modules.chart_maker import create_score_distribution_chart
from modules.chart_maker import create_skill_availability_chart

import matplotlib.pyplot as plt


def create_candidates():
    return [
        {
            "candidate_name": "Candidate A",
            "overall_score": 80,
            "matched_skills": ["Python", "SQL"],
        },
        {
            "candidate_name": "Candidate B",
            "overall_score": 60,
            "matched_skills": ["Python"],
        },
    ]


def test_candidate_score_chart():
    figure = create_candidate_score_chart(create_candidates())

    assert len(figure.axes[0].patches) == 2
    plt.close(figure)


def test_score_distribution_chart():
    figure = create_score_distribution_chart(create_candidates())

    assert len(figure.axes[0].patches) == 4
    plt.close(figure)


def test_skill_availability_chart():
    figure = create_skill_availability_chart(create_candidates())

    assert len(figure.axes[0].patches) == 2
    plt.close(figure)
