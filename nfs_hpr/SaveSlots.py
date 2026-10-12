"""
One game save per Archipelago seed.

The game keeps a single career in its Save folder. The client stores copies of
that folder's files in Archipelago's nfs_hpr_saves folder, one per seed (plus the
player's own career, "original"), and swaps them in while the game is closed.
Nothing is ever deleted without a copy being stored first.
"""
from __future__ import annotations

import os
import re
import shutil
import time
from typing import List, Optional

import Utils

STASH_FOLDER = "nfs_hpr_saves"


def stash_root() -> str:
    path = Utils.user_path(STASH_FOLDER)
    os.makedirs(path, exist_ok=True)
    return path


def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_") or "save"


def stashes() -> List[str]:
    root = stash_root()
    return sorted(n for n in os.listdir(root) if os.path.isdir(os.path.join(root, n)))


def _files(folder: str) -> List[str]:
    if not os.path.isdir(folder):
        return []
    return [n for n in os.listdir(folder) if os.path.isfile(os.path.join(folder, n))]


def stash(game_folder: str, name: str) -> Optional[str]:
    """Copy the game's save files into the stash `name` (replacing it). None if there was nothing to copy."""
    files = _files(game_folder)
    if not files:
        return None
    target = os.path.join(stash_root(), safe_name(name))
    temporary = target + ".tmp"
    shutil.rmtree(temporary, ignore_errors=True)
    os.makedirs(temporary)
    for name_ in files:
        shutil.copy2(os.path.join(game_folder, name_), os.path.join(temporary, name_))
    shutil.rmtree(target, ignore_errors=True)
    os.replace(temporary, target)
    return target


def clear(game_folder: str) -> None:
    """Remove the game's save files (only call after stash())."""
    for name in _files(game_folder):
        os.remove(os.path.join(game_folder, name))


def install(game_folder: str, name: str) -> bool:
    """Replace the game's save files with the stash `name`."""
    source = os.path.join(stash_root(), safe_name(name))
    if not os.path.isdir(source):
        return False
    os.makedirs(game_folder, exist_ok=True)
    clear(game_folder)
    for name_ in _files(source):
        shutil.copy2(os.path.join(source, name_), os.path.join(game_folder, name_))
    return True


def backup_name(owner: str) -> str:
    """Stash name for the save currently in the game: its owner, or a dated name if unknown."""
    return safe_name(owner) if owner else f"unknown_{time.strftime('%Y%m%d_%H%M%S')}"
