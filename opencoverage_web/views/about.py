"""About page with project background and attribution."""

from __future__ import annotations

import streamlit as st

from opencoverage_web import APP_NAME

CITATION = (
    "Vasquez-Gomez, J. I., Marciano-Melchor, M., Valentin, L., & Herrera-Lozada, J. C. (2020). "
    "Coverage path planning for 2d convex regions. "
    "*Journal of Intelligent & Robotic Systems*, 97(1), 81–94."
)


def render() -> None:
    """Render the About page."""
    st.title(f"About {APP_NAME}")

    st.markdown(
        f"""
        **{APP_NAME}** is a web application for **coverage path planning** designed to
        **compare route-planning algorithms** for aerial surveying. The tool implements
        several algorithms from the literature so users can upload a survey area,
        configure flight and sensor parameters, and evaluate how different planning
        strategies perform on the same mission.
        """
    )

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Implementation project")
        st.markdown(
            f"""
            - **App:** {APP_NAME}
            - **Library:** OpenCoverage
            - **Purpose:** Open-source implementation and comparison of coverage
              path planning methods for UAV missions
            - **Features:** Multiple sweep patterns, camera overlap control,
              mission splitting, and QGroundControl export
            - **License:** [MIT License](https://opensource.org/licenses/MIT)
            """
        )

        st.subheader("Research background")
        st.markdown(
            """
            The underlying research originates from work on systematic coverage of
            2D convex regions for autonomous aerial surveying. This web interface
            builds on that line of research by making algorithm comparison accessible
            through an interactive planner.
            """
        )

    with col_right:
        st.subheader("Reference")
        st.markdown(CITATION)

        st.subheader("Developer")
        st.markdown(
            """
            - **Name:** Juan Irving Vasquez
            - **Affiliation:** Instituto Politécnico Nacional
            - **Website:** [jivg.org](https://jivg.org)
            """
        )

        st.subheader("Links")
        st.markdown(
            f"""
            - [OpenCoverage library (GitHub)](https://github.com/irvingvasquez/opencoverage)
            - [{APP_NAME} (GitHub)](https://github.com/irvingvasquez/opencoverage-web)
            """
        )

    st.divider()

    st.markdown(
        """
        ### Supported planning patterns

        | Pattern | Description |
        |---------|-------------|
        | Back-and-forth | Standard boustrophedon sweep |
        | Long edge | Sweep lines perpendicular to the longest polygon edge |
        | Optimal sweep | Minimize horizontal sweep width over rotation angles |
        | Following wind | Align sweeps with meteorological wind direction |

        Use the **Planner** page to upload a polygon and configuration file, select a
        pattern in your INI settings, and compare the resulting flight paths on the map.
        """
    )
