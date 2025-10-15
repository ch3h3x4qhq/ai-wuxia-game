from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from .. import deps
from ..schemas import CombatStartRequest, CombatTurnRequest, CombatTurnResponse
from ..services import combat as combat_service

router = APIRouter(prefix="/combat", tags=["combat"])


@router.post("/start")
def start_combat(payload: CombatStartRequest, state=Depends(deps.get_state)) -> dict[str, object]:
    run = state.runs.get(payload.run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    combat_state = combat_service.start_combat(run, state.content, payload.enemy_code)
    return {"combat": combat_state}


@router.post("/turn", response_model=CombatTurnResponse)
def take_turn(payload: CombatTurnRequest, state=Depends(deps.get_state)) -> CombatTurnResponse:
    run = state.runs.get(payload.run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    combat_state = combat_service.player_turn(run, payload.action)
    return CombatTurnResponse(combat=combat_state, log=combat_state.log[-5:])
