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

