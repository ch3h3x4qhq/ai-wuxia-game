from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from ..schemas import EnemyTemplate, EventDefinition


@dataclass
class WorldContent:
    martial_arts: Dict[str, Dict[str, object]]
    enemies: Dict[str, EnemyTemplate]
    events: Dict[str, EventDefinition]
    rooms: List[List[str]]


def _load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_content(content_dir: Path) -> WorldContent:
    martial = _load_json(content_dir / "martial_arts.json")
    events_raw = _load_json(content_dir / "events.json")
    rooms_raw = _load_json(content_dir / "rooms.json")

    arts = {entry["code"]: entry for entry in martial.get("arts", [])}
    enemies = {
        entry["code"]: EnemyTemplate(**entry)
        for entry in martial.get("enemies", [])
    }
    events = {entry["code"]: EventDefinition(**entry) for entry in events_raw}

    rooms: List[List[str]] = []
    for template in rooms_raw:
        layout = template.get("layout")
        if isinstance(layout, list):
            rooms.append(layout)

    return WorldContent(martial_arts=arts, enemies=enemies, events=events, rooms=rooms)


def get_enemy_template(content: WorldContent, code: str) -> EnemyTemplate:
    if code not in content.enemies:
        raise KeyError(f"Unknown enemy code: {code}")
    return content.enemies[code]


def get_event(content: WorldContent, code: str) -> EventDefinition:
    if code not in content.events:
        raise KeyError(f"Unknown event code: {code}")
    return content.events[code]
