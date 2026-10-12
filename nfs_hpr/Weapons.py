"""
Progressive weapons, applied at the start of each event.

The game keeps one charge counter per weapon type for the whole event (player and
AI share the table, but each side has its own weapon types). For the player's side:

  0 items received   -> weapon blocked (0 charges)
  1 item             -> the event's normal charges
  2 / 3 / 4 items    -> +1 / +2 / +3 charges

Weapons the event does not offer are left alone. An event (re)start is detected by
a new event id, a charge going up (weapons never refill during an event) or the car
being moved back to the start; the starting charges are read as the car first moves. The game's own weapon levels
(power) still grow with successful hits, as in the normal game.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .Data import WEAPON_MAX_LEVEL

# Charge cell of each progressive weapon item.
WEAPON_CELL: Dict[str, int] = {
    "Progressive Cop Helicopter": 0,
    "Progressive Cop EMP": 1,
    "Progressive Racer Spike Strip": 2,
    "Progressive Cop Spike Strip": 3,
    "Progressive Racer Turbo": 4,
    "Progressive Racer EMP": 5,
    "Progressive Racer Jammer": 7,
    "Progressive Cop Roadblock": 8,
}
SIDE_ITEMS = {
    "Racer": [name for name in WEAPON_CELL if name.startswith("Progressive Racer")],
    "Cop": [name for name in WEAPON_CELL if name.startswith("Progressive Cop")],
}


def weapon_levels(received_names: List[str]) -> Dict[str, int]:
    levels = {name: 0 for name in WEAPON_CELL}
    for name in received_names:
        if name in levels:
            levels[name] = min(WEAPON_MAX_LEVEL, levels[name] + 1)
    return levels


def side_cells(side: str) -> List[int]:
    return [WEAPON_CELL[name] for name in SIDE_ITEMS[side]]


def target_charges(side: str, start: List[int], levels: Dict[str, int]) -> Dict[int, int]:
    """Charges to write for the player's side, by cell, from the event's starting charges.
    Only weapons the event offers (starting charges above 0) are touched."""
    targets = {}
    for name in SIDE_ITEMS[side]:
        cell = WEAPON_CELL[name]
        if start[cell] <= 0:
            continue
        level = levels[name]
        targets[cell] = 0 if level == 0 else start[cell] + (level - 1)
    return targets
