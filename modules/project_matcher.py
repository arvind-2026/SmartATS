from sentence_transformers.util import cos_sim

import config
from modules.semantic_matcher import get_match_label
from modules.semantic_matcher import split_into_chunks
from modules.skill_matcher import load_skill_aliases
from modules.skill_matcher import match_skill_list


def create_project_chunks(project_text):
    """Create meaningful project sentences for semantic comparison."""

    chunks = split_into_chunks(
        project_text,
        config.MINIMUM_RESUME_CHUNK_LENGTH,
    )

    return chunks[:config.MAXIMUM_PROJECT_CHUNKS]


def calculate_project_relevance(project_chunks, similarities):
    """Select the strongest project evidence and calculate relevance."""

    ranked_projects = []

    for index in range(len(project_chunks)):
        similarity = float(similarities[index].item())
        similarity = max(0, min(similarity, 1))
        ranked_projects.append({
            "project_evidence": project_chunks[index],
            "similarity_value": similarity,
        })

    ranked_projects.sort(
        key=lambda item: item["similarity_value"],
        reverse=True,
    )
    selected_projects = ranked_projects[:config.MAX_PROJECTS_FOR_SCORING]
    score_values = []
    evidence = []

    for project in selected_projects:
        similarity = project["similarity_value"]

        if similarity < config.NO_MATCH_LIMIT:
            score_values.append(0)
        else:
            score_values.append(similarity)

        evidence.append({
            "project_evidence": project["project_evidence"],
            "similarity": round(
                similarity * config.PERCENT_DIVISOR,
                config.ROUND_SCORE_DIGITS,
            ),
            "label": get_match_label(similarity),
        })

    if score_values:
        percentage = sum(score_values) / len(score_values)
        percentage = percentage * config.PERCENT_DIVISOR
    else:
        percentage = 0

    return {
        "percentage": round(percentage, config.ROUND_SCORE_DIGITS),
        "evidence": evidence,
    }


def calculate_project_percentage(relevance_percentage, technology_percentage):
    """Combine project relevance and technology evidence transparently."""

    relevance_value = relevance_percentage * config.PROJECT_RELEVANCE_POINTS
    technology_value = technology_percentage * config.PROJECT_TECHNOLOGY_POINTS
    percentage = (
        relevance_value + technology_value
    ) / config.PROJECT_COMPONENT_POINTS

    return round(percentage, config.ROUND_SCORE_DIGITS)


def match_projects(job_description, required_skills, project_text, model):
    """Measure project relevance and required technology evidence."""

    project_chunks = create_project_chunks(project_text)

    if not project_chunks:
        return {
            "percentage": 0,
            "relevance_percentage": 0,
            "technology_percentage": 0,
            "relevance_evidence": [],
            "technology_evidence": [],
            "matched_technologies": [],
            "message": "No project information was detected.",
        }

    job_embedding = model.encode(
        [job_description],
        convert_to_tensor=True,
        show_progress_bar=config.SBERT_PROGRESS_BAR,
    )
    project_embeddings = model.encode(
        project_chunks,
        convert_to_tensor=True,
        show_progress_bar=config.SBERT_PROGRESS_BAR,
    )
    similarities = cos_sim(job_embedding, project_embeddings)[0]
    relevance_result = calculate_project_relevance(
        project_chunks,
        similarities,
    )

    aliases = load_skill_aliases()
    technology_result = match_skill_list(
        required_skills,
        project_text,
        aliases,
    )
    percentage = calculate_project_percentage(
        relevance_result["percentage"],
        technology_result["percentage"],
    )

    return {
        "percentage": percentage,
        "relevance_percentage": relevance_result["percentage"],
        "technology_percentage": technology_result["percentage"],
        "relevance_evidence": relevance_result["evidence"],
        "technology_evidence": technology_result["evidence"],
        "matched_technologies": technology_result["matched_skills"],
        "message": "Project information was analysed.",
    }

