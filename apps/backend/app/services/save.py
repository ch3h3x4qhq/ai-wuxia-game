from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import portalocker

from ..config import Settings
from ..schemas import RunState


def _path(settings: Settings, run_id: str) -> Path:
    return settings.storage_dir / f"{run_id}.json"


def save_run(settings: Settings, run: RunState) -> None:
    path = _path(settings, run.run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = run.model_dump()
    with portalocker.Lock(str(path), "w", timeout=2) as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def load_run(settings: Settings, run_id: str) -> Optional[RunState]:
    path = _path(settings, run_id)
    if not path.exists():
        return None
    with portalocker.Lock(str(path), "r", timeout=2) as handle:
        payload = json.load(handle)
    return RunState.model_validate(payload)
