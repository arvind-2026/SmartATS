import streamlit as st

import config
from modules.csv_manager import load_jobs
from modules.csv_manager import save_job
from modules.id_generator import create_job_id


def convert_skill_text_to_list(skill_text):
    """Convert comma-separated skill text into a clean list."""

    skills = []

    for skill in skill_text.split(config.SKILL_SEPARATOR):
        clean_skill = skill.strip()

        if clean_skill and clean_skill not in skills:
            skills.append(clean_skill)

    return skills


def check_job_form(job_title, job_description, required_skills, weights):
    """Check the job form and return a list of validation messages."""

    errors = []

    if not job_title.strip():
        errors.append("Please enter a job title.")

    if len(job_description.strip()) < config.MINIMUM_JOB_DESCRIPTION_LENGTH:
        errors.append(
            "The job description must contain at least "
            + str(config.MINIMUM_JOB_DESCRIPTION_LENGTH)
            + " characters."
        )

    if len(required_skills) == 0:
        errors.append("Please enter at least one required skill.")

    if sum(weights) != config.TOTAL_SCORE_WEIGHT:
        errors.append(
            "Scoring weights must total "
            + str(config.TOTAL_SCORE_WEIGHT)
            + "%. The current total is "
            + str(sum(weights))
            + "%."
        )

    return errors


st.title("Job Setup")
st.write("Enter the requirements that will be used to screen every candidate fairly.")

saved_jobs = load_jobs()

if saved_jobs:
    st.subheader("Open a saved job")
    saved_job_ids = [job["job_id"] for job in saved_jobs]
    selected_job_id = st.selectbox("Saved jobs", saved_job_ids)
    selected_job = next(
        job for job in saved_jobs if job["job_id"] == selected_job_id
    )
    st.write(selected_job["job_title"])

    if st.button("Use selected job"):
        st.session_state["current_job"] = selected_job
        st.success("Current job set to " + selected_job["job_id"] + ".")

if "current_job" in st.session_state:
    st.info(
        "Current job: "
        + st.session_state["current_job"]["job_id"]
        + " — "
        + st.session_state["current_job"]["job_title"]
    )

st.subheader("Create a new job")

with st.form("job_setup_form"):
    job_title = st.text_input("Job title")
    job_description = st.text_area("Job description", height=220)

    required_skill_text = st.text_input(
        "Required skills",
        placeholder="Python, SQL, Git",
        help="Separate skills with commas.",
    )

    preferred_skill_text = st.text_input(
        "Preferred skills",
        placeholder="Docker, AWS",
        help="Separate skills with commas.",
    )

    required_experience = st.number_input(
        "Minimum experience in years",
        min_value=0.0,
        step=0.5,
    )

    required_education = st.text_input(
        "Required education",
        placeholder="Bachelor's degree in Computer Science or related field",
    )

    st.subheader("Scoring weights")
    st.caption("All five weights must add up to 100%.")

    semantic_weight = st.number_input(
        "Semantic similarity",
        min_value=0,
        max_value=config.TOTAL_SCORE_WEIGHT,
        value=config.DEFAULT_SEMANTIC_WEIGHT,
    )
    skill_weight = st.number_input(
        "Required skills",
        min_value=0,
        max_value=config.TOTAL_SCORE_WEIGHT,
        value=config.DEFAULT_SKILL_WEIGHT,
    )
    project_weight = st.number_input(
        "Related projects",
        min_value=0,
        max_value=config.TOTAL_SCORE_WEIGHT,
        value=config.DEFAULT_PROJECT_WEIGHT,
    )
    experience_weight = st.number_input(
        "Experience",
        min_value=0,
        max_value=config.TOTAL_SCORE_WEIGHT,
        value=config.DEFAULT_EXPERIENCE_WEIGHT,
    )
    education_weight = st.number_input(
        "Education",
        min_value=0,
        max_value=config.TOTAL_SCORE_WEIGHT,
        value=config.DEFAULT_EDUCATION_WEIGHT,
    )

    save_button = st.form_submit_button("Save job")


if save_button:
    required_skills = convert_skill_text_to_list(required_skill_text)
    preferred_skills = convert_skill_text_to_list(preferred_skill_text)

    weights = [
        semantic_weight,
        skill_weight,
        project_weight,
        experience_weight,
        education_weight,
    ]

    errors = check_job_form(
        job_title,
        job_description,
        required_skills,
        weights,
    )

    if errors:
        for error in errors:
            st.error(error)
    else:
        job = {
            "job_id": create_job_id(),
            "job_title": job_title.strip(),
            "job_description": job_description.strip(),
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "required_experience": required_experience,
            "required_education": required_education.strip(),
            "semantic_weight": semantic_weight,
            "skill_weight": skill_weight,
            "project_weight": project_weight,
            "experience_weight": experience_weight,
            "education_weight": education_weight,
        }

        save_job(job)
        st.session_state["current_job"] = job
        st.success("Job " + job["job_id"] + " saved successfully.")
