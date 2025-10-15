from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class Stats(BaseModel):
    force: int = 1
    agility: int = 1
    inner: int = 1
    mind: int = 1


class StatusEffect(BaseModel):
    type: Literal["slow", "bleed"]
    duration: int = 1
    potency: int | None = None
    data: Dict[str, Any] = Field(default_factory=dict)


class PlayerState(BaseModel):
    name: str = "无名侠客"
    stats: Stats = Field(default_factory=Stats)
    hp: int = 20
    mp: int = 5
    max_hp: int = 20
    max_mp: int = 5
    arts: List[str] = Field(default_factory=list)
    location_tag: str = "start"


class EnemyTemplate(BaseModel):
    code: str
    name: str
    stats: Stats
    max_hp: int
    max_mp: int
    arts: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    description: str = ""
    rewards: List[str] = Field(default_factory=list)


class CombatActor(BaseModel):
    code: str
    name: str
    stats: Stats
    hp: int
    mp: int
    max_hp: int
    max_mp: int
    statuses: List[StatusEffect] = Field(default_factory=list)
    is_player: bool = False
    last_move: Optional[str] = None
    repeat_count: int = 0
    slow_toggle: bool = False


class CombatState(BaseModel):
    player: CombatActor
    enemies: List[CombatActor]
    turn_order: List[str]
    current_index: int = 0
    log: List[str] = Field(default_factory=list)
    finished: bool = False
    rewards: Optional[List[str]] = None


class DungeonNode(BaseModel):
    index: int
    tag: str
    connections: List[int]


class DungeonMap(BaseModel):
    nodes: List[DungeonNode]

    def tag_for_index(self, index: int) -> str:
        for node in self.nodes:
            if node.index == index:
                return node.tag
        return "road"


class RunState(BaseModel):
    run_id: str
    seed: int
    rng_state: int
    node_index: int
    player: PlayerState
    backpack: List[str] = Field(default_factory=list)
    flags: Dict[str, Any] = Field(default_factory=dict)
    timestamp: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
    node_map: DungeonMap
    combat: Optional[CombatState] = None
    log: List[str] = Field(default_factory=list)
    pending_event: Optional[str] = None


class RunCreateRequest(BaseModel):
    seed: Optional[int] = None
    name: Optional[str] = None


class RunSaveResponse(BaseModel):
    ok: bool


class EventChoice(BaseModel):
    text: str
    effects: Dict[str, Any] = Field(default_factory=dict)


class EventDefinition(BaseModel):
    code: str
    name: str
    description: str
    tags: List[str]
    weight: int = 1
    choices: List[EventChoice]


class EventPayload(BaseModel):
    event: EventDefinition
    choices: List[EventChoice]


class EventNextRequest(BaseModel):
    run_id: str


class EventChooseRequest(BaseModel):
    run_id: str
    event_code: str
    choice_index: int


class CombatStartRequest(BaseModel):
    run_id: str
    enemy_code: str


class CombatTurnAction(BaseModel):
    type: Literal["move", "attack", "skill", "meditate", "wait"]
    dir: Optional[str] = None
    skill_id: Optional[str] = None


class CombatTurnRequest(BaseModel):
    run_id: str
    action: CombatTurnAction


class CombatTurnResponse(BaseModel):
    combat: CombatState
    log: List[str]
