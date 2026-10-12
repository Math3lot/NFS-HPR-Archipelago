from __future__ import annotations

from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, OptionGroup, PerGameCommonOptions, Range, Toggle


# ------------------------------------------------------------------------------------------- Goal

class Goal(Choice):
    """
    What you need to do to win.
    all_gold_medals: Gold on all 78 Racer events and Distinction on all 63 Cop events.
    final_events: finish Seacrest Tour (Racer) and End Of The Line (Cop).
    level_20_both: reach level 20 as both Racer and Cop.
    """
    display_name = "Goal"
    option_all_gold_medals = 0
    option_final_events = 1
    option_level_20_both = 2
    default = 1


# ---------------------------------------------------------------------------------- Randomization

class RandomizeEvents(DefaultOnToggle):
    """
    Events are items: an event is only on the map once you receive it.
    Off: events open as in the normal game. Medals are checks either way.
    """
    display_name = "Randomize Events"


class RandomizeVehicles(DefaultOnToggle):
    """
    Cars and series are items: a car is only in your garage once you receive it, and an event
    also needs its series and one of its cars. Preview and Gauntlet events need the car they lend.
    Off: cars and series unlock as in the normal game. Unlocking them is a check either way.
    """
    display_name = "Randomize Vehicles"


class RandomizeWeapons(DefaultOnToggle):
    """
    Each weapon is a progressive item (4 per weapon): without it the weapon has no charge, the
    first one gives the event's normal charges, each further one +1 charge.
    Off: weapons work as in the normal game.
    """
    display_name = "Randomize Weapons"


class RandomizeLevels(DefaultOnToggle):
    """
    Reaching each Racer and Cop level (2 to 20) is a check.
    """
    display_name = "Level Checks"


# ------------------------------------------------------------------------------------------ Start

class RandomStart(Toggle):
    """
    Each side starts with a random car, a random event that car can drive and that event's series.
    Off: you start with the Porsche Boxster Spyder and Roadsters Reborn (Racer), the Ford Crown
    Victoria and Chase 101 (Cop). Needs Randomize Events and Randomize Vehicles.
    """
    display_name = "Random Start"


class StartingEvents(Range):
    """
    Extra events you start with on each side, all drivable with your starting car (from the
    starting series). The normal start has only 1 such Racer event.
    """
    display_name = "Starting Events"
    range_start = 0
    range_end = 8
    default = 3


# ----------------------------------------------------------------------------------- Logic

class BountyMultiplier(Range):
    """
    How much bounty the logic assumes you earn per event, as a percentage of its medal reward.
    100 = the medal reward only, which every player earns: bounty from takedowns, near misses and
    drifts is extra margin. The highest levels and cars, beyond what all medals give, are only
    expected once every event of that side is done.
    Higher = harder: levels and bounty-locked cars are expected after fewer events, so you may
    need aggressive driving or replays to keep up.
    (With vanilla cars, the game itself needs more bounty, so the logic counts the game's own
    rate at 100.)
    """
    display_name = "Bounty Expectation"
    range_start = 100
    range_end = 300
    default = 100


# ---------------------------------------------------------------------------------- Traps & Filler

class TrapPercentage(Range):
    """
    Percentage of filler items replaced by traps. Each trap below has a weight: the higher, the
    more often it appears; 0 turns it off. With every trap at 0 there are no traps.
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 20


class _Weight(Range):
    range_start = 0
    range_end = 10
    default = 1


class FlatTireWeight(_Weight):
    """Flat Tire: damage, then the car spins out or skids. 0 = never."""
    display_name = "Flat Tire Weight"


class EmpImpactWeight(_Weight):
    """EMP Impact: damage, the car loses most of its speed and is jolted sideways. 0 = never."""
    display_name = "EMP Impact Weight"


class SpeedLimiterWeight(_Weight):
    """Speed Limiter: speed capped at 72 km/h for 10 seconds. 0 = never."""
    display_name = "Speed Limiter Weight"


class RoadblockWeight(_Weight):
    """Roadblock: the car is stopped dead. 0 = never."""
    display_name = "Roadblock Weight"


class SystemJammedWeight(_Weight):
    """System Jammed: nitro drained and unusable for 10 seconds. 0 = never."""
    display_name = "System Jammed Weight"


class ReversedSteeringWeight(_Weight):
    """Reversed Steering: left and right are swapped for 10 seconds. 0 = never."""
    display_name = "Reversed Steering Weight"


class BountyBundleWeight(_Weight):
    """Bounty Bundle filler (1,000 to 20,000 bounty, small amounts more common). 0 = never."""
    display_name = "Bounty Bundle Weight"
    default = 3


class NitroRefillWeight(_Weight):
    """Nitro Refill filler (Small to Full, small refills more common). 0 = never.
    If both filler weights are 0, Bounty Bundles are used."""
    display_name = "Nitro Refill Weight"


@dataclass
class NFSHotPursuitOptions(PerGameCommonOptions):
    goal: Goal
    randomize_events: RandomizeEvents
    randomize_vehicles: RandomizeVehicles
    randomize_weapons: RandomizeWeapons
    randomize_levels: RandomizeLevels
    random_start: RandomStart
    starting_events: StartingEvents
    bounty_multiplier: BountyMultiplier
    trap_percentage: TrapPercentage
    flat_tire_weight: FlatTireWeight
    emp_impact_weight: EmpImpactWeight
    speed_limiter_weight: SpeedLimiterWeight
    roadblock_weight: RoadblockWeight
    system_jammed_weight: SystemJammedWeight
    reversed_steering_weight: ReversedSteeringWeight
    bounty_bundle_weight: BountyBundleWeight
    nitro_refill_weight: NitroRefillWeight


option_groups = [
    OptionGroup("Goal", [Goal]),
    OptionGroup("Randomization", [RandomizeEvents, RandomizeVehicles, RandomizeWeapons, RandomizeLevels]),
    OptionGroup("Start", [RandomStart, StartingEvents]),
    OptionGroup("Logic", [BountyMultiplier]),
    OptionGroup("Traps", [TrapPercentage, FlatTireWeight, EmpImpactWeight, SpeedLimiterWeight,
                          RoadblockWeight, SystemJammedWeight, ReversedSteeringWeight]),
    OptionGroup("Filler", [BountyBundleWeight, NitroRefillWeight]),
]
