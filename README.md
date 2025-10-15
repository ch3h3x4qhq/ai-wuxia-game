# Wuxia Rogue-lite Demo

A local-only prototype showcasing a deterministic wuxia-inspired rogue-lite. The monorepo contains a Phaser 3 + TypeScript + Vite frontend and a FastAPI backend. Both sides communicate over JSON REST running on `http://localhost:8000`.

## Features

- Deterministic seeded runs with reproducible dungeon graphs and encounters.
- Authoritative backend handling world generation, events, and combat.
- Lightweight ECS-driven Phaser client rendering rooms with primitive graphics.
- JSON-driven content for martial arts, events, and rooms for quick authoring.
- Simple file-based save system under `apps/backend/storage/`.

## Getting Started

### 1. Backend

```bash
cd apps/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Frontend

```bash
cd apps/frontend
npm install
npm run dev
```

Vite serves the client at `http://localhost:5173`. Visit the URL in a browser once both services are running. The frontend expects the backend to be available at `http://localhost:8000`.

### `make` Shortcuts

From the repository root:

```bash
make dev   # run frontend + backend in watch mode
make be    # backend only
make fe    # frontend only
make test  # run backend pytest and frontend vitest
make fmt   # format both projects
```

## Data Authoring

Game content lives under `apps/backend/app/content/` as JSON files.

- `events.json`: describes adventure events with weighted choices.
- `martial_arts.json`: defines arts available to the player and enemies.
- `rooms.json`: ASCII templates for roguelite rooms; `#` walls, `.` floors, `@` spawn, `e` enemy, `D` door.

To add content, follow the existing schema in each file. After editing, restart the backend to reload data. Frontend TypeScript types mirror these schemas in `src/types.ts`.

## Determinism Notes

- Each run uses a Mulberry32 RNG seeded when the run is created. The backend persists the seed alongside the run snapshot.
- Dungeon generation, event selection, and combat rolls reference the deterministic RNG ensuring reproducible sessions.
- The frontend mirrors the deterministic utilities for prediction but always defers to backend responses as the source of truth.

## Roadmap

- 🎴 Add sprite-based animations and VFX.
- 🔊 Integrate local sound design hooks.
- 🏯 Introduce faction reputation systems influencing events.
- ✍️ Add AI-assisted copy polishing endpoint (placeholder for future expansion).

## License

MIT License. See [LICENSE](LICENSE).
