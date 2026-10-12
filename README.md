# Need for Speed Hot Pursuit Remastered — Archipelago

An [Archipelago](https://archipelago.gg) randomizer world and client for
**Need for Speed Hot Pursuit Remastered** (PC).

Events, series, cars and weapon upgrades become items shuffled across the multiworld.
Medals, Racer/Cop levels and in-game unlocks become checks. The client talks to the running
game: events and cars you have not received are hidden from the map and the garage, received
ones are unlocked directly, and traps hit you while you drive.

## Features

- **Events, series and cars as items.** Unreceived events are removed from the map and
  unreceived cars from the garage; received ones unlock whatever the game's own conditions.
- **Accurate logic.** Every event needs its event item, its series and one of the cars the
  game allows in it (Preview and Gauntlet events need the car they lend).
- **Progressive weapons.** Without a weapon item you have no charge; each item adds charges.
- **Traps that really hit:** Roadblock, Speed Limiter, System Jammed, EMP Impact (damage),
  Flat Tire (damage + spin-out or skid) and Reversed Steering.
- **Filler:** Bounty Bundles (added to your bounty) and Nitro Refills.
- **Tracker tab** in the client: series, cars and events, received or not.
- **One save per seed.** The client stores and swaps careers so each seed has its own.
- **Random Start** and extra **Starting Events** to avoid a slow start.
- **Goals:** all top medals, the two final events, or level 20 on both sides.

## Installation

1. Download `nfs_hpr.apworld` from the [latest release](../../releases/latest).
2. Put it in the `custom_worlds` folder of your Archipelago install
   (usually `C:\ProgramData\Archipelago\custom_worlds`).
3. Open the Archipelago Launcher and use **Generate Template Options** (or the Options
   Creator) to make your YAML.

Requires Archipelago 0.6.4 or newer and the PC version of the game (EA app).

Full guide: [setup guide](nfs_hpr/docs/setup_en.md) ·
[game page](nfs_hpr/docs/en_Need%20for%20Speed%20Hot%20Pursuit%20Remastered.md)

## Options

| Category | Option | What it does |
|---|---|---|
| Goal | `goal` | All top medals, final events (default), or level 20 on both sides |
| Randomization | `randomize_events` | Events are items |
| | `randomize_vehicles` | Cars and series are items |
| | `randomize_weapons` | Progressive weapon items |
| | `randomize_levels` | Each level reached is a check |
| Start | `random_start` | Random starting car, event and series on each side |
| | `starting_events` | Extra events at the start (0–8, default 3) |
| Logic | `bounty_multiplier` | Bounty Expectation: 100 = the normal game, higher = harder |
| Traps | `trap_percentage` | Share of filler replaced by traps |
| | `*_weight` | Weight of each trap (0 = off) |
| Filler | `bounty_bundle_weight`, `nitro_refill_weight` | Weight of each filler type |

## Quick start

1. **Turn off cloud saves** for the game in the EA app (game properties).
2. With the game closed, open **Need for Speed Hot Pursuit Remastered Client** from the
   Launcher, connect to your slot, and type `/use_save new` to start a fresh career for this
   seed (your old career is kept as `original`).
3. Start the game and load the career. Play: checks are sent each time the game saves.

Useful commands: `/tracker`, `/saves`, `/use_save NAME`, `/checks`.

## Notes

- The client reads and writes the game's memory. Run it as administrator if it cannot open
  the game process.
- Items received during an event show in game once you finish (or quit) your next event.

## License

[MIT](LICENSE) © Math3lot
