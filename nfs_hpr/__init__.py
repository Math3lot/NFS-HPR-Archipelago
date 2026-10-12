from __future__ import annotations

from typing import Any, Dict, List

from BaseClasses import Item, ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, Type, components, launch as launch_component

from .Data import (
    GAME_NAME,
    STARTING_EVENT_UNLOCKS,
    STARTING_RACER_VEHICLE_CHOICES,
    STARTING_COP_VEHICLE_CHOICES,
    STARTING_SERIES_UNLOCKS,
    GOAL_LOCATION,
    VICTORY_ITEM,
    TRAP_DURATIONS,
    BOUNTY_BUNDLE_VALUES,
    NITRO_REFILL_VALUES,
)
from .Items import (
    NFSHotPursuitItem,
    item_name_to_id,
    item_name_groups,
    get_item_classification,
    filler_type_weights,
    get_random_filler_item,
    create_item_pool,
)
from .Locations import location_name_to_id, location_name_groups
from .Options import NFSHotPursuitOptions, option_groups
from .Regions import create_regions, get_active_locations
from .Rules import early_events, random_start_for, set_rules


def launch_client(*args: str) -> None:
    from .Client import launch
    launch_component(launch, name="NFSHPRClient", args=args)


components.append(Component("Need for Speed Hot Pursuit Remastered Client", "NFSHPRClient",
                            func=launch_client, component_type=Type.CLIENT))


class NFSHotPursuitWeb(WebWorld):
    theme = "partyTime"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide for setting up Need for Speed Hot Pursuit Remastered for Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Math3lot"],
        )
    ]
    option_groups = option_groups


class NFSHotPursuitWorld(World):
    """
    Need for Speed Hot Pursuit Remastered: Racers versus Cops across Seacrest County.
    Events, series, vehicles and weapons are scattered across the multiworld; medals,
    levels, series and unlocked vehicles are checks.
    """

    game = GAME_NAME
    web = NFSHotPursuitWeb()

    options_dataclass = NFSHotPursuitOptions
    options: NFSHotPursuitOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    starting_vehicles: List[str]
    starting_events: List[str]
    starting_series: List[str]

    def generate_early(self) -> None:
        events_randomized = bool(self.options.randomize_events)
        vehicles_randomized = bool(self.options.randomize_vehicles)
        extra = self.options.starting_events.value
        random_start = bool(self.options.random_start) and events_randomized and vehicles_randomized
        self.starting_vehicles, self.starting_events, self.starting_series = [], [], []
        for side, choices in (("Racer", STARTING_RACER_VEHICLE_CHOICES), ("Cop", STARTING_COP_VEHICLE_CHOICES)):
            if random_start:
                car, events, series = random_start_for(side, self.random, extra)
            else:
                car = self.random.choice(choices)
                events = [STARTING_EVENT_UNLOCKS[0 if side == "Racer" else 1].split(" - ", 1)[1]]
                events += early_events(side, choices[0], extra, vehicles_randomized)
                series = [s for s in STARTING_SERIES_UNLOCKS if s.startswith(f"Unlock {side} ")][0].split(" - ", 1)[1]
            self.starting_vehicles.append(f"Unlock {side} Vehicle - {car}")
            self.starting_events += [f"Unlock {side} Event - {e}" for e in events]
            self.starting_series.append(f"Unlock {side} Series - {series}")

        starting = []
        if events_randomized:
            starting += self.starting_events
        if vehicles_randomized:
            starting += self.starting_vehicles + self.starting_series
        for name in starting:
            self.multiworld.push_precollected(self.create_item(name))

    def create_regions(self) -> None:
        create_regions(self)

    def create_item(self, name: str) -> Item:
        if name == VICTORY_ITEM:
            return NFSHotPursuitItem(name, ItemClassification.progression, None, self.player)
        return NFSHotPursuitItem(name, get_item_classification(name), item_name_to_id[name], self.player)

    def create_items(self) -> None:
        self.multiworld.itempool += create_item_pool(self, len(get_active_locations(self)))
        self.get_location(GOAL_LOCATION).place_locked_item(self.create_item(VICTORY_ITEM))

    def get_filler_item_name(self) -> str:
        return get_random_filler_item(self.random, filler_type_weights(self))

    def set_rules(self) -> None:
        set_rules(self)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "goal": self.options.goal.value,
            "randomize_events": bool(self.options.randomize_events),
            "randomize_vehicles": bool(self.options.randomize_vehicles),
            "randomize_weapons": bool(self.options.randomize_weapons),
            "randomize_levels": bool(self.options.randomize_levels),
            "trap_durations": TRAP_DURATIONS,
            "bounty_bundle_values": BOUNTY_BUNDLE_VALUES,
            "nitro_refill_values": NITRO_REFILL_VALUES,
        }
