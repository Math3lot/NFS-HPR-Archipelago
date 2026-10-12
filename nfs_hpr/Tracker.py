"""
What the player has unlocked so far (vehicles, series, events), for the client's
Tracker tab and the /tracker command.
"""
from __future__ import annotations

from typing import Dict, List, Set, Tuple

from .Data import COP_EVENTS_BY_SERIES, COP_VEHICLES_BY_UNIT, RACER_EVENTS_BY_SERIES, RACER_VEHICLES_BY_CLASS

SIDES: Tuple[Tuple[str, Dict[str, List[str]], Dict[str, List[str]]], ...] = (
    ("Racer", RACER_VEHICLES_BY_CLASS, RACER_EVENTS_BY_SERIES),
    ("Cop", COP_VEHICLES_BY_UNIT, COP_EVENTS_BY_SERIES),
)
UNLOCKED, LOCKED, HEADER = "66dd66", "808080", "ffcc44"


def _status(received: Set[str], randomized: bool, item: str) -> bool:
    return not randomized or item in received


def tracker_sections(received: Set[str], events_randomized: bool, vehicles_randomized: bool):
    """For each side and series: (side, series, series unlocked, [(vehicle, unlocked)], [(event, unlocked)])."""
    for side, vehicles_by_series, events_by_series in SIDES:
        for series, vehicles in vehicles_by_series.items():
            yield (
                side, series,
                _status(received, vehicles_randomized, f"Unlock {side} Series - {series}"),
                [(v, _status(received, vehicles_randomized, f"Unlock {side} Vehicle - {v}")) for v in vehicles],
                [(e, _status(received, events_randomized, f"Unlock {side} Event - {e}"))
                 for e in events_by_series.get(series, [])],
            )


def _colored(name: str, unlocked: bool) -> str:
    name = name.replace("&", "&amp;").replace("[", "&bl;").replace("]", "&br;")
    return f"[color={UNLOCKED if unlocked else LOCKED}]{name}[/color]"


def tracker_markup(received: Set[str], events_randomized: bool, vehicles_randomized: bool) -> str:
    """Kivy markup text for the Tracker tab."""
    lines = [f"[color={UNLOCKED}]Unlocked[/color]   [color={LOCKED}]Locked[/color]"]
    current_side = None
    for side, series, series_open, vehicles, events in tracker_sections(received, events_randomized,
                                                                        vehicles_randomized):
        if side != current_side:
            current_side = side
            lines.append(f"\n[size=22sp][b][color={HEADER}]{side.upper()}[/color][/b][/size]")
        lines.append(f"\n[b]{_colored(series, series_open)}[/b]  "
                     f"({'series unlocked' if series_open else 'series locked'})")
        got = sum(1 for _, u in vehicles if u)
        lines.append(f"  [b]Vehicles {got}/{len(vehicles)}:[/b] " + ", ".join(_colored(v, u) for v, u in vehicles))
        if events:
            got = sum(1 for _, u in events if u)
            lines.append(f"  [b]Events {got}/{len(events)}:[/b] " + ", ".join(_colored(e, u) for e, u in events))
    return "\n".join(lines)


def tracker_text(received: Set[str], events_randomized: bool, vehicles_randomized: bool, side_filter: str = "") -> List[str]:
    """Plain text lines for the /tracker command (unlocked items only, with counts)."""
    lines = []
    for side, series, series_open, vehicles, events in tracker_sections(received, events_randomized,
                                                                        vehicles_randomized):
        if side_filter and side.lower() != side_filter.lower():
            continue
        cars = [v for v, u in vehicles if u]
        evs = [e for e, u in events if u]
        lines.append(f"{side} {series} ({'unlocked' if series_open else 'LOCKED'}): "
                     f"{len(cars)}/{len(vehicles)} vehicles, {len(evs)}/{len(events)} events")
        if cars:
            lines.append("    Vehicles: " + ", ".join(cars))
        if evs:
            lines.append("    Events: " + ", ".join(evs))
    return lines
