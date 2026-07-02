"""Available coverage planning algorithms exposed by the OpenCoverage library."""

from __future__ import annotations

from dataclasses import dataclass

from opencoverage.models import SearchPatternType


@dataclass(frozen=True)
class PatternOption:
    """UI metadata for a library search pattern."""

    key: str
    label: str
    description: str
    pattern_type: SearchPatternType


PATTERN_OPTIONS: tuple[PatternOption, ...] = (
    PatternOption(
        key="back_forth",
        label="Back-and-forth",
        description="Standard boustrophedon sweep.",
        pattern_type=SearchPatternType.BACK_AND_FORTH,
    ),
    PatternOption(
        key="long_edge",
        label="Long edge",
        description="Sweep lines perpendicular to the longest polygon edge.",
        pattern_type=SearchPatternType.LONG_EDGE,
    ),
    PatternOption(
        key="optimal_sweep",
        label="Optimal sweep",
        description="Minimize horizontal sweep width over rotation angles.",
        pattern_type=SearchPatternType.OPTIMAL_SWEEP,
    ),
    PatternOption(
        key="following_wind",
        label="Following wind",
        description="Align sweeps with wind direction from the INI file.",
        pattern_type=SearchPatternType.FOLLOWING_WIND,
    ),
)

PATTERN_BY_KEY = {option.key: option for option in PATTERN_OPTIONS}
