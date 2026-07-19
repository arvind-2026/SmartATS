import config


def build_component_calculation(component):
    """Build a readable formula for one score component."""

    return (
        str(component["percentage"])
        + "% × "
        + str(component["weight"])
        + " / "
        + str(config.PERCENT_DIVISOR)
        + " = "
        + str(component["points"])
        + " points"
    )


def build_score_explanation(score_result):
    """Add readable formulas to a successful score result."""

    explanations = []

    for component in score_result["components"]:
        explanations.append({
            "label": component["label"],
            "percentage": component["percentage"],
            "weight": component["weight"],
            "points": component["points"],
            "calculation": build_component_calculation(component),
        })

    return explanations

