"""
Reads and writes the memory of the running game (Windows only, ctypes only).

Bounty layout found in memory: two adjacent u32, cop bounty then racer bounty.
The address changes every launch, so it is found by searching for the pair of
values read from the save file, then cached while it keeps matching.

Nitro gauge: f32 from 0 to 100, 0x108 bytes after the ASCII tag "EFIN". The
structure stays at the same address between events; out of an event the gauge
keeps its last value.

Physics bodies (16-byte aligned, 0x100 apart in a pool): mass f32 at +0x0C,
1/mass at +0x1C, gravity -9.81 at +0x2C, velocity x, y, z at +0x40 (world axes,
m/s), position x, y, z at +0x90. The player's car is the first vehicle body of
the pool (lowest address); opponents and traffic follow.
"""
from __future__ import annotations

import ctypes
import math
import struct
import sys
from typing import Iterator, List, Optional, Tuple

PROCESS_NAME = "NFS11Remastered.exe"
IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    from ctypes import wintypes

    _k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _k32.OpenProcess.restype = wintypes.HANDLE
    _k32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    _k32.ReadProcessMemory.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p,
                                       ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
    _k32.WriteProcessMemory.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p,
                                        ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
    _k32.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    _k32.CloseHandle.argtypes = [wintypes.HANDLE]

    class _MBI(ctypes.Structure):
        _fields_ = [
            ("BaseAddress", ctypes.c_void_p), ("AllocationBase", ctypes.c_void_p),
            ("AllocationProtect", wintypes.DWORD), ("PartitionId", wintypes.WORD),
            ("RegionSize", ctypes.c_size_t), ("State", wintypes.DWORD),
            ("Protect", wintypes.DWORD), ("Type", wintypes.DWORD),
        ]

    class _PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD), ("th32DefaultHeapID", ctypes.c_void_p),
            ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD), ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", wintypes.DWORD), ("szExeFile", ctypes.c_wchar * 260),
        ]

    _k32.VirtualQueryEx.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.POINTER(_MBI), ctypes.c_size_t]
    _k32.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(_PROCESSENTRY32W)]
    _k32.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(_PROCESSENTRY32W)]

_ACCESS = 0x0400 | 0x0010 | 0x0020 | 0x0008  # query, read, write, operation
_STILL_ACTIVE = 259
_WRITABLE = 0x04 | 0x08 | 0x40 | 0x80
_MEM_COMMIT, _PAGE_GUARD, _PAGE_NOACCESS = 0x1000, 0x100, 0x01

NITRO_TAG = b"EFIN"
NITRO_GAUGE_OFFSET = 0x108
NITRO_MAX = 100.0

GRAVITY = struct.pack("<f", -9.81)
BODY_GRAVITY = 0x2C
BODY_MASS, BODY_INVERSE_MASS = 0x0C, 0x1C
BODY_VELOCITY, BODY_ANGULAR, BODY_POSITION = 0x40, 0x50, 0x90
BODY_FORWARD = 0x80   # rotation matrix rows at 0x60 (side), 0x70 (up), 0x80 (forward)
VEHICLE_MIN_MASS = 500.0

# Weapon charges: 9 u32 cells, one per weapon type (both sides), found by a marker
# 0x4BEA160D at cells-0x73C and cells+0x438. The event's starting loadout is a
# copy 0x3C0 bytes after the live cells.
WEAPON_MARKER = struct.pack("<I", 0x4BEA160D)
WEAPON_MARKER_BEFORE, WEAPON_MARKER_AFTER = 0x73C, 0x438
WEAPON_CELLS = 9
WEAPON_LOADOUT = 0x3C0
WEAPON_ARMED = 0x1CC   # f32 before the cells: 1.0 while a weapon is ready to fire (weapon intro events arm one)

# The player's vehicle id: copies at fixed distances before the weapon cells.
VEHICLE_ID_OFFSETS = (0xEB20, 0xDCA8, 0xCE30, 0xB140)

# The current event id sits at a fixed address (checked across restarts: 0x12B660);
# the others followed it in one session only and are fallbacks.
EVENT_ID_ADDRESSES = (0x12B660, 0x12B698, 0x1525D0, 0x1592F0, 0x159340, 0x1593A8, 0x1595A0)

# Vehicle damage: 4 equal f32 lanes, 0 (new) to 1 (wrecked on the next big hit), one block per car.
# Found by 4 x FLT_MAX at +0x140; the car's position (x, y, z) is at -0xF0.
DAMAGE_MARKER = struct.pack("<f", 3.4028234663852886e38) * 4
DAMAGE_MARKER_OFFSET = 0x140
DAMAGE_POSITION = -0xF0
DAMAGE_MAX_DISTANCE = 20.0   # m between the block's position and the player's body
# Steering lock (degrees, f32) of the same car, at fixed distances before its damage block.
# Making it negative reverses the steering (wheels, physics and drift follow).
STEERING_LOCK_OFFSETS = (-0x164C, -0x15F0)
STEERING_LOCK_RANGE = (10.0, 60.0)

# Event unlock tree (see EventUnlocks.py): found from one node, the others are at known offsets.
TREE_ANCHOR_EVENT = 572460  # Racer - Title Fight

MIN_LOCATABLE_BOUNTY = 1000  # below this the (cop, racer) pair is everywhere in memory

CHUNK = 64 * 1024 * 1024
OVERLAP = 0x1000


def find_pid() -> Optional[int]:
    snapshot = _k32.CreateToolhelp32Snapshot(0x2, 0)  # TH32CS_SNAPPROCESS
    if not snapshot or snapshot == wintypes.HANDLE(-1).value:
        return None
    entry = _PROCESSENTRY32W()
    entry.dwSize = ctypes.sizeof(entry)
    try:
        ok = _k32.Process32FirstW(snapshot, ctypes.byref(entry))
        while ok:
            if entry.szExeFile.lower() == PROCESS_NAME.lower():
                return int(entry.th32ProcessID)
            ok = _k32.Process32NextW(snapshot, ctypes.byref(entry))
    finally:
        _k32.CloseHandle(snapshot)
    return None


class GameMemory:
    def __init__(self) -> None:
        self.pid: Optional[int] = None
        self.handle = None
        self.bounty_address: Optional[int] = None
        self.nitro_tag_address: Optional[int] = None
        self.body_address: Optional[int] = None
        self.weapons_address: Optional[int] = None
        self.damage_address: Optional[int] = None
        self.damage_debug = ""
        self.tree_base: Optional[int] = None

    # ------------------------------------------------------------------ process

    def attach(self) -> bool:
        """Open the game process if needed. False when the game is not running."""
        if not IS_WINDOWS:
            return False
        if self.handle and self._alive():
            return True
        self.detach()
        pid = find_pid()
        if pid is None:
            return False
        handle = _k32.OpenProcess(_ACCESS, False, pid)
        if not handle:
            raise PermissionError("Could not open the game process: run the client as administrator.")
        self.pid, self.handle = pid, handle
        return True

    def detach(self) -> None:
        if self.handle:
            _k32.CloseHandle(self.handle)
        self.pid = self.handle = self.bounty_address = self.nitro_tag_address = self.body_address = None
        self.weapons_address = self.damage_address = self.tree_base = None

    def _alive(self) -> bool:
        code = wintypes.DWORD()
        return bool(_k32.GetExitCodeProcess(self.handle, ctypes.byref(code))) and code.value == _STILL_ACTIVE

    def read(self, address: int, size: int) -> Optional[bytearray]:
        buf = bytearray(size)
        read = ctypes.c_size_t()
        target = (ctypes.c_char * size).from_buffer(buf)
        if not _k32.ReadProcessMemory(self.handle, ctypes.c_void_p(address), target, size, ctypes.byref(read)):
            return None
        return buf if read.value == size else None

    def write(self, address: int, data: bytes) -> bool:
        written = ctypes.c_size_t()
        ok = _k32.WriteProcessMemory(self.handle, ctypes.c_void_p(address), data, len(data), ctypes.byref(written))
        return bool(ok) and written.value == len(data)

    def _regions(self) -> Iterator[Tuple[int, bytearray]]:
        """Writable committed memory, big regions read in overlapping 64 MB chunks."""
        address, mbi = 0, _MBI()
        while _k32.VirtualQueryEx(self.handle, ctypes.c_void_p(address), ctypes.byref(mbi), ctypes.sizeof(mbi)):
            size = mbi.RegionSize
            if mbi.State == _MEM_COMMIT and mbi.Protect & _WRITABLE and not mbi.Protect & (_PAGE_GUARD | _PAGE_NOACCESS):
                offset = 0
                while offset < size:
                    data = self.read(address + offset, min(CHUNK + OVERLAP, size - offset))
                    if data:
                        yield address + offset, data
                    offset += CHUNK
            address += size
            if address >= 0x7FFFFFFFFFFF:
                break

    def find_all(self, needle: bytes, alignment: int = 4, limit: int = 100000) -> List[int]:
        """Addresses holding needle. Stops after `limit` hits: a common needle (all zeros...)
        would otherwise list millions of addresses and eat the memory."""
        hits = set()
        for base, data in self._regions():
            i = data.find(needle)
            while i != -1:
                if (base + i) % alignment == 0:
                    hits.add(base + i)
                    if len(hits) > limit:
                        return sorted(hits)
                i = data.find(needle, i + 1)
        return sorted(hits)  # chunks overlap

    # ------------------------------------------------------------------ bounty

    def read_bounty(self) -> Optional[Tuple[int, int]]:
        """(racer, cop) at the cached address, or None."""
        if self.bounty_address is None:
            return None
        data = self.read(self.bounty_address, 8)
        if data is None:
            return None
        cop, racer = struct.unpack("<II", data)
        return racer, cop

    def locate_bounty(self, racer: int, cop: int) -> int:
        """Search memory for the (cop, racer) pair. Returns the number of matches; caches a unique one."""
        if max(racer, cop) < MIN_LOCATABLE_BOUNTY:
            self.bounty_address = None
            return 2  # far too common a pair to be found (new career): ambiguous
        hits = self.find_all(struct.pack("<II", cop, racer), limit=1)
        self.bounty_address = hits[0] if len(hits) == 1 else None
        return len(hits)

    def write_bounty(self, racer: int, cop: int) -> bool:
        if self.bounty_address is None:
            return False
        return self.write(self.bounty_address, struct.pack("<II", cop, racer))

    # ------------------------------------------------------------------ nitro

    def _gauge_at(self, tag_address: int) -> Optional[float]:
        data = self.read(tag_address, NITRO_GAUGE_OFFSET + 4)
        if data is None or bytes(data[:4]) != NITRO_TAG:
            return None
        gauge = struct.unpack_from("<f", data, NITRO_GAUGE_OFFSET)[0]
        return gauge if 0.0 <= gauge <= NITRO_MAX else None

    def locate_nitro(self) -> int:
        """Search memory for the nitro structure. Returns the number of matches; caches a unique one."""
        hits = [a for a in self.find_all(NITRO_TAG) if self._gauge_at(a) is not None]
        self.nitro_tag_address = hits[0] if len(hits) == 1 else None
        return len(hits)

    def read_nitro(self) -> Optional[float]:
        if self.nitro_tag_address is None:
            return None
        gauge = self._gauge_at(self.nitro_tag_address)
        if gauge is None:
            self.nitro_tag_address = None
        return gauge

    def write_nitro(self, gauge: float) -> bool:
        if self.nitro_tag_address is None:
            return False
        value = max(0.0, min(NITRO_MAX, gauge))
        return self.write(self.nitro_tag_address + NITRO_GAUGE_OFFSET, struct.pack("<f", value))

    # ------------------------------------------------------------------ player car physics

    def _is_vehicle_body(self, address: int) -> bool:
        data = self.read(address, BODY_GRAVITY + 4)
        if data is None or bytes(data[BODY_GRAVITY:BODY_GRAVITY + 4]) != GRAVITY:
            return False
        mass = struct.unpack_from("<f", data, BODY_MASS)[0]
        inverse = struct.unpack_from("<f", data, BODY_INVERSE_MASS)[0]
        return mass >= VEHICLE_MIN_MASS and abs(mass * inverse - 1.0) < 0.01

    def locate_player_body(self) -> int:
        """Find vehicle bodies; the player's car is the first one. Returns the number of vehicles."""
        bodies = [hit - BODY_GRAVITY for hit in self.find_all(GRAVITY, alignment=4)
                  if (hit - BODY_GRAVITY) % 16 == 0 and self._is_vehicle_body(hit - BODY_GRAVITY)]
        self.body_address = bodies[0] if bodies else None
        return len(bodies)

    def player_body_ok(self) -> bool:
        if self.body_address is not None and not self._is_vehicle_body(self.body_address):
            self.body_address = None
        return self.body_address is not None

    def read_velocity(self) -> Optional[Tuple[float, float, float]]:
        if self.body_address is None:
            return None
        data = self.read(self.body_address + BODY_VELOCITY, 12)
        return struct.unpack("<3f", data) if data else None

    def write_velocity(self, velocity: Tuple[float, float, float]) -> bool:
        if self.body_address is None:
            return False
        return self.write(self.body_address + BODY_VELOCITY, struct.pack("<3f", *velocity))

    def read_position(self) -> Optional[Tuple[float, float, float]]:
        if self.body_address is None:
            return None
        data = self.read(self.body_address + BODY_POSITION, 12)
        return struct.unpack("<3f", data) if data else None

    # ------------------------------------------------------------------ current event and weapons

    def read_event_id(self, known_ids) -> Optional[int]:
        """The event being played: the first known event id found, most reliable address first."""
        for address in EVENT_ID_ADDRESSES:
            data = self.read(address, 4)
            if data:
                value = struct.unpack("<I", data)[0]
                if value in known_ids:
                    return value
        return None

    def _weapons_ok(self, address: int) -> bool:
        before = self.read(address - WEAPON_MARKER_BEFORE, 4)
        after = self.read(address + WEAPON_MARKER_AFTER, 4)
        return before is not None and after is not None and bytes(before) == WEAPON_MARKER == bytes(after)

    def locate_weapons(self) -> bool:
        if self.weapons_address is not None and self._weapons_ok(self.weapons_address):
            return True
        self.weapons_address = None
        for hit in self.find_all(WEAPON_MARKER):
            address = hit - WEAPON_MARKER_AFTER
            if self._weapons_ok(address):
                self.weapons_address = address
                return True
        return False

    def read_weapons(self) -> Optional[Tuple[List[int], List[int]]]:
        """(live charges, event loadout) for the 9 weapon cells."""
        if self.weapons_address is None:
            return None
        live = self.read(self.weapons_address, 4 * WEAPON_CELLS)
        loadout = self.read(self.weapons_address + WEAPON_LOADOUT, 4 * WEAPON_CELLS)
        if live is None or loadout is None:
            return None
        fmt = f"<{WEAPON_CELLS}I"
        return list(struct.unpack(fmt, live)), list(struct.unpack(fmt, loadout))

    def write_weapon(self, cell: int, charges: int) -> bool:
        if self.weapons_address is None:
            return False
        return self.write(self.weapons_address + 4 * cell, struct.pack("<I", max(0, charges)))

    def disarm_weapon(self) -> bool:
        """Take away the weapon the game holds ready (True if there was one)."""
        if self.weapons_address is None:
            return False
        data = self.read(self.weapons_address - WEAPON_ARMED, 4)
        if data is None or struct.unpack("<f", data)[0] <= 0.0:
            return False
        return self.write(self.weapons_address - WEAPON_ARMED, struct.pack("<f", 0.0))

    def read_vehicle_id(self, known_ids) -> Optional[int]:
        """The player's vehicle, read next to the weapon cells (locate_weapons first)."""
        if self.weapons_address is None:
            return None
        for offset in VEHICLE_ID_OFFSETS:
            data = self.read(self.weapons_address - offset, 4)
            if data:
                value = struct.unpack("<I", data)[0]
                if value in known_ids:
                    return value
        return None

    def read_angular(self) -> Optional[Tuple[float, float, float]]:
        """Rotation speed of the player's car (rad/s around world x, y = up, z)."""
        if self.body_address is None:
            return None
        data = self.read(self.body_address + BODY_ANGULAR, 12)
        return struct.unpack("<3f", data) if data else None

    def read_heading(self) -> Optional[float]:
        """Direction the player's car points to, in radians around the vertical axis."""
        if self.body_address is None:
            return None
        data = self.read(self.body_address + BODY_FORWARD, 12)
        if data is None:
            return None
        x, _, z = struct.unpack("<3f", data)
        return math.atan2(x, z)

    def write_angular(self, angular: Tuple[float, float, float]) -> bool:
        if self.body_address is None:
            return False
        return self.write(self.body_address + BODY_ANGULAR, struct.pack("<3f", *angular))

    # ------------------------------------------------------------------ damage

    def _damage_block(self, address: int) -> Optional[Tuple[float, Tuple[float, float, float]]]:
        """(damage, car position) if a valid damage block sits at address."""
        data = self.read(address + DAMAGE_POSITION, DAMAGE_MARKER_OFFSET - DAMAGE_POSITION + 16)
        if data is None or bytes(data[-16:]) != DAMAGE_MARKER:
            return None
        lanes = struct.unpack_from("<4f", data, -DAMAGE_POSITION)
        position = struct.unpack_from("<3f", data, 0)
        if max(lanes) - min(lanes) > 0.001 or not -0.001 <= lanes[0] <= 1.001:
            return None
        if not any(abs(c) > 1.0 for c in position) or not all(abs(c) < 100000 for c in position):
            return None
        return lanes[0], position

    def locate_damage(self) -> bool:
        """Find the damage block of the player's car (the one at the player's body position)."""
        self.damage_address = None
        blocks = []
        for hit in self.find_all(DAMAGE_MARKER, alignment=16):
            block = self._damage_block(hit - DAMAGE_MARKER_OFFSET)
            if block is not None:
                blocks.append((hit - DAMAGE_MARKER_OFFSET, block[1]))
        for attempt in range(2):
            if attempt == 1 or not self.player_body_ok():
                self.locate_player_body()  # cached body may belong to an older event
            player = self.read_position()
            if player is None:
                continue
            distances = [(sum((a - b) ** 2 for a, b in zip(pos, player)) ** 0.5, addr) for addr, pos in blocks]
            if distances:
                distance, address = min(distances)
                if distance <= DAMAGE_MAX_DISTANCE:
                    self.damage_address = address
                    return True
                self.damage_debug = f"{len(blocks)} damage blocks, nearest {distance:.0f} m away"
            else:
                self.damage_debug = "no damage block in memory"
        if player is None:
            self.damage_debug = "player car not found"
        return False

    def _damage_is_player(self) -> bool:
        """The cached block still follows the player's car (blocks are reused between events)."""
        if self.damage_address is None:
            return False
        block, player = self._damage_block(self.damage_address), self.read_position()
        if block is None or player is None:
            return False
        return sum((a - b) ** 2 for a, b in zip(block[1], player)) ** 0.5 <= DAMAGE_MAX_DISTANCE

    def read_damage(self) -> Optional[float]:
        if self.damage_address is None:
            return None
        block = self._damage_block(self.damage_address)
        if block is None:
            self.damage_address = None
            return None
        return block[0]

    def write_damage(self, damage: float) -> bool:
        if self.damage_address is None:
            return False
        return self.write(self.damage_address, struct.pack("<f", max(0.0, min(1.0, damage))) * 4)

    def read_steering_lock(self, relocate: bool = True) -> Optional[float]:
        """The player's car steering lock in degrees (negative while reversed), or None if not found."""
        if relocate and not self._damage_is_player() and not self.locate_damage():
            return None
        if self.damage_address is None:
            return None
        values = []
        for offset in STEERING_LOCK_OFFSETS:
            data = self.read(self.damage_address + offset, 4)
            if data is None:
                return None
            values.append(struct.unpack("<f", data)[0])
        low, high = STEERING_LOCK_RANGE
        if abs(values[0] - values[1]) > 0.01 or not low <= abs(values[0]) <= high:
            return None
        return values[0]

    def write_steering_lock(self, degrees: float) -> bool:
        if self.damage_address is None:
            return False
        data = struct.pack("<f", degrees)
        return all([self.write(self.damage_address + offset, data) for offset in STEERING_LOCK_OFFSETS])

    def add_damage(self, amount: float) -> Optional[float]:
        """Add damage to the player's car (locating its block if needed). New damage, or None."""
        current = self.read_damage() if self._damage_is_player() else None
        if current is None and self.locate_damage():
            current = self.read_damage()
        if current is None:
            return None
        new = min(1.0, current + amount)
        return new if self.write_damage(new) else None

    # ------------------------------------------------------------------ event unlock tree

    @staticmethod
    def _own_nodes(event_id: int):
        """The event's nodes, without the one lent to a first event (see ROOT_DONORS)."""
        from .EventUnlocks import EVENT_NODES, ROOT_DONORS
        nodes = EVENT_NODES.get(event_id, [])
        lent = [index for donor, index in ROOT_DONORS.values() if donor == event_id]
        return [node for k, node in enumerate(nodes) if k not in lent]

    def _tree_node_ok(self, base: int, event_id: int, offset: int, needs: List[int]) -> bool:
        data = self.read(base + offset, 0x18)
        if data is None:
            return False
        node_id, zero, _, count, eight = struct.unpack("<IIQII", data)
        return node_id == event_id and zero == 0 and count in (0, len(needs)) and eight == 8

    def locate_tree(self) -> bool:
        """Find the game's event unlock tree in memory (loaded before the career)."""
        from .EventUnlocks import EVENT_NODES
        self.tree_base = None
        anchor_offset = EVENT_NODES[TREE_ANCHOR_EVENT][0][0]
        for hit in self.find_all(struct.pack("<II", TREE_ANCHOR_EVENT, 0), alignment=16, limit=1000):
            base = hit - anchor_offset
            checks = [(eid, off, needs) for eid in list(EVENT_NODES)[::20] for off, needs in self._own_nodes(eid)]
            if all(self._tree_node_ok(base, eid, off, needs) for eid, off, needs in checks):
                self.tree_base = base
                return True
        return False

    def tree_ok(self) -> bool:
        from .EventUnlocks import EVENT_NODES
        if self.tree_base is None:
            return False
        offset, needs = EVENT_NODES[TREE_ANCHOR_EVENT][0]
        if not self._tree_node_ok(self.tree_base, TREE_ANCHOR_EVENT, offset, needs):
            self.tree_base = None
        return self.tree_base is not None

    def _write_needs(self, node: int, needs: List[int], ids: List[int]) -> bool:
        """Point the node's references at `ids` (one per reference)."""
        ok = True
        for k in range(len(needs)):
            data = self.read(node + 0x20 + 16 * k, 8)
            if data is None:
                return False
            reference = struct.unpack("<Q", data)[0] - 4
            ok &= self.write(reference, struct.pack("<I", ids[k]))
        return ok

    def set_event_state(self, event_id: int, side: str, state: str) -> bool:
        """state: "hidden" (needs itself: the game never opens it), "open" (needs nothing: unlocked
        by Archipelago, like the game's first events) or "vanilla" (the game's own needs)."""
        from .EventUnlocks import EVENT_NODES
        if self.tree_base is None:
            return False
        ok = True
        from .EventUnlocks import ROOT_EVENTS, ROOT_DONORS
        if event_id in ROOT_EVENTS.values() and side in ROOT_DONORS:
            return self._set_root_state(event_id, side, state)
        for offset, needs in self._own_nodes(event_id):
            if not self._tree_node_ok(self.tree_base, event_id, offset, needs):
                return False
            node = self.tree_base + offset
            ok &= self._write_needs(node, needs, [event_id] * len(needs) if state == "hidden" else needs)
            ok &= self.write(node + 0x10, struct.pack("<I", 0 if state == "open" else len(needs)))
        return ok

    def _set_root_state(self, root_id: int, side: str, state: str) -> bool:
        """A first event has no node of its own: give it the donor's spare node (hidden: needs
        itself; open: needs nothing), or hand the node back to the donor (vanilla)."""
        from .EventUnlocks import EVENT_NODES, ROOT_DONORS
        donor, index = ROOT_DONORS[side]
        offset, needs = EVENT_NODES[donor][index]
        node = self.tree_base + offset
        data = self.read(node, 0x18)
        if data is None:
            return False
        node_id, zero, _, count, eight = struct.unpack("<IIQII", data)
        if node_id not in (donor, root_id) or zero != 0 or eight != 8 or count not in (0, len(needs)):
            return False
        if state == "vanilla":
            ids, owner, count = needs, donor, len(needs)
        else:
            ids, owner, count = [root_id] * len(needs), root_id, 0 if state == "open" else len(needs)
        return (self._write_needs(node, needs, ids) and self.write(node + 0x10, struct.pack("<I", count))
                and self.write(node, struct.pack("<I", owner)))

    HIDDEN_VEHICLE_BOUNTY = 0x7FFFFFFF

    def set_vehicle_state(self, vehicle_id: int, side: str, state: str) -> bool:
        """state: "hidden" (unreachable bounty), "open" (no bounty, no event needed: unlocked by
        Archipelago) or "vanilla"."""
        from .EventUnlocks import VEHICLE_NODES
        if self.tree_base is None or vehicle_id not in VEHICLE_NODES:
            return False
        offset, bounty, needs = VEHICLE_NODES[vehicle_id]
        node = self.tree_base + offset
        data = self.read(node, 0x18)
        if data is None:
            return False
        node_id, _, _, count, eight = struct.unpack("<IIQII", data)
        if node_id != vehicle_id or eight != 8 or count not in (0, len(needs)):
            return False
        value = {"hidden": self.HIDDEN_VEHICLE_BOUNTY, "open": 0, "vanilla": bounty}[state]
        return (self.write(node + 4, struct.pack("<I", value)) and self._write_needs(node, needs, needs)
                and self.write(node + 0x10, struct.pack("<I", 0 if state == "open" else len(needs))))

    # ------------------------------------------------------------------ map lists (first events)
    # The game's first events have no unlock node: they are always on the map. The map draws its
    # events from small lists in memory: u64 pointer to the ids (just after the header), u32 count,
    # u32 4, then the u32 event ids. Removing an event from them keeps it off the map.

    def find_event_lists(self, event_id: int) -> List[Tuple[int, List[int]]]:
        """(ids address, ids) of every map list holding this event."""
        found = {}
        for hit in self.find_all(struct.pack("<I", event_id), alignment=4, limit=5000):
            header = self.read(hit - 0x10, 0x10)
            if header is None:
                continue
            for start in range(hit - 4 * 63, hit + 4, 4):  # the event may sit anywhere in the list
                head = self.read(start - 0x10, 0x10)
                if head is None:
                    continue
                pointer, count, size = struct.unpack("<QII", head)
                if pointer == start and size == 4 and 1 <= count <= 64 and start <= hit < start + 4 * count:
                    data = self.read(start, 4 * count)
                    if data is not None:
                        found[start] = list(struct.unpack(f"<{count}I", data))
                    break
        return sorted(found.items())

    def remove_from_list(self, start: int, ids: List[int], event_id: int) -> bool:
        kept = [i for i in ids if i != event_id]
        if len(kept) == len(ids):
            return True
        body = struct.pack(f"<{len(kept)}I", *kept) + struct.pack("<I", ids[-1]) * (len(ids) - len(kept))
        return self.write(start, body) and self.write(start - 8, struct.pack("<I", len(kept)))

    def restore_list(self, start: int, ids: List[int]) -> bool:
        return self.write(start, struct.pack(f"<{len(ids)}I", *ids)) and \
            self.write(start - 8, struct.pack("<I", len(ids)))
