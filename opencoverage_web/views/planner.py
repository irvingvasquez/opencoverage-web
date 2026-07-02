"""Planner page: upload inputs, run mission planning, view results."""

from __future__ import annotations

import shutil
from pathlib import Path

import streamlit as st
from shapely import wkt
from shapely.geometry import Polygon
from streamlit_folium import st_folium

from opencoverage_web.map_view import build_mission_map
from opencoverage_web.planning import load_survey_polygon, mission_to_qgc_bytes, plan_from_uploads


def _init_session_state() -> None:
    if "missions" not in st.session_state:
        st.session_state.missions = None
        st.session_state.survey_polygon_wkt = None
        st.session_state.plan_error = None


def _clear_results() -> None:
    st.session_state.missions = None
    st.session_state.survey_polygon_wkt = None
    st.session_state.plan_error = None


def render() -> None:
    """Render the mission planner page."""
    _init_session_state()

    st.title("Mission Planner")
    st.caption("Upload a survey polygon and configuration file to plan a UAV coverage mission.")

    with st.sidebar:
        st.header("Inputs")
        polygon_file = st.file_uploader(
            "Survey polygon",
            type=["kml", "kmz", "poly", "txt"],
            help="KML or Mission Planner .poly file defining the survey area.",
        )
        config_file = st.file_uploader(
            "Configuration (INI)",
            type=["ini"],
            help="UAV, camera, and planner settings.",
        )

        st.header("Options")
        use_gpu = st.checkbox("GPU (optimal sweep)", value=False, help="Use CuPy when available.")
        split_mission = st.checkbox(
            "Split by flight time",
            value=False,
            help="Split into segments using FlightTime from the INI file.",
        )
        plan_clicked = st.button("Plan mission", type="primary", use_container_width=True)
        if st.session_state.missions is not None:
            if st.button("Clear results", use_container_width=True):
                _clear_results()
                st.rerun()

    st.markdown(
        """
        Upload a **survey polygon** (KML or `.poly`) and an **INI configuration** file
        in the sidebar, then click **Plan mission** to compare coverage patterns and export
        QGroundControl waypoint files.
        """
    )

    if plan_clicked:
        _clear_results()
        if polygon_file is None:
            st.session_state.plan_error = "Upload a survey polygon file first."
        elif config_file is None:
            st.session_state.plan_error = "Upload an INI configuration file first."
        else:
            tmp_dir: Path | None = None
            try:
                with st.spinner("Planning mission…"):
                    missions, tmp_dir = plan_from_uploads(
                        polygon_file.getvalue(),
                        polygon_file.name,
                        config_file.getvalue(),
                        config_file.name,
                        gpu=use_gpu,
                        split=split_mission,
                    )
                    polygon_path = tmp_dir / polygon_file.name
                    survey_polygon = load_survey_polygon(polygon_path)
                    st.session_state.missions = missions
                    st.session_state.survey_polygon_wkt = survey_polygon.wkt
            except Exception as exc:
                st.session_state.plan_error = f"Planning failed: {exc}"
            finally:
                if tmp_dir is not None:
                    shutil.rmtree(tmp_dir, ignore_errors=True)

    if st.session_state.plan_error:
        st.error(st.session_state.plan_error)
    elif st.session_state.missions and st.session_state.survey_polygon_wkt:
        missions = st.session_state.missions
        survey_polygon = wkt.loads(st.session_state.survey_polygon_wkt)
        if not isinstance(survey_polygon, Polygon):
            st.error("Invalid survey polygon in session.")
        else:
            st.success(f"Planned {len(missions)} mission segment(s).")

            for index, mission in enumerate(missions, start=1):
                segment_label = f"Segment {index}" if len(missions) > 1 else "Mission"
                with st.expander(segment_label, expanded=len(missions) == 1):
                    col_map, col_stats = st.columns([2, 1])

                    with col_stats:
                        st.metric("Waypoints", len(mission.path))
                        st.metric("Flight height (m)", f"{mission.flight_height:.1f}")
                        st.metric("Capture rate (s)", f"{mission.capture_rate:.2f}")
                        if mission.flight_time_s:
                            st.metric("Est. flight time (s)", f"{mission.flight_time_s:.0f}")
                        st.metric("Forward spacing (m)", f"{mission.forward_distance:.1f}")
                        st.metric("Lateral spacing (m)", f"{mission.lateral_distance:.1f}")

                        qgc_bytes = mission_to_qgc_bytes(mission)
                        download_name = (
                            f"mission_{index}.waypoints"
                            if len(missions) > 1
                            else "mission.waypoints"
                        )
                        st.download_button(
                            label="Download QGC waypoints",
                            data=qgc_bytes,
                            file_name=download_name,
                            mime="text/plain",
                            use_container_width=True,
                            key=f"download_{index}",
                        )

                    with col_map:
                        segment_index = index if len(missions) > 1 else None
                        mission_map = build_mission_map(
                            polygon=survey_polygon,
                            mission=mission,
                            segment_index=segment_index,
                        )
                        st_folium(
                            mission_map,
                            width=None,
                            height=480,
                            returned_objects=[],
                            key=f"map_{index}",
                        )
    else:
        st.info("Configure inputs in the sidebar and click **Plan mission** to begin.")
