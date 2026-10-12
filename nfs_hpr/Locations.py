from __future__ import annotations

from typing import Dict

from BaseClasses import Location

from .Data import (
    GAME_NAME,
    ALL_LOCATIONS,
    RACER_MEDAL_LOCATIONS,
    COP_MEDAL_LOCATIONS,
    RACER_LEVEL_LOCATIONS,
    COP_LEVEL_LOCATIONS,
    RACER_VEHICLE_LOCATIONS,
    COP_VEHICLE_LOCATIONS,
    RACER_SERIES_LOCATIONS,
    COP_SERIES_LOCATIONS,
)

LOCATION_ID_START = 26_040_000


class NFSHotPursuitLocation(Location):
    game = GAME_NAME


# Same rule as for items: never reorder, always append new locations at the end.
location_name_to_id: Dict[str, int] = {
    name: LOCATION_ID_START + index for index, name in enumerate(ALL_LOCATIONS)
}

location_name_groups = {
    "Racer Medals": set(RACER_MEDAL_LOCATIONS),
    "Cop Medals": set(COP_MEDAL_LOCATIONS),
    "Racer Levels": set(RACER_LEVEL_LOCATIONS),
    "Cop Levels": set(COP_LEVEL_LOCATIONS),
    "Racer Vehicles": set(RACER_VEHICLE_LOCATIONS),
    "Cop Vehicles": set(COP_VEHICLE_LOCATIONS),
    "Racer Series": set(RACER_SERIES_LOCATIONS),
    "Cop Series": set(COP_SERIES_LOCATIONS),
}
