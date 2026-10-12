"""
Need for Speed Hot Pursuit Remastered client.

Watches the game's save file, works out which medals, levels, vehicles and
series have been earned, and sends them to the Archipelago server.
Received Bounty Bundles are written into the running game's memory; other
items are listed in the client for now.
"""
from __future__ import annotations

import asyncio
import glob
import json
import os
import struct
import threading
import time
from typing import Dict, List, Optional, Set, Tuple

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem

from .Checks import completed_locations, goal_reached
from .Data import BOUNTY_BUNDLE_VALUES, GAME_NAME, NITRO_REFILL_VALUES, TRAP_DURATIONS, TRAP_ITEMS
from .GameMemory import IS_WINDOWS, GameMemory, find_pid
from . import SaveSlots
from .Locations import location_name_to_id
from .EventsData import EVENTS_BY_ID
from .VehiclesData import VEHICLE_IDS, VEHICLES_BY_ID
from .Locks import hold_car, missing_unlocks
from .Tracker import tracker_markup, tracker_text
from .Weapons import side_cells, target_charges, weapon_levels
from .Traps import MOVING, SUPPORTED_TRAPS, run_trap, speed_of
from .SaveReader import STAT_COP_BOUNTY, STAT_RACER_BOUNTY, read_save, stat

POLL_SECONDS = 2.0
STATE_FILE = "nfs_hpr_client_state.json"
RESCAN_SECONDS = 30.0
WEAPON_LABELS = {0: "Helicopter", 1: "EMP", 2: "Spike Strip", 3: "Spike Strip", 4: "Turbo", 5: "EMP",
                 7: "Jammer", 8: "Roadblock"}
LOCK_GRACE_SECONDS = 8.0  # driving time allowed in a locked event before the car is held (scripted starts)
TRAP_RETRY_SECONDS = 20.0  # wait before trying again a trap that found no car (free drive, menus)
TRAP_WARNING_SECONDS = 5.0  # driving time between "Incoming" and the trap (change with /trap_delay)
MAX_BOUNTY_JUMP = 1_000_000  # bounty gained between two checks of the cached address, at most
SAVE_GLOB = os.path.join("Criterion Games", "Need for Speed(TM) Hot Pursuit Remastered", "Save", "*", "*.NFS11Save")


def find_save_file() -> Optional[str]:
    """Most recently modified save in the usual Documents folders."""
    home = os.path.expanduser("~")
    candidates = []
    for documents in (os.path.join(home, "Documents"), os.path.join(home, "OneDrive", "Documents")):
        candidates += glob.glob(os.path.join(documents, SAVE_GLOB))
    return max(candidates, key=os.path.getmtime) if candidates else None


class NFSHPRCommandProcessor(ClientCommandProcessor):
    def _cmd_save(self, path: str = "") -> bool:
        """Show the save file in use, or set it: /save <full path to .NFS11Save>"""
        ctx: NFSHPRContext = self.ctx  # type: ignore[assignment]
        if path:
            if not os.path.isfile(path):
                self.output(f"File not found: {path}")
                return False
            ctx.save_path = path
            ctx.save_mtime = 0.0
        self.output(f"Save file: {ctx.save_path or 'not found'}")
        return True

    def _cmd_trap_delay(self, seconds: str = "") -> bool:
        """Show or set the warning delay before a trap hits, in seconds of driving: /trap_delay 5"""
        ctx: NFSHPRContext = self.ctx  # type: ignore[assignment]
        if seconds:
            try:
                ctx.trap_delay = max(0.0, float(seconds))
            except ValueError:
                self.output("Usage: /trap_delay <seconds>")
                return False
        self.output(f"Traps hit after {ctx.trap_delay:g} seconds of driving.")
        return True

    def _cmd_tracker(self, side: str = "") -> bool:
        """List what you have unlocked (series, vehicles, events): /tracker, /tracker racer, /tracker cop"""
        ctx: NFSHPRContext = self.ctx  # type: ignore[assignment]
        for line in tracker_text(received_names(ctx), ctx.randomize_events, ctx.randomize_vehicles, side):
            self.output(line)
        return True

    def _cmd_saves(self) -> bool:
        """List the game saves the client keeps (one per seed) and which one is in the game now."""
        ctx: NFSHPRContext = self.ctx  # type: ignore[assignment]
        self.output(f"Save in the game now: {ctx.save_owner() or 'unknown (your own career?)'}")
        names = SaveSlots.stashes()
        self.output(f"Stored saves ({SaveSlots.stash_root()}): " + (", ".join(names) if names else "none"))
        if ctx.seed_save_name():
            self.output(f"This seed's save is called: {ctx.seed_save_name()}")
        self.output("Switch with /use_save new (new career for this seed) or /use_save NAME (game closed).")
        return True

    def _cmd_use_save(self, name: str = "") -> bool:
        """/use_save new = new career for this seed, /use_save current = this seed uses the save in the game,
        /use_save NAME = put a stored save back (game closed)"""
        ctx: NFSHPRContext = self.ctx  # type: ignore[assignment]
        if not name:
            self.output("Usage: /use_save new  or  /use_save NAME (see /saves)")
            return False
        return switch_save(ctx, name)

    def _cmd_checks(self) -> bool:
        """List the checks found in the save that the server has not confirmed yet."""
        ctx: NFSHPRContext = self.ctx  # type: ignore[assignment]
        pending = sorted(ctx.found_names - {ctx.location_names.lookup_in_game(i) for i in ctx.checked_locations})
        self.output(f"{len(ctx.found_names)} checks found in the save, {len(pending)} pending.")
        for name in pending[:30]:
            self.output(f"  {name}")
        return True


class NFSHPRContext(CommonContext):
    game = GAME_NAME
    items_handling = 0b111  # receive items from everywhere, including our own and starting inventory
    command_processor = NFSHPRCommandProcessor

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        super().__init__(server_address, password)
        self.save_path: Optional[str] = find_save_file()
        self.save_mtime: float = 0.0
        self.found_names: Set[str] = set()
        self.goal: int = 1
        self.levels_are_checks: bool = True
        self.goal_sent = False
        self.memory = GameMemory()
        self.save_bounty: Optional[Tuple[int, int]] = None  # (racer, cop) career stat in the last save read
        # Kept across restarts (client state file):
        self.applied_index: int = 0           # received items already handled
        self.bundle_bounty = [0, 0]           # (racer, cop) bounty given by Bounty Bundles so far
        self.pending_nitro: List[str] = []    # Nitro Refills waiting for an event
        self.pending_traps: List[str] = []    # traps waiting for the player to drive
        # About the running game process:
        self.mem_pid: Optional[int] = None
        self.mem_applied = [0, 0]             # (racer, cop) bundle bounty already written into this process
        self.mem_reference: Optional[Tuple[int, int]] = None  # (racer, cop) last seen at the bounty address
        self.last_scan: Tuple[Optional[Tuple[int, int]], float] = (None, 0.0)
        self.last_gauge: Optional[float] = None
        self.last_nitro_scan: float = 0.0
        self.last_body_scan: float = 0.0
        self.trap_thread: Optional[threading.Thread] = None
        self.trap_stop = threading.Event()
        self.trap_delay: float = TRAP_WARNING_SECONDS
        self.trap_retry_at: float = 0.0
        self.checks_paused = False
        self.randomize_weapons: bool = True
        self.weapon_event: Optional[int] = None    # event id seen on the last look
        self.weapon_live: Optional[List[int]] = None  # charges seen on the last look (after our writes)
        self.weapon_position = None                # player car position on the last look
        self.weapons_pending = False               # an event (re)start is waiting for the car to move
        self.weapons_disarm = False                # no charge for the player's side in this event
        self.randomize_events: bool = True
        self.randomize_vehicles: bool = True
        self.locked_event: Optional[int] = None
        self.hidden_events: Dict[int, str] = {}  # event id -> state written in this game process
        self.hidden_vehicles: Dict[int, str] = {}  # vehicle id -> state written in this game process
        self.last_tree_scan: float = 0.0
        self.hidden_logged = False
        self.root_lists: Dict[int, Dict[int, List[int]]] = {}  # first event -> map lists taken out of
        self.last_root_scan: Dict[int, float] = {}
        self.lock_seen: Optional[int] = None       # locked event first seen while driving...
        self.lock_seen_at: float = 0.0             # ...at this time (grace for the scripted start)    # event id currently held because it is locked
        self.lock_thread: Optional[threading.Thread] = None
        self.last_weapons_scan: float = 0.0
        self.waiting_reason: str = ""

    # ------------------------------------------------------------------ state kept across restarts

    def _state_key(self) -> str:
        return f"{self.server_seed_name}:{self.team}:{self.slot}"

    def _load_states(self) -> Dict[str, dict]:
        try:
            with open(Utils.user_path(STATE_FILE)) as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}

    def load_state(self) -> None:
        state = self._load_states().get(self._state_key(), {})
        self.applied_index = int(state.get("applied_index", 0))
        self.bundle_bounty = [int(state.get("racer_bundles", 0)), int(state.get("cop_bundles", 0))]
        self.pending_nitro = [n for n in state.get("pending_nitro", []) if n in NITRO_REFILL_VALUES]
        self.pending_traps = [n for n in state.get("pending_traps", []) if n in SUPPORTED_TRAPS]

    def save_state(self) -> None:
        states = self._load_states()
        states[self._state_key()] = {
            "applied_index": self.applied_index,
            "racer_bundles": self.bundle_bounty[0],
            "cop_bundles": self.bundle_bounty[1],
            "pending_nitro": self.pending_nitro,
            "pending_traps": self.pending_traps,
        }
        try:
            with open(Utils.user_path(STATE_FILE), "w") as f:
                json.dump(states, f)
        except OSError as error:
            logger.warning(f"Could not save the client state: {error}")

    # ------------------------------------------------------------------ which career is in the game

    def _global(self) -> dict:
        return self._load_states().get("_global", {})

    def _set_global(self, **values) -> None:
        states = self._load_states()
        states.setdefault("_global", {}).update(values)
        try:
            with open(Utils.user_path(STATE_FILE), "w") as f:
                json.dump(states, f)
        except OSError as error:
            logger.warning(f"Could not save the client state: {error}")

    def save_owner(self) -> str:
        """Name of the stored save the game's current save belongs to ('' if unknown)."""
        return self._global().get("save_owner", "")

    def seed_save_name(self) -> str:
        if not self.server_seed_name or self.slot is None:
            return ""
        return SaveSlots.safe_name(f"seed_{self.server_seed_name}_{self.auth or self.slot}")

    def game_save_folder(self) -> Optional[str]:
        if self.save_path:
            folder = os.path.dirname(self.save_path)
            if self._global().get("save_folder") != folder:
                self._set_global(save_folder=folder)
            return folder
        return self._global().get("save_folder") or None

    def bounty_bonus(self) -> Tuple[int, int]:
        """Bounty Bundles already written into the running game. Only those count for level and
        vehicle checks, so checks match what the game itself has unlocked (it cannot be written
        while the career bounty is still too low to be found in memory)."""
        return self.mem_applied[0], self.mem_applied[1]

    def wait(self, reason: str) -> None:
        """Log why items are not applied yet, once per reason."""
        if reason != self.waiting_reason:
            self.waiting_reason = reason
            logger.info(reason)

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            slot_data = args.get("slot_data", {}) or {}
            self.goal = int(slot_data.get("goal", 1))
            self.levels_are_checks = bool(slot_data.get("randomize_levels", True))
            self.randomize_weapons = bool(slot_data.get("randomize_weapons", True))
            self.randomize_events = bool(slot_data.get("randomize_events", True))
            self.randomize_vehicles = bool(slot_data.get("randomize_vehicles", True))
            self.save_mtime = 0.0  # re-scan the save right away
            self.load_state()
            auto_switch_save(self)
            if not IS_WINDOWS:
                logger.info("Items can only be applied in game on Windows.")
            logger.info(f"Save file: {self.save_path or 'not found, use /save <path>'}")
        elif cmd == "ReceivedItems":
            # On (re)connecting the server sends every item again: only show the new ones.
            start = int(args.get("index", 0))
            for offset, raw in enumerate(args.get("items", [])):
                if start + offset < self.applied_index:
                    continue
                item = NetworkItem(*raw)
                logger.info(f"Received: {self.item_names.lookup_in_game(item.item)}")

    def run_gui(self) -> None:
        from kvui import GameManager

        ctx = self

        class NFSHPRManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago Need for Speed Hot Pursuit Remastered Client"

            def build(self):
                container = super().build()
                try:
                    self.add_tracker_tab()
                except Exception as error:  # the tracker is a convenience: never break the client
                    logger.warning(f"Tracker tab unavailable ({error}); use /tracker instead.")
                return container

            def add_tracker_tab(self) -> None:
                from kivy.clock import Clock
                from kivy.uix.label import Label
                from kivy.uix.scrollview import ScrollView

                label = Label(markup=True, size_hint_y=None, halign="left", valign="top", padding=(12, 12))
                label.bind(width=lambda lbl, width: setattr(lbl, "text_size", (width, None)),
                           texture_size=lambda lbl, size: setattr(lbl, "height", size[1]))
                scroll = ScrollView(do_scroll_x=False)
                scroll.add_widget(label)
                self.add_client_tab("Tracker", scroll)
                last = {"text": None}

                def refresh(_dt) -> None:
                    # Redraw only when items arrived: the label is long and costly to render.
                    key = (len(ctx.items_received), ctx.randomize_events, ctx.randomize_vehicles)
                    if key == last["text"]:
                        return
                    last["text"] = key
                    label.text = tracker_markup(received_names(ctx), ctx.randomize_events, ctx.randomize_vehicles)

                Clock.schedule_interval(refresh, 5.0)
                refresh(0)

        self.ui = NFSHPRManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def find_save_in(folder: Optional[str]) -> Optional[str]:
    saves = glob.glob(os.path.join(folder, "*.NFS11Save")) if folder else []
    return max(saves, key=os.path.getmtime) if saves else None


def switch_save(ctx: NFSHPRContext, name: str) -> bool:
    """Put another career in the game (stored save NAME, or 'new' for a fresh one), keeping a copy of
    the current one. Only while the game is closed."""
    if IS_WINDOWS and find_pid() is not None and name.lower() != "current":
        logger.info("Close the game first: it would write its save over the swapped one.")
        return False
    folder = ctx.game_save_folder()
    if not folder:
        logger.info("The game's save folder is not known: start the game once, or use /save <path>.")
        return False
    seed_name = ctx.seed_save_name()
    if name.lower() == "current":
        if not seed_name:
            logger.info("Connect to the server first.")
            return False
        ctx._set_global(save_owner=seed_name)
        ctx.save_mtime = 0.0
        logger.info(f"The save in the game now belongs to {seed_name}: its progress counts as checks.")
        return True
    target = seed_name if name.lower() == "new" else SaveSlots.safe_name(name)
    if name.lower() == "new" and not seed_name:
        logger.info("Connect to the server first: the new career is stored under this seed's name.")
        return False
    if name.lower() != "new" and target not in SaveSlots.stashes():
        logger.info(f"No stored save called {target}. /saves lists them.")
        return False
    owner = ctx.save_owner()
    if not owner:
        owner = "original" if "original" not in SaveSlots.stashes() else SaveSlots.backup_name("")
    if owner == target and name.lower() != "new":
        logger.info(f"The game already has the save {target}.")
        return True
    stored = SaveSlots.stash(folder, owner)
    if stored:
        logger.info(f"Your current save was stored as {owner}.")
    if name.lower() == "new":
        SaveSlots.clear(folder)
        logger.info(f"Game save cleared: start the game for a new career. It belongs to {target} from now on.")
        logger.info("Turn off cloud saves for the game in the EA app first, or it brings the old career back.")
    else:
        SaveSlots.install(folder, target)
        logger.info(f"Save {target} is now in the game.")
    ctx._set_global(save_owner=target)
    ctx.save_mtime = 0.0
    ctx.found_names = set()
    return True


def auto_switch_save(ctx: NFSHPRContext) -> None:
    """On connecting: if this seed has a stored save and the game has another one, swap (game closed)."""
    try:
        seed_name = ctx.seed_save_name()
        owner = ctx.save_owner()
        if not seed_name or owner == seed_name:
            return
        if seed_name in SaveSlots.stashes():
            if IS_WINDOWS and find_pid() is not None:
                logger.info(f"This seed's save ({seed_name}) is stored but the game has another one: "
                            f"close the game and use /use_save {seed_name}.")
            else:
                switch_save(ctx, seed_name)
        else:
            logger.info(f"The game's save belongs to {owner or 'your own career'}, so no check is sent for now. "
                        "Close the game and use /use_save new for a new career (your current save is kept), "
                        "or /use_save current to play this seed on it. /saves lists the stored saves.")
    except OSError as error:
        logger.warning(f"Could not switch saves: {error}")


async def save_watcher(ctx: NFSHPRContext) -> None:
    while not ctx.exit_event.is_set():
        await asyncio.sleep(POLL_SECONDS)
        if not (ctx.server and ctx.slot):
            continue
        if not ctx.save_path or not os.path.isfile(ctx.save_path):
            found = find_save_in(ctx.game_save_folder()) or find_save_file()
            if found != ctx.save_path and found:
                ctx.save_path, ctx.save_mtime = found, 0.0
                logger.info(f"Save file: {found}")
            if not ctx.save_path:
                continue
        if ctx.save_owner() != ctx.seed_save_name():
            # The career in the game is not this seed's: never send its progress as checks.
            if not ctx.checks_paused:
                ctx.checks_paused = True
                logger.info("Checks paused: the save in the game does not belong to this seed. Use /use_save new "
                            "(game closed, new career) or /use_save current (play this seed on the current save).")
            continue
        ctx.checks_paused = False
        try:
            mtime = os.path.getmtime(ctx.save_path)
            if mtime == ctx.save_mtime:
                continue
            tables = read_save(ctx.save_path)
            ctx.save_mtime = mtime
        except (OSError, ValueError, KeyError) as error:
            # The game may be writing the file; try again on the next tick.
            logger.debug(f"Could not read the save yet: {error}")
            continue

        ctx.save_bounty = (stat(tables, STAT_RACER_BOUNTY), stat(tables, STAT_COP_BOUNTY))
        ctx.found_names = completed_locations(tables, ctx.levels_are_checks, ctx.bounty_bonus())
        ids = {location_name_to_id[name] for name in ctx.found_names if name in location_name_to_id}
        ids &= ctx.missing_locations | ctx.checked_locations  # only this slot's locations (options, free ones)
        new = ids - ctx.checked_locations - ctx.locations_checked
        if new:
            ctx.locations_checked |= new
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": sorted(new)}])
            for location_id in sorted(new):
                logger.info(f"Check: {ctx.location_names.lookup_in_game(location_id)}")

        if not ctx.goal_sent and goal_reached(tables, ctx.goal, ctx.bounty_bonus()):
            ctx.goal_sent = True
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            logger.info("Goal complete!")


WEAPON_POLL_SECONDS = 0.1


async def weapon_watcher(ctx: NFSHPRContext) -> None:
    """Fast loop for weapons: set the charges right as the player starts driving."""
    while not ctx.exit_event.is_set():
        await asyncio.sleep(WEAPON_POLL_SECONDS)
        if not (ctx.server and ctx.slot and IS_WINDOWS and ctx.memory.pid == ctx.mem_pid and ctx.mem_pid):
            continue
        try:
            await asyncio.to_thread(apply_weapons, ctx)
        except OSError:
            pass
        except Exception as error:
            logger.exception(f"Error while applying weapons: {error}")
            await asyncio.sleep(5)


async def item_applier(ctx: NFSHPRContext) -> None:
    while not ctx.exit_event.is_set():
        await asyncio.sleep(POLL_SECONDS)
        if not (ctx.server and ctx.slot and IS_WINDOWS):
            continue
        try:
            # Memory scans take a few seconds: keep them off the UI thread.
            await asyncio.to_thread(apply_pending_items, ctx)
        except PermissionError as error:
            ctx.wait(str(error))
        except OSError as error:
            logger.debug(f"Memory access failed: {error}")
            ctx.memory.detach()
        except Exception as error:  # never let item application take the client down
            logger.exception(f"Error while applying items: {error}")
            await asyncio.sleep(10)


def take_new_items(ctx: NFSHPRContext) -> None:
    """Record newly received consumables (kept in the state file): bundle totals, pending refills."""
    received = ctx.items_received
    if len(received) <= ctx.applied_index:
        return
    base = ctx.save_bounty or (0, 0)
    for item in received[ctx.applied_index:]:
        name = ctx.item_names.lookup_in_game(item.item)
        if name in NITRO_REFILL_VALUES:
            ctx.pending_nitro.append(name)
            logger.info(f"{name} will be applied during your next event.")
            continue
        if name in TRAP_ITEMS:
            if name in SUPPORTED_TRAPS:
                ctx.pending_traps.append(name)
                logger.info(f"{name} will hit you as soon as you drive.")
            else:
                logger.info(f"{name} is not supported by this client version yet.")
            continue
        if name not in BOUNTY_BUNDLE_VALUES:
            continue
        # A bundle goes to the side that is behind, to help both level goals along.
        side = 0 if base[0] + ctx.bundle_bounty[0] <= base[1] + ctx.bundle_bounty[1] else 1
        ctx.bundle_bounty[side] += BOUNTY_BUNDLE_VALUES[name]
        logger.info(f"{name} goes to {'Racer' if side == 0 else 'Cop'} bounty.")
    ctx.applied_index = len(received)
    ctx.save_state()
    ctx.save_mtime = 0.0  # re-evaluate level checks with the new bounty


def apply_pending_items(ctx: NFSHPRContext) -> None:
    take_new_items(ctx)
    # Check the game process every time: a restart wipes what we wrote into it.
    if not ctx.memory.attach():
        if any(ctx.bundle_bounty) or ctx.pending_nitro:
            ctx.wait("Waiting for the game to apply received items...")
        return
    if ctx.memory.pid != ctx.mem_pid:  # new game process: nothing written into it yet
        if ctx.mem_pid is not None:
            logger.info("Game restarted: Bounty Bundles will be applied again.")
        ctx.mem_pid, ctx.mem_applied, ctx.mem_reference = ctx.memory.pid, [0, 0], None
        ctx.memory.bounty_address = None
        ctx.memory.nitro_tag_address = None
        ctx.memory.body_address = None
        ctx.memory.weapons_address = None
        ctx.weapon_event = ctx.weapon_live = ctx.weapon_position = None
        ctx.weapons_pending = False
        ctx.weapons_disarm = False
        ctx.last_weapons_scan = 0.0
        ctx.last_scan = (None, 0.0)
        ctx.last_gauge = None
        ctx.last_nitro_scan = 0.0
        ctx.hidden_events = {}
        ctx.hidden_vehicles = {}
        ctx.last_tree_scan = 0.0
        ctx.hidden_logged = False
        ctx.root_lists, ctx.last_root_scan = {}, {}
    hide_locked_events(ctx)  # first: it must happen before the career is loaded
    apply_bounty(ctx)
    apply_nitro(ctx)
    enforce_locks(ctx)
    start_trap(ctx)
    # Weapons are watched by their own fast loop (weapon_watcher): the first charge is
    # usable as soon as the car moves, so a 2-second check would come too late.


TREE_RESCAN_SECONDS = 3.0


def hide_locked_events(ctx: NFSHPRContext) -> None:
    """Make the game follow Archipelago: events and cars not received are kept out of the game
    (their unlock-tree nodes become unreachable); received ones are unlocked right away (they only
    need the side's first event). The game reads the tree when the career loads, so the client
    must be connected before that; later changes show once the city reloads (Free Drive or an event)."""
    if not (ctx.randomize_events or ctx.randomize_vehicles):
        return
    if not ctx.memory.tree_ok():
        if time.monotonic() - ctx.last_tree_scan < TREE_RESCAN_SECONDS:
            return
        ctx.last_tree_scan = time.monotonic()
        if not ctx.memory.locate_tree():
            return
        ctx.hidden_events = {}
        ctx.hidden_vehicles = {}
    received = received_names(ctx)
    newly_open = []
    for event_id, event in EVENTS_BY_ID.items():
        missing = missing_unlocks(event, received, ctx.randomize_events, ctx.randomize_vehicles)
        if missing:
            state = "hidden"
        else:
            state = "open" if ctx.randomize_events else "vanilla"
        if ctx.hidden_events.get(event_id) == state:
            continue
        if ctx.memory.set_event_state(event_id, event["side"], state):
            if ctx.hidden_events.get(event_id) == "hidden" and state != "hidden":
                newly_open.append(f"{event['name']} ({event['side']})")
            ctx.hidden_events[event_id] = state
    if ctx.randomize_vehicles:
        for (side, name), vehicle_id in VEHICLE_IDS.items():
            state = "open" if f"Unlock {side} Vehicle - {name}" in received else "hidden"
            if ctx.hidden_vehicles.get(vehicle_id) == state:
                continue
            if ctx.memory.set_vehicle_state(vehicle_id, side, state):
                if ctx.hidden_vehicles.get(vehicle_id) == "hidden" and state == "open":
                    newly_open.append(f"the {name} ({side})")
                ctx.hidden_vehicles[vehicle_id] = state
    if ctx.randomize_events:
        newly_open += manage_first_events(ctx, received)
    for name in newly_open:
        logger.info(f"Unlocked in game: {name}.")
    if newly_open:
        # the game only re-reads its unlocks when the city reloads
        logger.info("To see it now: enter Free Drive and go back to the map "
                    "(or finish or quit an event).")
    if not ctx.hidden_logged and (ctx.hidden_events or ctx.hidden_vehicles):
        ctx.hidden_logged = True
        events = sum(1 for v in ctx.hidden_events.values() if v == "hidden")
        cars = sum(1 for v in ctx.hidden_vehicles.values() if v == "hidden")
        logger.info(f"The game follows Archipelago: {events} events and {cars} cars are kept out until "
                    "received, received ones are unlocked (connect the client before loading your career).")


ROOT_RESCAN_SECONDS = 60.0


def manage_first_events(ctx: NFSHPRContext, received: Set[str]) -> List[str]:
    """The first event of each side has no unlock node, so the game always lists it on the map:
    take it out of the map lists while it is not received, put the lists back once it is."""
    from .EventUnlocks import ROOT_EVENTS
    opened = []
    for side, root_id in ROOT_EVENTS.items():
        event = EVENTS_BY_ID[root_id]
        hidden = bool(missing_unlocks(event, received, ctx.randomize_events, ctx.randomize_vehicles))
        saved = ctx.root_lists.setdefault(root_id, {})
        if not hidden:
            if saved:
                for start, ids in saved.items():
                    ctx.memory.restore_list(start, ids)
                saved.clear()
                opened.append(f"{event['name']} ({side})")
            continue
        # cached lists: put the event out again if the game wrote it back
        for start, ids in saved.items():
            data = ctx.memory.read(start - 8, 4)
            if data is not None and struct.unpack("<I", data)[0] == len(ids):
                ctx.memory.remove_from_list(start, ids, root_id)
        last = ctx.last_root_scan.get(root_id, 0.0)
        if saved and time.monotonic() - last < ROOT_RESCAN_SECONDS:
            continue
        if not saved and time.monotonic() - last < TREE_RESCAN_SECONDS * 5:
            continue
        ctx.last_root_scan[root_id] = time.monotonic()
        for start, ids in ctx.memory.find_event_lists(root_id):  # lists are rebuilt on career load
            saved[start] = ids
            ctx.memory.remove_from_list(start, ids, root_id)
    return opened


def received_names(ctx: NFSHPRContext) -> Set[str]:
    return {ctx.item_names.lookup_in_game(item.item) for item in ctx.items_received}


def enforce_locks(ctx: NFSHPRContext) -> None:
    """Hold the car still in an event Archipelago has not unlocked yet."""
    if not (ctx.randomize_events or ctx.randomize_vehicles):
        return
    event_id = ctx.memory.read_event_id(EVENTS_BY_ID)
    if event_id is None:
        return
    event = EVENTS_BY_ID[event_id]
    vehicle = None
    if ctx.randomize_vehicles and ctx.memory.weapons_address is None \
            and time.monotonic() - ctx.last_weapons_scan >= RESCAN_SECONDS:
        if not ctx.memory.locate_weapons():  # the car id is read next to the weapon cells
            ctx.last_weapons_scan = time.monotonic()
    if ctx.randomize_vehicles and ctx.memory.weapons_address is not None:
        vehicle_id = ctx.memory.read_vehicle_id(VEHICLES_BY_ID)
        vehicle = VEHICLES_BY_ID.get(vehicle_id) if vehicle_id is not None else None
    missing = missing_unlocks(event, received_names(ctx), ctx.randomize_events, ctx.randomize_vehicles, vehicle)
    if not missing:
        if ctx.locked_event == event_id:
            logger.info(f"{event['name']} is now unlocked.")
        ctx.locked_event = None
        ctx.lock_seen = None
        return
    if ctx.lock_thread and ctx.lock_thread.is_alive():
        return
    if not ctx.memory.player_body_ok() and not ctx.memory.locate_player_body():
        return
    velocity = ctx.memory.read_velocity()
    if velocity is None or speed_of(velocity) < 0.5:
        return  # not driving (map, menus, start line): nothing to hold yet
    # Let the event's scripted start finish first (rolling starts, intro camera): holding the car
    # during it can leave the game stuck with no pause menu.
    if ctx.lock_seen != event_id:
        ctx.lock_seen, ctx.lock_seen_at = event_id, time.monotonic()
    if time.monotonic() - ctx.lock_seen_at < LOCK_GRACE_SECONDS:
        return
    if ctx.locked_event != event_id:
        car = f" with the {vehicle[1]}" if vehicle else ""
        logger.info(f"{event['name']} ({event['side']}){car} is locked in Archipelago: missing "
                    f"{', '.join(missing)}. Quit it from the pause menu.")
    ctx.locked_event = event_id

    def still_locked() -> bool:
        if not (ctx.server and ctx.slot):
            return False  # disconnected: let go
        if ctx.locked_event != event_id or ctx.memory.read_event_id(EVENTS_BY_ID) != event_id:
            return False
        # Still the same car? (a restart with another car may be allowed)
        if vehicle is not None:
            return VEHICLES_BY_ID.get(ctx.memory.read_vehicle_id(VEHICLES_BY_ID)) == vehicle
        return True

    ctx.trap_stop.clear()
    ctx.lock_thread = threading.Thread(target=hold_car, args=(ctx.memory, still_locked, ctx.trap_stop),
                                       name="NFSHPRLock", daemon=True)
    ctx.lock_thread.start()


def apply_weapons(ctx: NFSHPRContext) -> None:
    """At each event (re)start, set the player's weapon charges from the progressive items received."""
    if not ctx.randomize_weapons:
        return
    event_id = ctx.memory.read_event_id(EVENTS_BY_ID)
    if event_id is None:
        return
    if ctx.memory.weapons_address is None and time.monotonic() - ctx.last_weapons_scan < RESCAN_SECONDS:
        return
    if not ctx.memory.locate_weapons():
        ctx.last_weapons_scan = time.monotonic()
        return
    state = ctx.memory.read_weapons()
    if state is None:
        return
    live = state[0]
    event = EVENTS_BY_ID[event_id]
    side = event["side"]
    cells = side_cells(side)

    if not ctx.memory.player_body_ok() and time.monotonic() - ctx.last_body_scan >= 5.0:
        ctx.last_body_scan = time.monotonic()  # full memory scan: not more than every 5 s
        ctx.memory.locate_player_body()
    velocity = ctx.memory.read_velocity()
    position = ctx.memory.read_position()

    restarted = event_id != ctx.weapon_event or ctx.weapon_live is None
    if not restarted:
        # Weapons never refill during an event; the car only jumps far when the event restarts.
        restarted = any(live[c] > ctx.weapon_live[c] for c in cells)
        if position and ctx.weapon_position:
            jump = sum((a - b) ** 2 for a, b in zip(position, ctx.weapon_position)) ** 0.5
            restarted = restarted or jump > 300.0
    if restarted:
        ctx.weapons_pending = True
        ctx.weapons_disarm = False
    ctx.weapon_event, ctx.weapon_position = event_id, position
    ctx.weapon_live = list(live)
    if ctx.weapons_disarm:
        # No charge for this side: weapon intro events still hold one weapon ready, take it away.
        if ctx.memory.disarm_weapon():
            logger.debug("Disarmed the weapon the event held ready.")
    if not ctx.weapons_pending:
        return
    # Wait until the car moves: the game updates the event id and charges a moment after the start.
    if velocity is None or speed_of(velocity) < 1.0:
        return

    received = [ctx.item_names.lookup_in_game(item.item) for item in ctx.items_received]
    targets = target_charges(side, live, weapon_levels(received))
    for cell, charges in targets.items():
        if live[cell] != charges:
            ctx.memory.write_weapon(cell, charges)
            ctx.weapon_live[cell] = charges
    ctx.weapons_pending = False
    ctx.weapons_disarm = sum(targets.get(cell, live[cell]) for cell in cells) == 0
    if ctx.weapons_disarm:
        ctx.memory.disarm_weapon()
    summary = ", ".join(f"{WEAPON_LABELS[cell]} {charges}" for cell, charges in sorted(targets.items()))
    logger.info(f"Weapons for {event['name']} ({side}): {summary or 'none in this event'}.")


def start_trap(ctx: NFSHPRContext) -> None:
    """Start the next pending trap once the player is driving (one trap at a time)."""
    if not ctx.pending_traps or (ctx.trap_thread and ctx.trap_thread.is_alive()):
        return
    if time.monotonic() < ctx.trap_retry_at:  # the last try found no car to hit: wait a bit
        return
    if not ctx.memory.player_body_ok():
        if time.monotonic() - ctx.last_body_scan < RESCAN_SECONDS:
            return
        ctx.last_body_scan = time.monotonic()
        if not ctx.memory.locate_player_body():
            return
    velocity = ctx.memory.read_velocity()
    if not velocity or speed_of(velocity) < MOVING:
        return
    name = ctx.pending_traps[0]
    if name == "Trap - System Jammed" and ctx.memory.read_nitro() is None and ctx.memory.locate_nitro() != 1:
        return
    ctx.trap_stop.clear()

    def trap() -> None:
        try:
            run_trap(ctx.memory, name, float(TRAP_DURATIONS.get(name, 0)), logger.info, ctx.trap_stop,
                     ctx.trap_delay)
        except Exception:  # did not trigger: keep it, try again a bit later
            ctx.trap_retry_at = time.monotonic() + TRAP_RETRY_SECONDS
            return
        if ctx.pending_traps and ctx.pending_traps[0] == name:
            ctx.pending_traps.pop(0)
            ctx.save_state()

    ctx.trap_thread = threading.Thread(target=trap, name="NFSHPRTrap", daemon=True)
    ctx.trap_thread.start()


def apply_nitro(ctx: NFSHPRContext) -> None:
    """Add one pending Nitro Refill once an event is running.

    Out of an event the gauge keeps its last value, so a gauge that moves between
    two looks (2 s apart) means the player is driving in an event, not paused.
    """
    if not ctx.pending_nitro:
        ctx.last_gauge = None
        return
    gauge = ctx.memory.read_nitro()
    if gauge is None:
        if time.monotonic() - ctx.last_nitro_scan < RESCAN_SECONDS:
            return
        ctx.last_nitro_scan = time.monotonic()
        if ctx.memory.locate_nitro() != 1:
            return
        gauge = ctx.memory.read_nitro()
        ctx.last_gauge = None
        if gauge is None:
            return
    previous, ctx.last_gauge = ctx.last_gauge, gauge
    if previous is None or gauge == previous or gauge >= 100.0:
        return  # not racing (map, menu, pause) or nothing to fill
    name = ctx.pending_nitro[0]
    amount = NITRO_REFILL_VALUES[name]
    new_gauge = 100.0 if amount >= 100 else min(100.0, gauge + amount)
    if ctx.memory.write_nitro(new_gauge):
        ctx.pending_nitro.pop(0)
        ctx.save_state()
        ctx.last_gauge = new_gauge
        logger.info(f"Applied {name}: nitro {gauge:.0f}% -> {new_gauge:.0f}%.")


def apply_bounty(ctx: NFSHPRContext) -> None:
    """Make the game's displayed bounty equal career bounty + Bounty Bundles.

    The save only keeps the career bounty earned in events; the game rebuilds the
    displayed bounty from it at launch. So the bundles are written again into
    every new game process, as a difference on top of what the game shows.
    """
    missing = [ctx.bundle_bounty[i] - ctx.mem_applied[i] for i in (0, 1)]
    if missing == [0, 0]:
        return
    if ctx.save_bounty is None:
        ctx.wait("Waiting for the save file to apply Bounty Bundles...")
        return

    current = ctx.memory.read_bounty()
    if current is not None and still_bounty(ctx, current):
        ctx.mem_reference = current
    else:
        current = locate_bounty(ctx)
        if current is None:
            return

    missing = [ctx.bundle_bounty[i] - ctx.mem_applied[i] for i in (0, 1)]
    if missing == [0, 0]:
        ctx.waiting_reason = ""
        logger.info("Bounty Bundles were already applied in game.")
        return
    racer, cop = current[0] + missing[0], current[1] + missing[1]
    if not ctx.memory.write_bounty(racer, cop):
        ctx.wait("Could not write the bounty to game memory, retrying...")
        return
    ctx.mem_applied = list(ctx.bundle_bounty)
    ctx.mem_reference = (racer, cop)
    ctx.save_mtime = 0.0  # re-evaluate level and vehicle checks with the applied bounty
    ctx.waiting_reason = ""
    logger.info(f"Game bounty is now Racer {racer:,} / Cop {cop:,}.")


def still_bounty(ctx: NFSHPRContext, current: Tuple[int, int]) -> bool:
    """The cached address still holds the bounty: it only ever goes up, by event-sized steps."""
    reference = ctx.mem_reference
    return reference is not None and all(0 <= now - before <= MAX_BOUNTY_JUMP
                                         for now, before in zip(current, reference))


def locate_bounty(ctx: NFSHPRContext) -> Optional[Tuple[int, int]]:
    """Find the displayed (racer, cop) bounty in memory.

    It is the career bounty from the save plus whatever bundle bounty is already in
    this game process: what we wrote so far, or all of it if an earlier client run
    already applied it before this client was restarted.
    """
    save = ctx.save_bounty
    candidates = [tuple(ctx.mem_applied)]
    if list(ctx.bundle_bounty) != ctx.mem_applied:
        candidates.append(tuple(ctx.bundle_bounty))
    # A full scan takes seconds: only retry when the save changed, or every 30 s.
    last_save, last_time = ctx.last_scan
    if save == last_save and time.monotonic() - last_time < RESCAN_SECONDS:
        return None
    ctx.last_scan = (save, time.monotonic())

    ambiguous = False
    for applied in candidates:
        expected = (save[0] + applied[0], save[1] + applied[1])
        matches = ctx.memory.locate_bounty(*expected)
        if matches == 1:
            ctx.mem_applied = list(applied)
            ctx.mem_reference = expected
            ctx.save_mtime = 0.0
            return expected
        ambiguous |= matches > 1
    ctx.memory.bounty_address = None
    ctx.wait("Bounty is ambiguous in game memory (bounty too low on both sides): "
             "it will be applied after your next event." if ambiguous else
             "Bounty not found in game memory yet: it will be applied once your career is loaded "
             "and you are on the map.")
    return None


def launch(*launch_args: str) -> None:
    async def main() -> None:
        parser = get_base_parser(description="Need for Speed Hot Pursuit Remastered Client")
        args = parser.parse_args(launch_args)

        ctx = NFSHPRContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        watcher = asyncio.create_task(save_watcher(ctx), name="SaveWatcher")
        applier = asyncio.create_task(item_applier(ctx), name="ItemApplier")
        weapons = asyncio.create_task(weapon_watcher(ctx), name="WeaponWatcher")
        await ctx.exit_event.wait()
        ctx.server_address = None
        watcher.cancel()
        applier.cancel()
        weapons.cancel()
        ctx.trap_stop.set()
        ctx.memory.detach()
        await ctx.shutdown()

    Utils.init_logging("NFSHPRClient")
    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
