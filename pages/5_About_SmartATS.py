import streamlit as st

import config


st.title("About SmartATS")
st.write(
    "SmartATS is an educational AI-assisted resume screening and applicant "
    "tracking system. It compares resume evidence with one confirmed job "
    "configuration and supports, but does not replace, human hiring review."
)

st.subheader("How the AI works")
st.write(
    "Sentence-BERT converts job requirements and resume sentences into "
    "embeddings. Cosine similarity measures how closely their meanings align. "
    "SmartATS displays the strongest resume sentence for every requirement."
)
st.code(config.SBERT_MODEL_NAME)

st.subheader("Default scoring method")

for component in config.SCORE_COMPONENTS:
    weight = getattr(config, component["default_weight_key"])
    st.write(component["label"] + ": " + str(weight) + "%")

st.write(
    "HR can change the weights during job setup. The same saved weights are "
    "used for every candidate screened for that job."
)

st.subheader("Explainability")
st.markdown(
    """
- Each component displays its percentage, weight, and awarded points.
- Matched skills include the exact resume line used as evidence.
- Semantic results connect each job requirement with resume evidence.
- Project relevance and project technologies are scored separately.
- Extraction warnings remain visible for manual review.
"""
)

st.subheader("Privacy and fairness")
st.write(
    "Names, contact details, photographs, addresses, age, gender, religion, "
    "marital status, and nationality do not contribute to the score. Contact "
    "details are stored only to help HR identify and communicate with candidates."
)

st.subheader("Limitations")
st.markdown(
    """
- A similarity score does not prove job performance or candidate ability.
- Skills not written in a resume may be reported as not detected.
- Complex layouts and scanned documents can reduce extraction quality.
- Experience dates and education equivalence may require HR verification.
- The final hiring decision must always be made by qualified human reviewers.
"""
)

st.info(config.RESPONSIBLE_AI_MESSAGE)
