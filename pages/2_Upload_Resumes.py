import streamlit as st

import config
from modules.file_validator import validate_file
from modules.file_validator import validate_file_count
from modules.resume_extractor import extract_resume_text


st.title("Upload Resumes")
st.write("Upload candidate resumes for the selected job.")

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

                    st.text_area(
                        "Extracted text preview",
                        value=result["text"],
                        height=config.TEXT_PREVIEW_HEIGHT,
                        key="preview_" + result["file_name"],
                    )
                else:
                    st.error(result["message"])
