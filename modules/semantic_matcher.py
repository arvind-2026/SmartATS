import re

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

import config


def split_into_chunks(text, minimum_length):
    """Split text into useful lines and sentences for semantic comparison."""

    pieces = re.split(r"[\n.!?;]+", text)
    chunks = []

    for piece in pieces:
        clean_piece = " ".join(piece.strip().split())

        if len(clean_piece) >= minimum_length and clean_piece not in chunks:
            chunks.append(clean_piece)

    return chunks


def create_job_requirements(job_description):
    """Create a limited list of requirements from the job description."""

    requirements = split_into_chunks(
        job_description,
        config.MINIMUM_REQUIREMENT_LENGTH,
    )

    return requirements[:config.MAXIMUM_JOB_REQUIREMENTS]


def create_resume_chunks(sections, clean_text):
    """Create resume chunks while excluding separately scored sections."""

    included_text = []

    if sections:
        for section_name, section_text in sections.items():
            if section_name not in config.SEMANTIC_EXCLUDED_SECTIONS:
                included_text.append(section_text)
    else:
        included_text.append(clean_text)

    resume_text = "\n".join(included_text)
    chunks = split_into_chunks(
        resume_text,
        config.MINIMUM_RESUME_CHUNK_LENGTH,
    )

    return chunks[:config.MAXIMUM_RESUME_CHUNKS]


def load_sbert_model():
    """Load the configured Sentence-BERT model."""

    return SentenceTransformer(config.SBERT_MODEL_NAME)


def get_match_label(similarity):
    """Convert a semantic similarity value into an explainable label."""

    if similarity >= config.STRONG_MATCH_LIMIT:
        return "Strong"

    if similarity >= config.WEAK_MATCH_LIMIT:
        return "Moderate"

    if similarity >= config.NO_MATCH_LIMIT:
        return "Weak"

    return "No useful match"


def calculate_semantic_result(requirements, resume_chunks, similarity_matrix):
    """Build an explainable result from an SBERT similarity matrix."""

    evidence = []
    score_values = []

    for requirement_index in range(len(requirements)):
        row = similarity_matrix[requirement_index]
        best_index = int(row.argmax().item())
        similarity = float(row[best_index].item())
        similarity = max(0, min(similarity, 1))

        if similarity < config.NO_MATCH_LIMIT:
            score_value = 0
        else:
            score_value = similarity

        score_values.append(score_value)
        evidence.append({
            "requirement": requirements[requirement_index],
            "resume_evidence": resume_chunks[best_index],
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
        "number_of_requirements": len(requirements),
    }


def match_semantic_requirements(job_description, sections, clean_text, model):
    """Compare job requirements with resume chunks using SBERT."""

    requirements = create_job_requirements(job_description)
    resume_chunks = create_resume_chunks(sections, clean_text)

    if not requirements or not resume_chunks:
        return {
            "percentage": 0,
            "evidence": [],
            "number_of_requirements": len(requirements),
        }

    requirement_embeddings = model.encode(
        requirements,
        convert_to_tensor=True,
        show_progress_bar=config.SBERT_PROGRESS_BAR,
    )
    resume_embeddings = model.encode(
        resume_chunks,
        convert_to_tensor=True,
        show_progress_bar=config.SBERT_PROGRESS_BAR,
    )
    similarity_matrix = cos_sim(requirement_embeddings, resume_embeddings)

    return calculate_semantic_result(
        requirements,
        resume_chunks,
        similarity_matrix,
    )

