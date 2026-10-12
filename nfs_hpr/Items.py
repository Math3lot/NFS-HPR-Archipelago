from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from BaseClasses import Item, ItemClassification

from .Data import (
    GAME_NAME,
    ALL_EVENT_UNLOCK_ITEMS,
    ALL_VEHICLE_UNLOCK_ITEMS,
    ALL_WEAPON_ITEMS,
    WEAPON_MAX_LEVEL,
    STARTING_EVENT_UNLOCKS,
    BOUNTY_BUNDLE_ITEMS,
    BOUNTY_BUNDLE_WEIGHTS,
    NITRO_REFILL_ITEMS,
    NITRO_REFILL_WEIGHTS,
    FILLER_TYPE_WEIGHTS,
    TRAP_ITEMS,
    RACER_EVENT_UNLOCK_ITEMS,
    COP_EVENT_UNLOCK_ITEMS,
    RACER_VEHICLE_UNLOCK_ITEMS,
    COP_VEHICLE_UNLOCK_ITEMS,
    RACER_WEAPON_ITEMS,
    COP_WEAPON_ITEMS,
    ALL_SERIES_UNLOCK_ITEMS,
    RACER_SERIES_UNLOCK_ITEMS,
    COP_SERIES_UNLOCK_ITEMS,
    STARTING_SERIES_UNLOCKS,
)

if TYPE_CHECKING:
    from . import NFSHotPursuitWorld

ITEM_ID_START = 26_040_000


class NFSHotPursuitItem(Item):
    game = GAME_NAME


PROGRESSION_ITEMS = set(ALL_EVENT_UNLOCK_ITEMS + ALL_VEHICLE_UNLOCK_ITEMS + ALL_SERIES_UNLOCK_ITEMS)
USEFUL_ITEMS = set(ALL_WEAPON_ITEMS)
TRAP_SET = set(TRAP_ITEMS)

# This order is frozen: never reorder or remove entries once released,
# otherwise IDs change. Always append new items at the end.
ALL_ITEM_NAMES: List[str] = (
    ALL_EVENT_UNLOCK_ITEMS
    + ALL_VEHICLE_UNLOCK_ITEMS
    + ALL_WEAPON_ITEMS
    + BOUNTY_BUNDLE_ITEMS
    + NITRO_REFILL_ITEMS
    + TRAP_ITEMS
    + ALL_SERIES_UNLOCK_ITEMS
)

item_name_to_id: Dict[str, int] = {
    name: ITEM_ID_START + index for index, name in enumerate(ALL_ITEM_NAMES)
}

item_name_groups = {
    "Racer Events": set(RACER_EVENT_UNLOCK_ITEMS),
    "Cop Events": set(COP_EVENT_UNLOCK_ITEMS),
    "Racer Vehicles": set(RACER_VEHICLE_UNLOCK_ITEMS),
    "Cop Vehicles": set(COP_VEHICLE_UNLOCK_ITEMS),
    "Racer Weapons": set(RACER_WEAPON_ITEMS),
    "Cop Weapons": set(COP_WEAPON_ITEMS),
    "Bounty Bundles": set(BOUNTY_BUNDLE_ITEMS),
    "Nitro Refills": set(NITRO_REFILL_ITEMS),
    "Traps": set(TRAP_ITEMS),
    "Racer Series": set(RACER_SERIES_UNLOCK_ITEMS),
    "Cop Series": set(COP_SERIES_UNLOCK_ITEMS),
}


def get_item_classification(name: str) -> ItemClassification:
    if name in PROGRESSION_ITEMS:
        return ItemClassification.progression
    if name in USEFUL_ITEMS:
        return ItemClassification.useful
    if name in TRAP_SET:
        return ItemClassification.trap
    return ItemClassification.filler


def _weighted(random, weights: Dict[str, int]) -> str:
    return random.choices(list(weights), weights=list(weights.values()), k=1)[0]


def filler_type_weights(world: "NFSHotPursuitWorld") -> Dict[str, int]:
    weights = {"bounty": world.options.bounty_bundle_weight.value,
               "nitro": world.options.nitro_refill_weight.value}
    return weights if any(weights.values()) else {"bounty": 1}


def trap_weights(world: "NFSHotPursuitWorld") -> Dict[str, int]:
    o = world.options
    return {
        "Trap - Flat Tire": o.flat_tire_weight.value,
        "Trap - EMP Impact": o.emp_impact_weight.value,
        "Trap - Speed Limiter 10s": o.speed_limiter_weight.value,
        "Trap - Roadblock Deployed": o.roadblock_weight.value,
        "Trap - System Jammed": o.system_jammed_weight.value,
        "Trap - Reversed Steering": o.reversed_steering_weight.value,
    }


def get_random_filler_item(random, type_weights: Dict[str, int] = FILLER_TYPE_WEIGHTS) -> str:
    if _weighted(random, type_weights) == "bounty":
        return _weighted(random, BOUNTY_BUNDLE_WEIGHTS)
    return _weighted(random, NITRO_REFILL_WEIGHTS)


def create_item_pool(world: "NFSHotPursuitWorld", location_count: int) -> List[NFSHotPursuitItem]:
    names: List[str] = []

    if world.options.randomize_events:
        names += [n for n in ALL_EVENT_UNLOCK_ITEMS if n not in world.starting_events]

    if world.options.randomize_vehicles:
        names += [n for n in ALL_VEHICLE_UNLOCK_ITEMS if n not in world.starting_vehicles]
        names += [n for n in ALL_SERIES_UNLOCK_ITEMS if n not in world.starting_series]

    if world.options.randomize_weapons:
        for weapon in ALL_WEAPON_ITEMS:
            names += [weapon] * WEAPON_MAX_LEVEL

    remaining = location_count - len(names)
    if remaining < 0:
        raise Exception(
            f"{GAME_NAME}: {len(names)} required items but only {location_count} locations."
        )

    traps = {name: w for name, w in trap_weights(world).items() if w > 0}
    trap_count = remaining * world.options.trap_percentage.value // 100 if traps else 0
    names += [_weighted(world.random, traps) for _ in range(trap_count)]
    fillers = filler_type_weights(world)
    names += [get_random_filler_item(world.random, fillers) for _ in range(remaining - trap_count)]

    return [world.create_item(n) for n in names]
