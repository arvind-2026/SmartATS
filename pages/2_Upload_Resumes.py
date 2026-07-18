import streamlit as st

import config
from modules.file_validator import validate_file
from modules.file_validator import validate_file_count


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

            st.caption("Text extraction will be added in the next project step.")

