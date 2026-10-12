# Need for Speed Hot Pursuit Remastered

## What does randomization do to this game?

Every Racer and Cop event must be unlocked by an item before it can be played. Series
(Sports to Hyper, Traffic Police to Special Response), vehicles and progressive weapon
upgrades are also items. Medals (Bronze/Silver/Gold and Pass/Merit/Distinction),
Racer/Cop levels 1-20, each series and each vehicle you unlock in-game are checks.

Events, vehicles/series, weapons and level checks can each be left vanilla with the
`randomize_events`, `randomize_vehicles`, `randomize_weapons` and `randomize_levels` options.

## What is the goal?

Depending on your options: earn every top medal, finish Seacrest Tour and End Of The Line,
or reach level 20 on both sides.

## What other items are there?

Bounty Bundles and Nitro Refills as filler, plus traps: Flat Tire, EMP Impact,
Speed Limiter, Roadblock Deployed, System Jammed and Reversed Steering. `trap_percentage`
sets how many fillers become traps; each trap and each filler has its own weight
(0 turns it off).

## How much bounty does the logic expect?

`bounty_multiplier` (Bounty Expectation): at 100 the logic only counts each event's medal
reward, which every player earns; bounty from takedowns, near misses and drifts is extra margin.
The highest levels and cars (beyond what all medals give) are only expected once every event of
that side is done. Higher values expect more bounty per event, so levels and bounty-locked cars
come into logic after fewer events. With vanilla cars, the game itself needs more bounty than the
medals give, so 100 then counts the game's own rate.