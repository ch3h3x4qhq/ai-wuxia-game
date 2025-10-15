from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .config import Settings, get_settings
from .schemas import RunState
from .services.world import WorldContent, load_content


@dataclass
class AppState:
    """In-memory container for shared services."""

    settings: Settings
    content: WorldContent
    runs: Dict[str, RunState]


def build_state() -> AppState:
    settings = get_settings()
    content = load_content(settings.content_dir)
    return AppState(settings=settings, content=content, runs={})


STATE = build_state()


def get_state() -> AppState:
    return STATE
