"""
Turns a parsed save into the set of Archipelago locations it has completed.
Pure logic (no I/O, no network) so it can be tested on real save files.
"""
from __future__ import annotations

from typing import Dict, Iterable, Optional, Set, Tuple

from .Data import (
    LEVEL_BOUNTY,
    MAX_LEVEL,
    RACER_MEDAL_TIERS,
    COP_MEDAL_TIERS,
    RACER_VEHICLE_UNLOCKS,
    COP_VEHICLE_UNLOCKS,
    RACER_SERIES_UNLOCK_EVENT,
    COP_SERIES_UNLOCK_EVENT,
    RACER_FINAL_EVENT,
    COP_FINAL_EVENT,
    racer_medal_location,
    cop_medal_location,
)
from .EventsData import EVENTS, EVENTS_BY_ID
from .SaveReader import STAT_COP_BOUNTY, STAT_RACER_BOUNTY, Table, stat

GOLD, SILVER, BRONZE = 3, 2, 1


def medal_for(event: dict, row: dict) -> int:
    """Medal earned in one saved event result: 0 none, 1 bronze, 2 silver, 3 gold."""
    if not row.get("success"):
        return 0
    kind, targets = event["kind"], event["targets"]
    if kind == "position":
        return {1: GOLD, 2: SILVER, 3: BRONZE}.get(int(row.get("position", 0)), 0)
    if kind == "time":
        seconds = int(row.get("time", 0)) / 1_000_000
        gold, silver = targets[0], targets[1]
        if gold and seconds <= gold:
            return GOLD
        if silver and seconds <= silver:
            return SILVER
        return BRONZE
    if kind == "count":
        busts = int(row.get("busts", 0))
        gold, silver = targets[0], targets[1]
        if gold and busts >= gold:
            return GOLD
        if silver and busts >= silver:
            return SILVER
        return BRONZE
    return 0


def event_medals(tables: Dict[str, Table]) -> Dict[int, int]:
    """Best medal per event id found in the save."""
    best: Dict[int, int] = {}
    for row in tables["events"].rows:
        event = EVENTS_BY_ID.get(row.get("event_id"))
        if event:
            best[event["id"]] = max(best.get(event["id"], 0), medal_for(event, row))
    return best


def level_for_bounty(bounty: int) -> int:
    return sum(1 for threshold in LEVEL_BOUNTY if bounty >= threshold)


def completed_locations(tables: Dict[str, Table], levels_are_checks: bool = True,
                        bonus: Tuple[int, int] = (0, 0)) -> Set[str]:
    """bonus: (racer, cop) bounty from Bounty Bundles, which the save does not record."""
    medals = event_medals(tables)
    done: Set[str] = set()

    completed_names = {"Racer": set(), "Cop": set()}
    for event_id, medal in medals.items():
        event = EVENTS_BY_ID[event_id]
        side, name = event["side"], event["name"]
        if medal:
            completed_names[side].add(name)
        tiers = RACER_MEDAL_TIERS if side == "Racer" else COP_MEDAL_TIERS
        location = racer_medal_location if side == "Racer" else cop_medal_location
        for tier_index in range(medal):  # bronze..earned medal
            done.add(location(name, tiers[tier_index]))

    bounty = {"Racer": stat(tables, STAT_RACER_BOUNTY) + bonus[0], "Cop": stat(tables, STAT_COP_BOUNTY) + bonus[1]}

    if levels_are_checks:
        for side in ("Racer", "Cop"):
            for lvl in range(1, level_for_bounty(bounty[side]) + 1):
                done.add(f"{side} Level {lvl} Reached")

    for side, unlocks in (("Racer", RACER_VEHICLE_UNLOCKS), ("Cop", COP_VEHICLE_UNLOCKS)):
        for vehicle, condition in unlocks.items():
            if isinstance(condition, str):
                reached = condition in completed_names[side]
            else:
                reached = bounty[side] >= condition
            if reached:
                done.add(f"{side} Vehicle - {vehicle} Unlocked")

    for side, series_events in (("Racer", RACER_SERIES_UNLOCK_EVENT), ("Cop", COP_SERIES_UNLOCK_EVENT)):
        for series, unlock_event in series_events.items():
            if unlock_event is None or unlock_event in completed_names[side]:
                done.add(f"{side} Series - {series} Unlocked")

    return done


def goal_reached(tables: Dict[str, Table], goal: int, bonus: Tuple[int, int] = (0, 0)) -> bool:
    """goal values match Options.Goal: 0 all gold medals, 1 final events, 2 level 20 both."""
    medals = event_medals(tables)
    by_name = {(EVENTS_BY_ID[i]["side"], EVENTS_BY_ID[i]["name"]): m for i, m in medals.items()}
    if goal == 0:
        return all(by_name.get((e["side"], e["name"]), 0) == GOLD for e in EVENTS)
    if goal == 1:
        return by_name.get(("Racer", RACER_FINAL_EVENT), 0) > 0 and by_name.get(("Cop", COP_FINAL_EVENT), 0) > 0
    top = LEVEL_BOUNTY[MAX_LEVEL - 1]
    return stat(tables, STAT_RACER_BOUNTY) + bonus[0] >= top and stat(tables, STAT_COP_BOUNTY) + bonus[1] >= top
