# Need for Speed Hot Pursuit Remastered Setup Guide

## Required software

- Need for Speed Hot Pursuit Remastered (PC)
- Archipelago 0.6.4 or newer

## Installation

1. Put `nfs_hpr.apworld` in the `custom_worlds` folder of your Archipelago install.
2. Generate a template YAML from the Archipelago Launcher ("Generate Template Options").
3. Fill in your slot name and options, then generate as usual.

## Playing

1. Start the game and load your career.
2. In the Archipelago Launcher, open **Need for Speed Hot Pursuit Remastered Client**.
3. Connect to the server with your slot name.
4. Play: every time the game saves (after each event), the client reads the save and sends
   your new medals, ranks, vehicles and series as checks.

The client finds the save automatically in
`Documents\Criterion Games\Need for Speed(TM) Hot Pursuit Remastered\Save`.
If it cannot, use `/save <full path to the .NFS11Save file>`.
`/checks` lists the checks found in the save.

Received Bounty Bundles are added to the game's bounty while it runs (to the side that is
behind). Run the client as administrator if it reports it cannot open the game process.
The client adds them again each time the game starts, since the save only keeps the bounty
earned in events.

Received Nitro Refills wait until you are driving in an event (the gauge is moving), then
fill the nitro gauge.

Traps hit you after a 5-second warning while you drive in an event (/trap_delay changes it): Roadblock Deployed stops your car dead,
Speed Limiter caps your speed at 72 km/h for 10 seconds, System Jammed empties your nitro
for 10 seconds, EMP Impact damages your car (+25 %), takes most of your speed and jolts the
car, Flat Tire damages your car (+15 %), makes it spin out or skid and slows you for 8 seconds
(a car at full damage is wrecked by the next big hit), Reversed Steering reverses your steering (the car's steering lock is made negative) for
10 seconds (timed traps pause with the game).

Progressive weapons (when weapons are randomized) are applied at the start of each event,
for your side only: a weapon you have not received has 0 charges; the first item gives the
event's normal charges, each further item +1 charge. The game's own weapon levels still grow
with successful hits. When you have no charge at all in an event, the weapon a weapon-intro
event holds ready is taken away too.

The game follows Archipelago: connect the client before loading your career. Events and cars
you have not received are kept out of the game (off the map, out of the garage). Received ones
are unlocked by the client, whatever the game's own conditions (bounty, previous events). Items
received during play show once you finish your next event (the game updates its unlocks then). The logic expects the same.

Locked events and cars: if you start an event Archipelago has not unlocked (its event item,
or, when vehicles are randomized, its series item or the item of the car you picked has not
been received), after a few seconds (so the event's scripted start can finish) the client
slows your car to a crawl and tells you what is missing; disconnecting the client lets it go. Quit the event
from the pause menu, or restart it with another car. Every event needs one of its own cars
(the game's list), Preview and Gauntlet events included: you need the car they lend.

Random Start (option): each side starts with a random car, a random event it can drive and that
event's series, plus more events of that series with Starting Events.

Tracker: the client's **Tracker** tab shows, for each racer and cop series, whether the series
is unlocked and which of its vehicles and events you have received (green: unlocked, grey:
locked). `/tracker` (or `/tracker racer`, `/tracker cop`) prints the same in the log.

Saves: the game has a single career, so the client keeps one save per seed for you, in
Archipelago's `nfs_hpr_saves` folder. With the game closed:
- `/use_save new` stores your current save (the first time, as `original`) and empties the
  game's save folder: the game starts a new career, which belongs to this seed.
- `/use_save current` plays this seed on the save already in the game (its progress so far
  counts as checks).
- `/use_save NAME` puts a stored save back (for example `/use_save original`).
- `/saves` lists the stored saves and tells which one is in the game.
Until the save in the game belongs to the seed you are connected to, the client sends no
checks, so another career's progress is never sent by mistake.
When you connect to a seed whose save is stored and the game is closed, the client swaps it
in by itself (after storing the save that was there). Nothing is deleted without a copy.
Turn off cloud saves for the game in the EA app (game properties) before using these
commands: otherwise the EA app downloads your old career back over the swapped save.
