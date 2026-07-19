import config


def get_score_category(score):
    """Return the configured category for an overall ATS score."""

    if score >= config.STRONG_SCORE_LIMIT:
        return config.STRONG_SCORE_LABEL

    if score >= config.GOOD_SCORE_LIMIT:
        return config.GOOD_SCORE_LABEL

    if score >= config.PARTIAL_SCORE_LIMIT:
        return config.PARTIAL_SCORE_LABEL

    return config.LOW_SCORE_LABEL


def validate_job_weights(job):
    """Check that all job scoring weights total the configured maximum."""

    total_weight = 0

    for component in config.SCORE_COMPONENTS:
        total_weight += job[component["weight_key"]]

    return total_weight == config.TOTAL_SCORE_WEIGHT, total_weight


def calculate_final_score(component_percentages, job):
    """Apply job weights and return every scoring calculation."""

    weights_are_valid, total_weight = validate_job_weights(job)

    if not weights_are_valid:
        return {
            "success": False,
            "overall_score": 0,
            "category": "",
            "components": [],
            "message": (
                "Scoring weights total "
                + str(total_weight)
                + "%. They must total "
                + str(config.TOTAL_SCORE_WEIGHT)
                + "%."
            ),
        }

    component_results = []
    overall_score = 0

    for component in config.SCORE_COMPONENTS:
        component_key = component["key"]
        percentage = component_percentages.get(component_key, 0)
        weight = job[component["weight_key"]]
        points = percentage * weight / config.PERCENT_DIVISOR
        points = round(points, config.ROUND_SCORE_DIGITS)
        overall_score += points

        component_results.append({
            "key": component_key,
            "label": component["label"],
            "percentage": percentage,
            "weight": weight,
            "points": points,
        })

    overall_score = round(overall_score, config.ROUND_SCORE_DIGITS)

    return {
        "success": True,
        "overall_score": overall_score,
        "category": get_score_category(overall_score),
        "components": component_results,
        "message": "Final score calculated successfully.",
    }

