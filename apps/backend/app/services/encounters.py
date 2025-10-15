from __future__ import annotations

from typing import Dict, List, Optional

from ..schemas import EventDefinition, EventPayload, RunState
from . import rng as rng_service
from .world import WorldContent, get_event


def _eligible_events(content: WorldContent, node_tag: str) -> List[EventDefinition]:
    matches = [event for event in content.events.values() if node_tag in event.tags]
    if matches:
        return matches
    return list(content.events.values())


def next_event(run: RunState, content: WorldContent) -> EventPayload:
    node_tag = run.node_map.tag_for_index(run.node_index)
    events = _eligible_events(content, node_tag)
    weighted = [(event.weight, event.code) for event in events]
    selected_code = rng_service.choose_weighted(run, weighted)
    event = get_event(content, selected_code)
    run.pending_event = event.code
    return EventPayload(event=event, choices=event.choices)


def apply_choice(
    run: RunState, content: WorldContent, event_code: str, choice_index: int
) -> Dict[str, object]:
    if event_code not in content.events:
        raise ValueError("Unknown event code")
    event = content.events[event_code]
    if choice_index < 0 or choice_index >= len(event.choices):
        raise ValueError("Choice out of range")
    choice = event.choices[choice_index]
    run.pending_event = None

    log: List[str] = [f"你选择了：{choice.text}"]
    combat_enemy: Optional[str] = None

    effects = choice.effects
    hp_delta = int(effects.get("hp", 0))
    if hp_delta:
        run.player.hp = max(0, min(run.player.max_hp, run.player.hp + hp_delta))
        log.append(f"气血变化 {hp_delta:+d}")
    mp_delta = int(effects.get("mp", 0))
    if mp_delta:
        run.player.mp = max(0, min(run.player.max_mp, run.player.mp + mp_delta))
        log.append(f"真气变化 {mp_delta:+d}")

    flag = effects.get("flag")
    if isinstance(flag, dict):
        run.flags.update(flag)
        log.append("触发奇遇标记。")

    art = effects.get("gain_art")
    if isinstance(art, str) and art not in run.player.arts:
        run.player.arts.append(art)
        log.append(f"习得武学《{art}》。")

    loot = effects.get("loot")
    if isinstance(loot, str):
        run.backpack.append(loot)
        log.append(f"获得物品：{loot}")

    combat_enemy = effects.get("start_combat")
    if combat_enemy:
        log.append("敌人现身！")

    run.log.extend(log)
    run.player.location_tag = run.node_map.tag_for_index(run.node_index)
    return {"log": log, "start_combat": combat_enemy, "event": event, "choice": choice}
