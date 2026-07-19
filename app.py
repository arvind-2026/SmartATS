import streamlit as st

import config


st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.PAGE_LAYOUT,
)

st.title(config.APP_NAME)
st.subheader(config.APP_SUBTITLE)
st.write(config.APP_DESCRIPTION)
st.info(config.RESPONSIBLE_AI_MESSAGE)

st.subheader("How to use SmartATS")
st.markdown(
    """
1. Create or reopen a job in **Job Setup**.
2. Upload and validate resumes in **Upload Resumes**.
3. Review extracted text and detected evidence.
4. Run semantic analysis and verify the score calculation.
5. Save candidate results for the HR Dashboard.
6. Compare candidates and record the final human review.
"""
)

st.subheader("Important principle")
st.write(
    "No score without calculation, no calculation without evidence, "
    "and no automated rejection."
)

st.warning(
    "Candidate names, email addresses, phone numbers, photographs, addresses, "
    "and other personal details are not used in scoring."
)
