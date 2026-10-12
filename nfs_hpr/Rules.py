from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Dict, List

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

from .EventUnlocks import COP_EVENT_PREREQUISITES, RACER_EVENT_PREREQUISITES
from .Data import (
    FREE_AT_START_LOCATIONS,
    RACER_EVENTS,
    COP_EVENTS,
    RACER_MEDAL_TIERS,
    COP_MEDAL_TIERS,
    RACER_EVENT_SERIES,
    COP_EVENT_SERIES,
    RACER_EVENT_VEHICLES,
    COP_EVENT_VEHICLES,
    RACER_LOANED_VEHICLE_EVENTS,
    COP_LOANED_VEHICLE_EVENTS,
    RACER_VEHICLES_BY_CLASS,
    COP_VEHICLES_BY_UNIT,
    RACER_VEHICLE_UNLOCKS,
    COP_VEHICLE_UNLOCKS,
    RACER_SERIES_UNLOCK_EVENT,
    COP_SERIES_UNLOCK_EVENT,
    RACER_EVENT_GOLD_BOUNTY,
    COP_EVENT_GOLD_BOUNTY,
    RACER_FINAL_EVENT,
    COP_FINAL_EVENT,
    MAX_LEVEL,
    LEVEL_BOUNTY,
    GOAL_LOCATION,
    VICTORY_ITEM,
    racer_medal_location,
    cop_medal_location,
)
from .Options import Goal

if TYPE_CHECKING:
    from . import NFSHotPursuitWorld

Rule = Callable[[CollectionState], bool]

SIDES = {
    "Racer": {
        "events": RACER_EVENTS,
        "event_series": RACER_EVENT_SERIES,
        "event_vehicles": RACER_EVENT_VEHICLES,
        "loaned": RACER_LOANED_VEHICLE_EVENTS,
        "vehicles_by_series": RACER_VEHICLES_BY_CLASS,
        "vehicle_unlocks": RACER_VEHICLE_UNLOCKS,
        "series_unlock_event": RACER_SERIES_UNLOCK_EVENT,
        "gold_bounty": RACER_EVENT_GOLD_BOUNTY,
        "medal_tiers": RACER_MEDAL_TIERS,
        "medal_location": racer_medal_location,
        "prerequisites": RACER_EVENT_PREREQUISITES,
    },
    "Cop": {
        "events": COP_EVENTS,
        "event_series": COP_EVENT_SERIES,
        "event_vehicles": COP_EVENT_VEHICLES,
        "loaned": COP_LOANED_VEHICLE_EVENTS,
        "vehicles_by_series": COP_VEHICLES_BY_UNIT,
        "vehicle_unlocks": COP_VEHICLE_UNLOCKS,
        "series_unlock_event": COP_SERIES_UNLOCK_EVENT,
        "gold_bounty": COP_EVENT_GOLD_BOUNTY,
        "medal_tiers": COP_MEDAL_TIERS,
        "medal_location": cop_medal_location,
        "prerequisites": COP_EVENT_PREREQUISITES,
    },
}


def lent_car(side: str, event: str) -> bool:
    """The game lends the car for this event: Preview/Gauntlet events, and events whose only
    cars are unlocked by that very event (Previous Conviction, Fast Lane...)."""
    data = SIDES[side]
    if event in data["loaned"]:
        return True
    cars = data["event_vehicles"][event]
    return bool(cars) and all(data["vehicle_unlocks"][v] == event for v in cars)


def game_progression(side: str, multiplier: float) -> int:
    """Events the game itself lets you reach (all items owned) when each event is worth its gold
    bounty x multiplier: prerequisite events done and an allowed car unlocked in game."""
    data = SIDES[side]
    done, bounty_total, changed = set(), 0.0, True
    while changed:
        changed = False
        for event in data["events"]:
            if event in done or not all(p in done for p in data["prerequisites"].get(event, ())):
                continue
            if not lent_car(side, event):
                cars = data["event_vehicles"][event]
                conditions = [data["vehicle_unlocks"][v] for v in cars]
                if not any(c in done if isinstance(c, str) else bounty_total >= c for c in conditions):
                    continue
            done.add(event)
            bounty_total += data["gold_bounty"].get(event, 0) * multiplier
            changed = True
    return len(done)


def early_events(side: str, starting_vehicle: str, count: int, vehicles_randomized: bool = True) -> List[str]:
    """Up to `count` events after the first one that the game opens early and the starting car
    can drive, in unlock order, staying in the starting series."""
    data = SIDES[side]
    first = data["events"][0]
    series = data["event_series"][first]
    done, chosen = {first}, []
    while len(chosen) < count:
        for event in data["events"]:
            if event in done or data["event_series"][event] != series:
                continue
            if not all(p in done for p in data["prerequisites"].get(event, ())):
                continue
            # randomized cars: even a lent car must have been received
            if vehicles_randomized or not lent_car(side, event):
                if starting_vehicle not in data["event_vehicles"][event]:
                    continue
            done.add(event)
            chosen.append(event)
            break
        else:
            break
    return chosen


def random_start_for(side: str, random, extra: int):
    """(car, events, series) for a random start: a random car that some event accepts, a random
    event it can drive, that event's series, and up to `extra` more events of that series."""
    data = SIDES[side]
    cars = sorted({car for event in data["events"] for car in data["event_vehicles"][event]})
    car = random.choice(cars)
    drivable = [e for e in data["events"] if car in data["event_vehicles"][e]]
    first = random.choice(drivable)
    series = data["event_series"][first]
    others = [e for e in drivable if e != first and data["event_series"][e] == series]
    return car, [first] + random.sample(others, min(extra, len(others))), series


_REQUIRED: Dict[bool, float] = {}


def required_multiplier(vehicles_randomized: bool) -> float:
    """Smallest bounty multiplier with which the game's own progression opens every event: medal
    bounty alone is not enough (the game also pays bounty during events and for replays)."""
    if vehicles_randomized not in _REQUIRED:
        multiplier = 1.0
        while any(game_progression(side, multiplier) < len(SIDES[side]["events"]) for side in SIDES):
            multiplier += 0.05
        _REQUIRED[vehicles_randomized] = round(multiplier, 2)
    return _REQUIRED[vehicles_randomized]


def set_rules(world: "NFSHotPursuitWorld") -> None:
    player = world.player
    mw = world.multiworld
    events_randomized = bool(world.options.randomize_events)
    vehicles_randomized = bool(world.options.randomize_vehicles)

    def get(name: str):
        return mw.get_location(name, player)

    # 100% = the normal game's bounty rate: medal rewards only cover part of what events pay
    multiplier = world.options.bounty_multiplier.value / 100 * required_multiplier(vehicles_randomized)

    # What the player can really play depends on Archipelago items AND on the game's own
    # progression, which the client cannot unlock: an event opens in game once its
    # prerequisite events are done, and a car is only in the garage once its in-game
    # condition (bounty or event) is met. Both feed each other (events give bounty, bounty
    # gives cars, cars open events), so playable events are computed as a fixed point,
    # once per state and item count.
    side_names = list(SIDES)
    item_needs: Dict[str, Dict[str, List[str]]] = {}
    vehicle_options: Dict[str, Dict[str, List[str]]] = {}
    for side, data in SIDES.items():
        item_needs[side], vehicle_options[side] = {}, {}
        for event in data["events"]:
            needs = []
            if events_randomized:
                needs.append(f"Unlock {side} Event - {event}")
            series = data["event_series"][event]
            if vehicles_randomized:
                needs.append(f"Unlock {side} Series - {series}")
            item_needs[side][event] = needs
            # randomized cars: every event needs one of its cars received, lent ones included
            if vehicles_randomized or not lent_car(side, event):
                vehicle_options[side][event] = list(data["event_vehicles"][event])
    cache: Dict[str, object] = {"key": None, "value": None}
    first = {side: SIDES[side]["events"][0] for side in side_names}
    max_bounty = {side: sum(SIDES[side]["gold_bounty"].values()) * multiplier for side in side_names}

    def playable(state: CollectionState):
        """(playable events by side, reachable bounty by side) for this state."""
        key = (id(state), sum(state.prog_items[player].values()))
        if cache["key"] == key:
            return cache["value"]
        events = {side: set() for side in side_names}
        bounty_of = {side: 0.0 for side in side_names}
        changed = True
        while changed:
            changed = False
            for side in side_names:
                data = SIDES[side]
                done = events[side]

                def car_ready(vehicle: str) -> bool:
                    if vehicles_randomized:  # the client unlocks received cars in game
                        return state.has(f"Unlock {side} Vehicle - {vehicle}", player)
                    condition = data["vehicle_unlocks"][vehicle]
                    if isinstance(condition, str):
                        return condition in done
                    # events can be replayed for more bounty: cap at what all events give
                    return bounty_of[side] >= min(condition, max_bounty[side]) - 1e-6

                for event in data["events"]:
                    if event in done:
                        continue
                    if not state.has_all(item_needs[side][event], player):
                        continue
                    # randomized events: the client opens received ones directly in game
                    if not events_randomized and not all(p in done for p in data["prerequisites"].get(event, ())):
                        continue
                    cars = vehicle_options[side].get(event)
                    if cars is not None and not any(car_ready(v) for v in cars):
                        continue
                    done.add(event)
                    bounty_of[side] += data["gold_bounty"].get(event, 0) * multiplier
                    changed = True
        cache["key"], cache["value"] = key, (events, bounty_of)
        return events, bounty_of

    def make_access(side: str, event: str) -> Rule:
        return lambda state: event in playable(state)[0][side]

    access: Dict[str, Dict[str, Rule]] = {
        side: {event: make_access(side, event) for event in data["events"]}
        for side, data in SIDES.items()
    }

    def bounty(side: str, threshold: int) -> Rule:
        """Bounty reachable from playable events (gold bounty x multiplier). A threshold above
        what all events can give needs every event of that side."""
        if threshold <= 0:
            return lambda state: True
        target = min(threshold, max_bounty[side])
        return lambda state: playable(state)[1][side] >= target - 1e-6

    def level(side: str, lvl: int) -> Rule:
        return bounty(side, LEVEL_BOUNTY[lvl - 1])

    for side, data in SIDES.items():
        # Medals: require access to their event
        for event in data["events"]:
            for tier in data["medal_tiers"]:
                set_rule(get(data["medal_location"](event, tier)), access[side][event])

        # Levels
        if world.options.randomize_levels:
            for lvl in range(1, MAX_LEVEL + 1):
                if f"{side} Level {lvl} Reached" not in FREE_AT_START_LOCATIONS:
                    set_rule(get(f"{side} Level {lvl} Reached"), level(side, lvl))

        # Vehicle checks: the in-game unlock condition, either a bounty threshold
        # (see bounty()) or completing a specific event
        for vehicle, condition in data["vehicle_unlocks"].items():
            if isinstance(condition, str):
                rule = access[side][condition]
            else:
                rule = bounty(side, condition)
            if f"{side} Vehicle - {vehicle} Unlocked" not in FREE_AT_START_LOCATIONS:
                set_rule(get(f"{side} Vehicle - {vehicle} Unlocked"), rule)

        # Series checks: completing the event that opens the series in-game
        for series, unlock_event in data["series_unlock_event"].items():
            if unlock_event is not None:
                set_rule(get(f"{side} Series - {series} Unlocked"), access[side][unlock_event])

    # Goal
    goal = world.options.goal.value
    if goal == Goal.option_all_gold_medals:
        rules = list(access["Racer"].values()) + list(access["Cop"].values())
        goal_rule = lambda state: all(r(state) for r in rules)
    elif goal == Goal.option_final_events:
        racer_final = access["Racer"][RACER_FINAL_EVENT]
        cop_final = access["Cop"][COP_FINAL_EVENT]
        goal_rule = lambda state: racer_final(state) and cop_final(state)
    else:
        r20, c20 = level("Racer", MAX_LEVEL), level("Cop", MAX_LEVEL)
        goal_rule = lambda state: r20(state) and c20(state)

    set_rule(get(GOAL_LOCATION), goal_rule)
    mw.completion_condition[player] = lambda state: state.has(VICTORY_ITEM, player)
