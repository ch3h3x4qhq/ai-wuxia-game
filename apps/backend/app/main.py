from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .deps import get_state
from .routers import combat, events, health, runs


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Wuxia Rogue-lite API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/api")
    app.include_router(runs.router, prefix="/api")
    app.include_router(events.router, prefix="/api")
    app.include_router(combat.router, prefix="/api")

    @app.on_event("startup")
    def _startup() -> None:
        # Touch the global state to ensure content is loaded.
        get_state()

    return app


app = create_app()
