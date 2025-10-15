from __future__ import annotations

import secrets
import time
import uuid

from fastapi import APIRouter, Depends, HTTPException

from .. import deps
from ..schemas import (
    RunCreateRequest,
    RunSaveResponse,
    RunState,
    PlayerState,
    Stats,
)
from ..services import dungeon
from ..services.save import load_run as load_run_file, save_run as save_run_file

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post("/new", response_model=RunState)
def create_run(
    payload: RunCreateRequest,
    state=Depends(deps.get_state),
) -> RunState:
    seed = payload.seed if payload.seed is not None else secrets.randbits(32)
    run_id = uuid.uuid4().hex[:8]
    node_map = dungeon.generate_dungeon(seed)
    name = payload.name or "云游剑客"
    base_stats = Stats(force=4, agility=3, inner=3, mind=2)
    player = PlayerState(
        name=name,
        stats=base_stats,
        hp=24,
        mp=6,
        max_hp=24,
        max_mp=6,
        arts=["dragon_elephant"],
        location_tag=node_map.tag_for_index(0),
    )
    run = RunState(
        run_id=run_id,
        seed=seed,
        rng_state=seed,
        node_index=0,
        player=player,
        node_map=node_map,
        backpack=[],
        flags={},
        timestamp=int(time.time()),
    )
    state.runs[run_id] = run
    return run


@router.get("/{run_id}", response_model=RunState)
def get_run(run_id: str, state=Depends(deps.get_state)) -> RunState:
    run = state.runs.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("/{run_id}/save", response_model=RunSaveResponse)
def save_run(run_id: str, state=Depends(deps.get_state)) -> RunSaveResponse:
    run = state.runs.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    save_run_file(state.settings, run)
    return RunSaveResponse(ok=True)


@router.post("/{run_id}/load", response_model=RunState)
def load_run(run_id: str, state=Depends(deps.get_state)) -> RunState:
    loaded = load_run_file(state.settings, run_id)
    if not loaded:
        raise HTTPException(status_code=404, detail="Save not found")
    state.runs[run_id] = loaded
    return loaded
