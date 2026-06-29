"""Folium map helpers for mission visualization."""

from __future__ import annotations

import folium
from shapely.geometry import Polygon

from opencoverage.io.coords import local_to_geodetic, path_to_geodetics
from opencoverage.models import FlightMission, GeodeticCoordinate


def _latlng(geo: GeodeticCoordinate) -> tuple[float, float]:
    return (geo.latitude, geo.longitude)


def polygon_to_latlngs(polygon: Polygon, reference: GeodeticCoordinate) -> list[tuple[float, float]]:
    """Convert a local-meter polygon exterior to lat/lon pairs."""
    return [
        _latlng(local_to_geodetic(x, y, reference))
        for x, y in polygon.exterior.coords[:-1]
    ]


def build_mission_map(
    *,
    polygon: Polygon,
    mission: FlightMission,
    segment_index: int | None = None,
) -> folium.Map:
    """Build a Folium map showing the survey polygon and planned path."""
    reference = mission.reference
    if reference is None:
        raise ValueError("Mission is missing a geodetic reference point.")

    boundary = polygon_to_latlngs(polygon, reference)
    path = [
        _latlng(geo)
        for geo in path_to_geodetics(mission.path, reference, mission.flight_height)
    ]

    center = boundary[0] if boundary else (reference.latitude, reference.longitude)
    title_suffix = f" (segment {segment_index})" if segment_index is not None else ""
    mission_map = folium.Map(location=center, zoom_start=16, tiles="OpenStreetMap")

    folium.Polygon(
        locations=boundary,
        color="#2563eb",
        weight=2,
        fill=True,
        fill_color="#93c5fd",
        fill_opacity=0.25,
        popup=f"Survey area{title_suffix}",
    ).add_to(mission_map)

    if len(path) >= 2:
        folium.PolyLine(
            locations=path,
            color="#dc2626",
            weight=3,
            opacity=0.85,
            popup=f"Flight path ({len(path)} waypoints)",
        ).add_to(mission_map)

    if mission.home is not None:
        folium.Marker(
            _latlng(mission.home),
            popup="Home",
            icon=folium.Icon(color="green", icon="home"),
        ).add_to(mission_map)

    if mission.takeoff is not None:
        folium.Marker(
            _latlng(mission.takeoff),
            popup="Takeoff",
            icon=folium.Icon(color="blue", icon="plane"),
        ).add_to(mission_map)

    mission_map.fit_bounds(boundary)
    return mission_map
