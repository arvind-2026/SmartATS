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
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Git",
    "REST API",
    "Responsive Design",
    "Jest",
]
PREFERRED_SKILLS = ["TypeScript", "Redux", "Figma"]


def create_job():
    """Return the job dictionary used by the TXT test dataset."""

    return {
        "job_description": (DATASET_FOLDER / "job_description.txt").read_text(encoding="utf-8"),
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


def analyse_resume(txt_path, job, sbert_model, name_model):
    """Run one TXT resume through the complete SmartATS scoring pipeline."""

    extraction = extract_resume_text(txt_path.name, txt_path.read_bytes())
    if not extraction["success"]:
        return {"file": txt_path.name, "error": extraction["message"]}

    clean_text = clean_resume_text(extraction["text"])
    section_result = detect_sections(clean_text)
    sections = section_result["sections"]
    contact = extract_candidate_contact(extraction["text"], txt_path.name, name_model)
    skills = match_job_skills(job["required_skills"], job["preferred_skills"], clean_text)
    experience = match_experience(job["required_experience"], sections.get("experience", clean_text))
    education = match_education(job["required_education"], sections.get("education", clean_text))
    semantic = match_semantic_requirements(job["job_description"], sections, clean_text, sbert_model)
    projects = match_projects(job["job_description"], job["required_skills"], sections.get("projects", ""), sbert_model)
    percentages = {
        "semantic": semantic["percentage"],
        "skills": skills["required"]["percentage"],
        "projects": projects["percentage"],
        "experience": experience["percentage"],
        "education": education["percentage"],
    }
    score = calculate_final_score(percentages, job)

    return {
        "file": txt_path.name,
        "name": contact["name"],
        "email": contact["email"],
        "phone": contact["phone"],
        "quality": extraction["quality"],
        "sections": ", ".join(section_result["detected_headings"]),
        "semantic": semantic["percentage"],
        "skills": skills["required"]["percentage"],
        "projects": projects["percentage"],
        "experience": experience["percentage"],
        "education": education["percentage"],
        "overall": score["overall_score"],
        "category": score["category"],
    }


def main():
    """Analyse all TXT resumes and print their descending score order."""

    print("Loading SBERT and spaCy models...")
    sbert_model = load_sbert_model()
    name_model = load_name_ner_model()
    job = create_job()
    results = []

    for txt_path in sorted(DATASET_FOLDER.glob("*.txt")):
        if txt_path.name != "job_description.txt":
            results.append(analyse_resume(txt_path, job, sbert_model, name_model))

    results.sort(key=lambda item: item.get("overall", 0), reverse=True)
    print("\nSmartATS TXT test dataset results")
    print("=" * 96)

    for rank, result in enumerate(results, start=1):
        if "error" in result:
            print(rank, result["file"], "ERROR:", result["error"])
            continue
        print(str(rank) + ".", result["name"], "| Overall:", result["overall"], "| Category:", result["category"])
        print("   Semantic:", result["semantic"], "Skills:", result["skills"], "Projects:", result["projects"], "Experience:", result["experience"], "Education:", result["education"])
        print("   Contact:", result["email"], "|", result["phone"], "| Quality:", result["quality"])
        print("   Sections:", result["sections"] or "Paragraph analysis")


if __name__ == "__main__":
    main()

