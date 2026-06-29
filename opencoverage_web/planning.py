"""Planning helpers for the web UI."""

from __future__ import annotations

import tempfile
from pathlib import Path

from opencoverage.io.survey_input import read_survey_map
from opencoverage.models import FlightMission
from opencoverage.planner import plan


def plan_from_uploads(
    polygon_bytes: bytes,
    polygon_name: str,
    config_bytes: bytes | None,
    config_name: str | None,
    *,
    gpu: bool = False,
    split: bool = False,
) -> tuple[list[FlightMission], Path]:
    """
    Run mission planning from uploaded file contents.

    Returns the mission list and the path to a temporary directory holding
    the uploaded files (caller should clean up when done).
    """
    suffix = Path(polygon_name).suffix.lower()
    if suffix not in {".kml", ".kmz", ".poly", ".txt"}:
        raise ValueError("Polygon file must be .kml, .kmz, .poly, or .txt")

    tmp_dir = Path(tempfile.mkdtemp(prefix="opencoverage_web_"))
    polygon_path = tmp_dir / Path(polygon_name).name
    polygon_path.write_bytes(polygon_bytes)

    config_path: Path | None = None
    if config_bytes is not None and config_name:
        config_path = tmp_dir / Path(config_name).name
        config_path.write_bytes(config_bytes)

    result = plan(
        polygon=polygon_path,
        config=config_path,
        gpu=gpu,
        split=split,
    )
    missions = result if isinstance(result, list) else [result]
    return missions, tmp_dir


def load_survey_polygon(polygon_path: Path):
    """Load the survey polygon from a file on disk."""
    return read_survey_map(polygon_path).polygon


def mission_to_qgc_bytes(mission: FlightMission) -> bytes:
    """Serialize a mission as QGroundControl waypoint file bytes."""
    reference = mission.reference
    if reference is None:
        raise ValueError("Mission is missing a geodetic reference point.")

    tmp = Path(tempfile.mkstemp(suffix=".waypoints")[1])
    try:
        mission.save_qgc(tmp, reference=reference)
        return tmp.read_bytes()
    finally:
        tmp.unlink(missing_ok=True)
