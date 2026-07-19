import config
import matplotlib


matplotlib.use(config.MATPLOTLIB_BACKEND)

import matplotlib.pyplot as plt


def create_candidate_score_chart(candidates):
    """Create a bar chart comparing overall candidate scores."""

    chart_candidates = candidates[:config.MAX_CANDIDATES_IN_CHART]
    names = [candidate["candidate_name"] for candidate in chart_candidates]
    scores = [candidate["overall_score"] for candidate in chart_candidates]

    figure, axis = plt.subplots(
        figsize=(config.CHART_WIDTH, config.CHART_HEIGHT)
    )
    bars = axis.bar(names, scores, color=config.CHART_COLOR_PRIMARY)
    axis.set_title("Candidate Overall Score Comparison")
    axis.set_ylabel("Overall score (%)")
    axis.set_ylim(
        config.MINIMUM_DASHBOARD_SCORE,
        config.MAXIMUM_DASHBOARD_SCORE,
    )
    axis.tick_params(axis="x", rotation=45)
    axis.bar_label(bars, fmt="%.1f")
    figure.tight_layout()

    return figure


def create_score_distribution_chart(candidates):
    """Create a chart showing candidates in each match category."""

    labels = [
        config.STRONG_SCORE_LABEL,
        config.GOOD_SCORE_LABEL,
        config.PARTIAL_SCORE_LABEL,
        config.LOW_SCORE_LABEL,
    ]
    counts = dict.fromkeys(labels, 0)

    for candidate in candidates:
        score = candidate["overall_score"]

        if score >= config.STRONG_SCORE_LIMIT:
            counts[config.STRONG_SCORE_LABEL] += 1
        elif score >= config.GOOD_SCORE_LIMIT:
            counts[config.GOOD_SCORE_LABEL] += 1
        elif score >= config.PARTIAL_SCORE_LIMIT:
            counts[config.PARTIAL_SCORE_LABEL] += 1
        else:
            counts[config.LOW_SCORE_LABEL] += 1

    colors = [
        config.CHART_COLOR_SUCCESS,
        config.CHART_COLOR_PRIMARY,
        config.CHART_COLOR_WARNING,
        config.CHART_COLOR_DANGER,
    ]
    figure, axis = plt.subplots(
        figsize=(config.CHART_WIDTH, config.CHART_HEIGHT)
    )
    bars = axis.bar(labels, [counts[label] for label in labels], color=colors)
    axis.set_title("Candidate Match Distribution")
    axis.set_ylabel("Number of candidates")
    axis.bar_label(bars)
    axis.tick_params(axis="x", rotation=20)
    figure.tight_layout()

    return figure


def create_skill_availability_chart(candidates):
    """Create a horizontal chart of matched skills across candidates."""

    skill_counts = {}

    for candidate in candidates:
        for skill in candidate["matched_skills"]:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

    sorted_skills = sorted(
        skill_counts.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    sorted_skills = sorted_skills[:config.MAX_CANDIDATES_IN_CHART]
    names = [item[0] for item in sorted_skills]
    counts = [item[1] for item in sorted_skills]

    figure, axis = plt.subplots(
        figsize=(config.CHART_WIDTH, config.CHART_HEIGHT)
    )
    bars = axis.barh(names, counts, color=config.CHART_COLOR_SUCCESS)
    axis.set_title("Matched Skill Availability")
    axis.set_xlabel("Number of candidates")
    axis.bar_label(bars)
    axis.invert_yaxis()
    figure.tight_layout()

    return figure
