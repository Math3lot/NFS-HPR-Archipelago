"""
Trap effects, run in a background thread while the player drives.

Timed traps only count time while the car is actually moving in an event
(position changes), so pausing the game does not burn their duration.
"""
from __future__ import annotations

import math
import random
import threading
import time
from typing import Callable, Optional

from .GameMemory import GameMemory

TICK = 0.02                 # 50 writes per second
SPEED_LIMIT = 20.0          # m/s (72 km/h) while the Speed Limiter is on
MOVING = 3.0                # m/s: above this the player is driving

SUPPORTED_TRAPS = {
    "Trap - Roadblock Deployed",
    "Trap - Speed Limiter 10s",
    "Trap - System Jammed",
    "Trap - EMP Impact",
    "Trap - Flat Tire",
    "Trap - Reversed Steering",
}
EMP_DAMAGE = 0.25            # damage added by the EMP (0..1, the car is wrecked near 1)
FLAT_TIRE_DAMAGE = 0.15      # damage added when the tire blows
DAMAGE_TRAPS = {"Trap - EMP Impact": EMP_DAMAGE, "Trap - Flat Tire": FLAT_TIRE_DAMAGE}
EMP_SPEED_KEPT = 0.35        # the EMP hit keeps 35 % of the speed
EMP_SPIN = 2.5               # rad/s of yaw jolt
FLAT_TIRE_SPEED = 0.6        # flat tire: speed capped at 60 % of the speed when it blew
# When the tire blows the car either spins a full turn or fishtails, like a spike strip hit.
SPIN_RATE = 8.0              # rad/s pushed until the car has really turned 360 degrees
SPIN_MAX_TIME = 3.5          # s: give up the spin after this (car stuck against a wall...)
SPIN_SPEED_LOSS = 0.985      # velocity kept per tick while spinning
SKID_TIME = 2.5              # s of fishtailing
SKID_YAW = 3.0               # rad/s at the start, fading out
SKID_PERIOD = 0.9            # s per left-right swing
SKID_SPEED_LOSS = 0.993


_flat_count = 0


def _next_flat_spin() -> bool:
    """Flat tires alternate: spin out, then skid, then spin out..."""
    global _flat_count
    _flat_count += 1
    return _flat_count % 2 == 1


def speed_of(velocity) -> float:
    return math.sqrt(sum(c * c for c in velocity))


def drive_for(memory: GameMemory, seconds: float, stop: threading.Event) -> bool:
    """Wait until the car has been driving (position changing) for `seconds`. False if the event ended."""
    last_position = memory.read_position()
    last_time = time.monotonic()
    while seconds > 0 and not stop.is_set():
        time.sleep(TICK * 5)
        now = time.monotonic()
        position = memory.read_position() if memory.player_body_ok() else None
        if position is None:
            return False
        if position != last_position:
            seconds -= now - last_time
        last_position, last_time = position, now
    return not stop.is_set()


def run_trap(memory: GameMemory, name: str, duration: float, log: Callable[[str], None],
             stop: threading.Event, delay: float = 0.0) -> None:
    steering_lock: Optional[float] = None  # reversed steering: the car's normal lock, to put back
    try:
        if delay > 0:
            log(f"Incoming: {name[7:]} in {delay:g} seconds of driving!")
            if name in DAMAGE_TRAPS or name == "Trap - Reversed Steering":
                memory.locate_damage()  # memory scan done during the warning, so the hit is instant
            if not drive_for(memory, delay, stop):
                log(f"{name[7:]} did not trigger (event over), it will come back.")
                raise _Requeue()
        damage_note = ""
        if name in DAMAGE_TRAPS:
            damage = memory.add_damage(DAMAGE_TRAPS[name])
            if damage is None:  # free drive or menus: no damage there, try again later in an event
                log(f"{name[7:]}: your car was not found ({memory.damage_debug}), it will come back in an event.")
                raise _Requeue()
            damage_note = f" Damage {damage:.0%}."
        if name == "Trap - Roadblock Deployed":
            # Hit a roadblock: the car stops dead. Repeat briefly so a physics step cannot undo it.
            end = time.monotonic() + 0.3
            while time.monotonic() < end and not stop.is_set():
                memory.write_velocity((0.0, 0.0, 0.0))
                time.sleep(TICK)
            log("Roadblock! Your car was stopped.")
            return

        if name == "Trap - EMP Impact":
            velocity = memory.read_velocity()
            angular = memory.read_angular()
            if velocity:
                memory.write_velocity(tuple(c * EMP_SPEED_KEPT for c in velocity))
            if angular:
                memory.write_angular((angular[0], angular[1] + random.choice((-1, 1)) * EMP_SPIN, angular[2]))
            log(f"EMP Impact! Your car lost most of its speed.{damage_note}")
            return

        remaining = duration
        start_velocity = memory.read_velocity()
        flat_cap = max(SPEED_LIMIT, speed_of(start_velocity) * FLAT_TIRE_SPEED) if start_velocity else SPEED_LIMIT
        flat_mode = "spin" if name == "Trap - Flat Tire" and _next_flat_spin() else "skid"
        flat_side = random.choice((-1, 1))
        spun, last_heading = 0.0, None
        if name == "Trap - Reversed Steering":
            lock = memory.read_steering_lock()
            if lock is None:
                log(f"Reversed Steering: your car was not found ({memory.damage_debug or 'unexpected values'}), "
                    "it will come back in an event.")
                raise _Requeue()
            steering_lock = abs(lock)
            memory.write_steering_lock(-steering_lock)
        last_position: Optional[tuple] = memory.read_position()
        last_time = time.monotonic()
        if name == "Trap - Flat Tire":
            log(f"Flat Tire! Your car {'spins out' if flat_mode == 'spin' else 'skids'}, "
                f"slowed for {duration:g} seconds.{damage_note}")
        else:
            log(f"{name[7:]} active for {duration:g} seconds.{damage_note}")
        while remaining > 0 and not stop.is_set():
            now = time.monotonic()
            position = memory.read_position()
            if position is None:
                break  # car gone (event over)
            position_moved = position != last_position
            if position_moved:  # game running, not paused
                remaining -= now - last_time
            last_position, last_time = position, now

            if name == "Trap - Speed Limiter 10s":
                velocity = memory.read_velocity()
                if velocity:
                    speed = speed_of(velocity)
                    if speed > SPEED_LIMIT:
                        scale = SPEED_LIMIT / speed
                        memory.write_velocity(tuple(c * scale for c in velocity))
            elif name == "Trap - System Jammed":
                if memory.read_nitro() is not None:
                    memory.write_nitro(0.0)
            elif name == "Trap - Flat Tire":
                driven = duration - remaining
                velocity = memory.read_velocity()
                angular = memory.read_angular()
                if flat_mode == "spin" and spun < 2 * math.pi and driven < SPIN_MAX_TIME:
                    # full turn, the car keeps sliding the way it went. The tires fight the
                    # rotation between writes, so measure the angle the car body really turned
                    # (its heading) and keep pushing until it reaches 360 degrees.
                    heading = memory.read_heading()
                    if heading is not None:
                        if last_heading is not None:
                            step = (heading - last_heading + math.pi) % (2 * math.pi) - math.pi
                            if step * flat_side > 0:  # only count turning the way we push
                                spun += abs(step)
                        last_heading = heading
                    if angular:
                        memory.write_angular((angular[0], flat_side * SPIN_RATE, angular[2]))
                    if velocity:
                        memory.write_velocity(tuple(c * SPIN_SPEED_LOSS for c in velocity))
                elif flat_mode == "skid" and driven < SKID_TIME:
                    # the rear swings left and right, less and less
                    fade = 1.0 - driven / SKID_TIME
                    yaw = flat_side * SKID_YAW * fade * math.sin(2 * math.pi * driven / SKID_PERIOD)
                    if angular and speed_of(velocity or (0, 0, 0)) > MOVING:
                        memory.write_angular((angular[0], yaw, angular[2]))
                    if velocity:
                        memory.write_velocity(tuple(c * SKID_SPEED_LOSS for c in velocity))
                elif velocity:
                    speed = speed_of(velocity)
                    if speed > flat_cap:
                        memory.write_velocity(tuple(c * flat_cap / speed for c in velocity))
            elif name == "Trap - Reversed Steering" and steering_lock is not None:
                # The game keeps the steering lock, but put it back if it was reset (car respawn).
                lock = memory.read_steering_lock(relocate=False)
                if lock is not None and lock > 0:
                    steering_lock = lock
                    memory.write_steering_lock(-lock)
                time.sleep(0.2)
            time.sleep(TICK)
        log(f"{name[7:]} is over.")
    except OSError as error:
        log(f"{name[7:]} stopped early: {error}")
    finally:
        if name == "Trap - Reversed Steering" and steering_lock is not None:
            try:
                lock = memory.read_steering_lock(relocate=False)
                if lock is not None and lock < 0:
                    memory.write_steering_lock(steering_lock)
            except OSError:
                pass


class _Requeue(Exception):
    """The trap could not trigger: the caller puts it back in the queue."""
