import pandas as pd
import streamlit as st

import config
from modules.chart_maker import create_candidate_score_chart
from modules.chart_maker import create_component_comparison_chart
from modules.chart_maker import create_score_distribution_chart
from modules.chart_maker import create_skill_availability_chart
from modules.csv_exporter import create_candidate_export
from modules.csv_manager import load_candidates
from modules.csv_manager import load_jobs


def join_skill_list(skills):
    """Prepare skill lists for dashboard table display."""

    return ", ".join(skills)


st.title("HR Dashboard")
st.caption(config.RESPONSIBLE_AI_MESSAGE)

candidates = load_candidates()
jobs = load_jobs()

if not candidates:
    st.info("No saved candidate results are available yet.")
else:
    job_titles = {}

    for job in jobs:
        job_titles[job["job_id"]] = job["job_title"]

    job_options = [config.ALL_FILTER_OPTION]

    for candidate in candidates:
        job_id = candidate["job_id"]

        if job_id not in job_options:
            job_options.append(job_id)

    selected_job = st.selectbox(
        "Job",
        job_options,
        format_func=lambda job_id: (
            config.ALL_FILTER_OPTION
            if job_id == config.ALL_FILTER_OPTION
            else job_id + " — " + job_titles.get(job_id, "Saved job")
        ),
    )
    minimum_score = st.slider(
        "Minimum overall score",
        min_value=config.MINIMUM_DASHBOARD_SCORE,
        max_value=config.MAXIMUM_DASHBOARD_SCORE,
        value=config.MINIMUM_DASHBOARD_SCORE,
        step=config.DASHBOARD_SCORE_STEP,
    )
    selected_status = st.selectbox(
        "Review status",
        [config.ALL_FILTER_OPTION] + config.REVIEW_STATUSES,
    )
    required_skill_filter = st.text_input("Matched skill contains")

    filtered_candidates = []

    for candidate in candidates:
        if selected_job != config.ALL_FILTER_OPTION:
            if candidate["job_id"] != selected_job:
                continue

        if candidate["overall_score"] < minimum_score:
            continue

        if selected_status != config.ALL_FILTER_OPTION:
            if candidate["review_status"] != selected_status:
                continue

        if required_skill_filter.strip():
            matched_text = " ".join(candidate["matched_skills"]).lower()

            if required_skill_filter.lower().strip() not in matched_text:
                continue

        filtered_candidates.append(candidate)

    filtered_candidates.sort(
        key=lambda candidate: candidate["overall_score"],
        reverse=True,
    )

    for index in range(len(filtered_candidates)):
        filtered_candidates[index]["rank"] = index + 1

    total_candidates = len(candidates)
    displayed_candidates = len(filtered_candidates)
    strong_candidates = 0

    for candidate in filtered_candidates:
        if candidate["overall_score"] >= config.STRONG_SCORE_LIMIT:
            strong_candidates += 1

    column_one, column_two, column_three = st.columns(3)
    column_one.metric("Saved candidates", total_candidates)
    column_two.metric("Displayed candidates", displayed_candidates)
    column_three.metric("Strong matches", strong_candidates)

    if not filtered_candidates:
        st.warning("No candidates match the selected filters.")
    else:
        table_rows = []

        for candidate in filtered_candidates:
            row = candidate.copy()
            row["matched_skills"] = join_skill_list(candidate["matched_skills"])
            row["missing_skills"] = join_skill_list(candidate["missing_skills"])
            table_rows.append(row)

        dashboard_table = pd.DataFrame(table_rows)
        dashboard_table = dashboard_table[config.DASHBOARD_TABLE_COLUMNS]
        st.subheader("Candidate ranking")
        st.dataframe(dashboard_table, hide_index=True, use_container_width=True)

        st.subheader("Score visualisations")
        st.pyplot(create_candidate_score_chart(filtered_candidates))
        st.pyplot(create_component_comparison_chart(filtered_candidates))
        st.pyplot(create_score_distribution_chart(filtered_candidates))

        has_matched_skills = any(
            candidate["matched_skills"] for candidate in filtered_candidates
        )

        if has_matched_skills:
            st.pyplot(create_skill_availability_chart(filtered_candidates))

        export_text = create_candidate_export(filtered_candidates)
        st.download_button(
            "Export filtered candidates as CSV",
            data=export_text,
            file_name=config.CSV_EXPORT_FILE_NAME,
            mime="text/csv",
        )
