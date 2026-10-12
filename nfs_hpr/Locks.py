"""
Locked events: the game does not know what Archipelago has unlocked, so when the
player starts an event they have not received (or whose series is locked, or in a
car they have not received, when vehicles are randomized), the
client holds their car still for as long as they stay in it.
"""
from __future__ import annotations

import threading
import time
from typing import Callable, List, Optional, Set, Tuple

from .Data import COP_EVENT_SERIES, COP_EVENT_VEHICLES, RACER_EVENT_SERIES, RACER_EVENT_VEHICLES
from .GameMemory import GameMemory
from .Traps import speed_of

TICK = 0.03
HOLD_SPEED = 1.0  # m/s: a locked car can only crawl
EVENT_SERIES = {"Racer": RACER_EVENT_SERIES, "Cop": COP_EVENT_SERIES}
EVENT_VEHICLES = {"Racer": RACER_EVENT_VEHICLES, "Cop": COP_EVENT_VEHICLES}


def missing_unlocks(event: dict, received: Set[str], events_randomized: bool, series_randomized: bool,
                    vehicle: Optional[Tuple[str, str]] = None) -> List[str]:
    """Items the player still needs for this event and car (empty list: allowed).
    vehicle: (side, name) of the car being driven, when known."""
    side, name = event["side"], event["name"]
    missing = []
    if events_randomized and f"Unlock {side} Event - {name}" not in received:
        missing.append(f"Unlock {side} Event - {name}")
    if series_randomized:
        series = EVENT_SERIES[side][name]
        if f"Unlock {side} Series - {series}" not in received:
            missing.append(f"Unlock {side} Series - {series}")
        if vehicle and vehicle[0] == side:
            # the car being driven, lent ones included, must have been received
            item = f"Unlock {side} Vehicle - {vehicle[1]}"
            if item not in received:
                missing.append(item)
        elif vehicle is None:
            # map check: the event needs at least one of its cars
            cars = EVENT_VEHICLES[side][name]
            if cars and not any(f"Unlock {side} Vehicle - {v}" in received for v in cars):
                missing.append(f"one of its cars ({', '.join(cars)})")
    return missing


def hold_car(memory: GameMemory, still_locked: Callable[[], bool], stop: threading.Event) -> None:
    """Keep the player's car stopped while the locked event is on screen."""
    while not stop.is_set() and still_locked():
        try:
            velocity = memory.read_velocity()
            speed = speed_of(velocity) if velocity else 0.0
            if speed > HOLD_SPEED:
                # crawl, not a dead stop: the game keeps working (pause menu, scripted sequences)
                memory.write_velocity(tuple(c * HOLD_SPEED / speed for c in velocity))
        except OSError:
            break
        time.sleep(TICK)
