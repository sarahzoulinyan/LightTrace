"""Utilities for loading geographic coordinate boundary files."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable


def parse_coordinate_lines(lines: Iterable[str]) -> list[tuple[float, float]]:
    """Parse ``(latitude, longitude)`` records from an iterable of lines."""

    coordinates: list[tuple[float, float]] = []

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        value = line.removesuffix(",").strip()
        value = value.removeprefix("(").removesuffix(")")
        parts = [part.strip() for part in value.split(",")]
        if len(parts) != 2:
            raise ValueError(
                f"Invalid coordinate on line {line_number}: expected two values"
            )

        try:
            latitude, longitude = (float(part) for part in parts)
        except ValueError as exc:
            raise ValueError(
                f"Invalid coordinate on line {line_number}: values must be numeric"
            ) from exc

        if not math.isfinite(latitude) or not math.isfinite(longitude):
            raise ValueError(
                f"Invalid coordinate on line {line_number}: values must be finite"
            )
        if not -90 <= latitude <= 90:
            raise ValueError(
                f"Invalid coordinate on line {line_number}: latitude out of range"
            )
        if not -180 <= longitude <= 180:
            raise ValueError(
                f"Invalid coordinate on line {line_number}: longitude out of range"
            )

        coordinates.append((latitude, longitude))

    if not coordinates:
        raise ValueError("Coordinate file contains no coordinate records")

    return coordinates


def load_coordinates(path: str | Path) -> list[tuple[float, float]]:
    """Load and parse a UTF-8 coordinate boundary file."""

    with Path(path).open(encoding="utf-8") as coordinate_file:
        return parse_coordinate_lines(coordinate_file)
