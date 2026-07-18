import streamlit as st

import config
from modules.education_matcher import match_education
from modules.experience_matcher import match_experience
from modules.file_validator import validate_file
from modules.file_validator import validate_file_count
from modules.resume_extractor import extract_resume_text
from modules.section_detector import detect_sections
from modules.semantic_matcher import load_sbert_model
from modules.semantic_matcher import match_semantic_requirements
from modules.skill_matcher import match_job_skills
from modules.text_cleaner import clean_resume_text


st.title("Upload Resumes")
st.write("Upload candidate resumes for the selected job.")


@st.cache_resource
def get_cached_sbert_model():
    """Load SBERT once and reuse it for all uploaded resumes."""

    return load_sbert_model()

if "current_job" not in st.session_state:
    st.warning("Create or select a job before uploading resumes.")
else:
    current_job = st.session_state["current_job"]
    st.info("Current job: " + current_job["job_title"])

    uploaded_files = st.file_uploader(
        "Choose resume files",
        type=config.ALLOWED_FILE_TYPES,
        accept_multiple_files=True,
        help=(
            "Accepted formats: PDF, DOCX and TXT. Maximum size: "
            + str(config.MAX_FILE_SIZE_MB)
            + " MB per file."
        ),
    )

    if uploaded_files:
        count_is_valid, count_message = validate_file_count(len(uploaded_files))

        if not count_is_valid:
            st.error(count_message)
        else:
            valid_files = []

            for uploaded_file in uploaded_files:
                result = validate_file(uploaded_file.name, uploaded_file.size)

                if result["valid"]:
                    valid_files.append(uploaded_file)
                    st.success(uploaded_file.name + ": " + result["message"])
                else:
                    st.error(uploaded_file.name + ": " + result["message"])

            st.write(
                "Valid resumes: "
                + str(len(valid_files))
                + " of "
                + str(len(uploaded_files))
            )

            extract_button = st.button(
                "Extract resume text",
                disabled=len(valid_files) == 0,
            )

            if extract_button:
                extraction_results = []

                for valid_file in valid_files:
                    result = extract_resume_text(
                        valid_file.name,
                        valid_file.getvalue(),
                    )
                    extraction_results.append(result)

                st.session_state["extraction_results"] = extraction_results

    if "extraction_results" in st.session_state:
        st.subheader("Extraction results")

        for result in st.session_state["extraction_results"]:
            with st.expander(result["file_name"], expanded=True):
                st.write("Extraction quality: " + result["quality"])

                if result["success"]:
                    if result["quality"] == "Low":
                        st.warning(result["message"])
                    else:
                        st.success(result["message"])

                    edited_text = st.text_area(
                        "Extracted text preview",
                        value=result["text"],
                        height=config.TEXT_PREVIEW_HEIGHT,
                        key="preview_" + result["file_name"],
                    )

                    result["text"] = edited_text
                    clean_text = clean_resume_text(edited_text)
                    section_result = detect_sections(clean_text)
                    result["clean_text"] = clean_text
                    result["sections"] = section_result["sections"]

                    skill_result = match_job_skills(
                        current_job["required_skills"],
                        current_job["preferred_skills"],
                        clean_text,
                    )
                    result["skill_result"] = skill_result

                    if section_result["uses_paragraph_analysis"]:
                        st.info(
                            "No clear section headings were detected. "
                            "Paragraph-level analysis will be used."
                        )
                    else:
                        heading_text = ", ".join(
                            section_result["detected_headings"]
                        )
                        st.write("Detected sections: " + heading_text)

                    st.markdown("#### Required skill evidence")
                    required_result = skill_result["required"]

                    st.write(
                        "Required skill match: "
                        + str(required_result["percentage"])
                        + "%"
                    )

                    if required_result["evidence"]:
                        for evidence in required_result["evidence"]:
                            st.success(
                                evidence["skill"]
                                + " — Evidence: "
                                + evidence["evidence"]
                            )

                    if required_result["missing_skills"]:
                        missing_text = ", ".join(
                            required_result["missing_skills"]
                        )
                        st.warning("Not detected: " + missing_text)

                    preferred_result = skill_result["preferred"]

                    if current_job["preferred_skills"]:
                        st.markdown("#### Preferred skills")
                        st.write(
                            "Preferred skill match: "
                            + str(preferred_result["percentage"])
                            + "%"
                        )

                    experience_text = section_result["sections"].get(
                        "experience",
                        clean_text,
                    )
                    experience_result = match_experience(
                        current_job["required_experience"],
                        experience_text,
                    )
                    result["experience_result"] = experience_result

                    st.markdown("#### Experience evidence")
                    st.write(experience_result["message"])

                    if experience_result["evidence"]:
                        st.write(
                            "Detected date or duration evidence: "
                            + ", ".join(experience_result["evidence"])
                        )

                    education_text = section_result["sections"].get(
                        "education",
                        clean_text,
                    )
                    education_result = match_education(
                        current_job["required_education"],
                        education_text,
                    )
                    result["education_result"] = education_result

                    st.markdown("#### Education evidence")
                    st.write(education_result["status"])
                    st.write(
                        "Required level: "
                        + (education_result["required_level"] or "Not determined")
                    )
                    st.write(
                        "Detected level: "
                        + (education_result["detected_level"] or "Not detected")
                    )

                    semantic_button = st.button(
                        "Run semantic analysis",
                        key="semantic_" + result["file_name"],
                    )

                    semantic_key = "semantic_result_" + result["file_name"]

                    if semantic_button:
                        with st.spinner(config.MODEL_LOADING_MESSAGE):
                            model = get_cached_sbert_model()
                            semantic_result = match_semantic_requirements(
                                current_job["job_description"],
                                section_result["sections"],
                                clean_text,
                                model,
                            )
                            st.session_state[semantic_key] = semantic_result

                    if semantic_key in st.session_state:
                        semantic_result = st.session_state[semantic_key]
                        result["semantic_result"] = semantic_result
                        st.markdown("#### Semantic evidence")
                        st.write(
                            "Semantic match: "
                            + str(semantic_result["percentage"])
                            + "%"
                        )

                        for evidence in semantic_result["evidence"]:
                            st.write("**Job requirement:** " + evidence["requirement"])
                            st.write(
                                "**Résumé evidence:** "
                                + evidence["resume_evidence"]
                            )
                            st.caption(
                                evidence["label"]
                                + " match — "
                                + str(evidence["similarity"])
                                + "%"
                            )
                            st.divider()
                else:
                    st.error(result["message"])
