"""Streamlit entry point for OpenCoverage web UI."""

from __future__ import annotations

import streamlit as st

from opencoverage_web.views import about, planner

st.set_page_config(
    page_title="OpenCoverage",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    div[data-testid="stSidebarNav"] {padding-top: 1rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

page = st.navigation(
    [
        st.Page(
            planner.render,
            title="Planner",
            icon="🛸",
            default=True,
            url_path="planner",
        ),
        st.Page(
            about.render,
            title="About",
            icon="ℹ️",
            url_path="about",
        ),
    ]
)
page.run()
