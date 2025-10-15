from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def get_health() -> dict[str, object]:
    return {"status": "ok", "ts": int(datetime.utcnow().timestamp())}
