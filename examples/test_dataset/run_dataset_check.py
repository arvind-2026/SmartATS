from pathlib import Path
import sys


PROJECT_FOLDER = Path(__file__).parents[2]
sys.path.insert(0, str(PROJECT_FOLDER))

import config
from modules.contact_extractor import extract_candidate_contact
from modules.contact_extractor import load_name_ner_model
from modules.education_matcher import match_education
from modules.experience_matcher import match_experience
from modules.project_matcher import match_projects
from modules.resume_extractor import extract_resume_text
from modules.score_calculator import calculate_final_score
from modules.section_detector import detect_sections
from modules.semantic_matcher import load_sbert_model
from modules.semantic_matcher import match_semantic_requirements
from modules.skill_matcher import match_job_skills
from modules.text_cleaner import clean_resume_text


DATASET_FOLDER = Path(__file__).parent
REQUIRED_SKILLS = [
    "Python",
    "FastAPI",
    "Flask",
    "PostgreSQL",
    "Git",
    "Docker",
    "REST API",
    "Pytest",
]
PREFERRED_SKILLS = ["AWS", "Redis", "CI/CD", "GitHub Actions"]


def create_job():
    """Return the job dictionary used by this test dataset."""

    return {
        "job_description": (DATASET_FOLDER / "job_description.txt").read_text(
            encoding="utf-8"
        ),
        "required_skills": REQUIRED_SKILLS,
        "preferred_skills": PREFERRED_SKILLS,
        "required_experience": 2,
        "required_education": "Bachelor's degree in Computer Science",
        "semantic_weight": config.DEFAULT_SEMANTIC_WEIGHT,
        "skill_weight": config.DEFAULT_SKILL_WEIGHT,
        "project_weight": config.DEFAULT_PROJECT_WEIGHT,
        "experience_weight": config.DEFAULT_EXPERIENCE_WEIGHT,
        "education_weight": config.DEFAULT_EDUCATION_WEIGHT,
    }


def analyse_resume(pdf_path, job, sbert_model, name_model):
    """Run one dataset PDF through the complete SmartATS scoring pipeline."""

    extraction = extract_resume_text(pdf_path.name, pdf_path.read_bytes())

    if not extraction["success"]:
        return {
            "file": pdf_path.name,
            "error": extraction["message"],
        }

    clean_text = clean_resume_text(extraction["text"])
    section_result = detect_sections(clean_text)
    sections = section_result["sections"]
    contact = extract_candidate_contact(
        extraction["text"],
        pdf_path.name,
        name_model,
    )
    skill_result = match_job_skills(
        job["required_skills"],
        job["preferred_skills"],
        clean_text,
    )
    experience_text = sections.get("experience", clean_text)
    experience_result = match_experience(
        job["required_experience"],
        experience_text,
    )
    education_text = sections.get("education", clean_text)
    education_result = match_education(
        job["required_education"],
        education_text,
    )
    semantic_result = match_semantic_requirements(
        job["job_description"],
        sections,
        clean_text,
        sbert_model,
    )
    project_result = match_projects(
        job["job_description"],
        job["required_skills"],
        sections.get("projects", ""),
        sbert_model,
    )
    percentages = {
        "semantic": semantic_result["percentage"],
        "skills": skill_result["required"]["percentage"],
        "projects": project_result["percentage"],
        "experience": experience_result["percentage"],
        "education": education_result["percentage"],
    }
    score_result = calculate_final_score(percentages, job)

    return {
        "file": pdf_path.name,
        "name": contact["name"],
        "email": contact["email"],
        "phone": contact["phone"],
        "quality": extraction["quality"],
        "sections": ", ".join(section_result["detected_headings"]),
        "semantic": semantic_result["percentage"],
        "skills": skill_result["required"]["percentage"],
        "projects": project_result["percentage"],
        "experience": experience_result["percentage"],
        "education": education_result["percentage"],
        "overall": score_result["overall_score"],
        "category": score_result["category"],
    }


def main():
    """Analyse all dataset PDFs and print their descending score order."""

    print("Loading SBERT and spaCy models...")
    sbert_model = load_sbert_model()
    name_model = load_name_ner_model()
    job = create_job()
    results = []

    for pdf_path in sorted(DATASET_FOLDER.glob("*.pdf")):
        result = analyse_resume(pdf_path, job, sbert_model, name_model)
        results.append(result)

    results.sort(key=lambda item: item.get("overall", 0), reverse=True)

    print("\nSmartATS test dataset results")
    print("=" * 96)

    for rank, result in enumerate(results, start=1):
        if "error" in result:
            print(rank, result["file"], "ERROR:", result["error"])
            continue

        print(
            str(rank) + ".",
            result["name"],
            "| Overall:",
            result["overall"],
            "| Category:",
            result["category"],
        )
        print(
            "   Semantic:",
            result["semantic"],
            "Skills:",
            result["skills"],
            "Projects:",
            result["projects"],
            "Experience:",
            result["experience"],
            "Education:",
            result["education"],
        )
        print(
            "   Contact:",
            result["email"],
            "|",
            result["phone"],
            "| Quality:",
            result["quality"],
        )
        print("   Sections:", result["sections"] or "Paragraph analysis")


if __name__ == "__main__":
    main()

