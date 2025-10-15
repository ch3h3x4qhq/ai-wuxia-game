from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from .. import deps
from ..schemas import EventChooseRequest, EventNextRequest, EventPayload
from ..services import combat
from ..services import encounters

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/next", response_model=EventPayload)
def next_event(payload: EventNextRequest, state=Depends(deps.get_state)) -> EventPayload:
    run = state.runs.get(payload.run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return encounters.next_event(run, state.content)


@router.post("/choose")
def choose_event(payload: EventChooseRequest, state=Depends(deps.get_state)) -> dict[str, object]:
    run = state.runs.get(payload.run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    outcome = encounters.apply_choice(run, state.content, payload.event_code, payload.choice_index)
    enemy_code = outcome.get("start_combat")
    if enemy_code:
        combat_state = combat.ensure_combat(run, state.content, enemy_code)
        outcome["combat"] = combat_state
    return outcome
