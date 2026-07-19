import pandas as pd
import streamlit as st

import config
from modules.csv_manager import load_candidate_score_details
from modules.csv_manager import load_candidate_semantic_evidence
from modules.csv_manager import load_candidates
from modules.csv_manager import update_candidate_review


st.title("Candidate Details")
st.caption(config.RESPONSIBLE_AI_MESSAGE)

candidates = load_candidates()

if not candidates:
    st.info("No saved candidate results are available yet.")
else:
    candidate_ids = [candidate["candidate_id"] for candidate in candidates]
    selected_candidate_id = st.selectbox(
        "Select candidate",
        candidate_ids,
        format_func=lambda candidate_id: next(
            candidate["candidate_name"]
            + " — "
            + candidate_id
            for candidate in candidates
            if candidate["candidate_id"] == candidate_id
        ),
    )
    candidate = next(
        candidate
        for candidate in candidates
        if candidate["candidate_id"] == selected_candidate_id
    )

    st.header(candidate["candidate_name"])
    st.write("Email: " + (candidate["candidate_email"] or "Not detected"))
    st.write("Contact: " + (candidate["candidate_phone"] or "Not detected"))
    st.write("Résumé file: " + candidate["file_name"])
    st.write("Extraction quality: " + candidate["extraction_quality"])

    column_one, column_two, column_three = st.columns(3)
    column_one.metric("Overall score", str(candidate["overall_score"]) + "%")
    column_two.metric("Skill score", str(candidate["skill_score"]) + "%")
    column_three.metric("Project score", str(candidate["project_score"]) + "%")

    st.subheader("Skill evidence summary")
    st.success(
        "Matched skills: "
        + (", ".join(candidate["matched_skills"]) or "None detected")
    )
    st.warning(
        "Not detected: "
        + (", ".join(candidate["missing_skills"]) or "None")
    )

    score_details = load_candidate_score_details(selected_candidate_id)

    if score_details:
        st.subheader("Stored score calculations")
        st.dataframe(
            pd.DataFrame(score_details),
            hide_index=True,
            use_container_width=True,
        )

    evidence_items = load_candidate_semantic_evidence(selected_candidate_id)

    if evidence_items:
        st.subheader("Stored semantic evidence")

        for evidence in evidence_items:
            st.write("**Job requirement:** " + evidence["job_requirement"])
            st.write("**Résumé evidence:** " + evidence["resume_evidence"])
            st.caption("Similarity: " + evidence["similarity"] + "%")
            st.divider()

    st.subheader("HR review")
    current_status_index = config.REVIEW_STATUSES.index(
        candidate["review_status"]
    )
    review_status = st.selectbox(
        "Review status",
        config.REVIEW_STATUSES,
        index=current_status_index,
    )
    hr_notes = st.text_area("HR notes", value=candidate["hr_notes"])

    if st.button("Save HR review"):
        saved = update_candidate_review(
            selected_candidate_id,
            review_status,
            hr_notes.strip(),
        )

        if saved:
            st.success("HR review saved successfully.")
        else:
            st.error("Candidate review could not be saved.")

