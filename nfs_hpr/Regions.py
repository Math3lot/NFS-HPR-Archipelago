from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from .Data import ALL_LOCATIONS, FREE_AT_START_LOCATIONS, GOAL_LOCATION, RACER_LEVEL_LOCATIONS, COP_LEVEL_LOCATIONS
from .Locations import NFSHotPursuitLocation, location_name_to_id

if TYPE_CHECKING:
    from . import NFSHotPursuitWorld

LEVEL_LOCATIONS = set(RACER_LEVEL_LOCATIONS + COP_LEVEL_LOCATIONS)


def get_active_locations(world: "NFSHotPursuitWorld") -> list[str]:
    """Locations that exist for this slot, depending on options."""
    return [name for name in ALL_LOCATIONS
            if name not in FREE_AT_START_LOCATIONS
            and (world.options.randomize_levels or name not in LEVEL_LOCATIONS)]


def create_regions(world: "NFSHotPursuitWorld") -> None:
    """
    A single region: Seacrest County is fully open, so access to checks
    is handled entirely by rules (event/series unlocks and levels).
    """
    menu = Region("Menu", world.player, world.multiworld)

    for name in get_active_locations(world):
        menu.locations.append(
            NFSHotPursuitLocation(world.player, name, location_name_to_id[name], menu)
        )

    # Event location (no ID) that holds the Victory item
    menu.locations.append(NFSHotPursuitLocation(world.player, GOAL_LOCATION, None, menu))

    world.multiworld.regions.append(menu)
