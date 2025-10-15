from __future__ import annotations

import math
from typing import List, Optional

from ..schemas import (
    CombatActor,
    CombatState,
    CombatTurnAction,
    PlayerState,
    RunState,
    StatusEffect,
    Stats,
)
from . import rng as rng_service
from .world import WorldContent, get_enemy_template


def _player_actor(player: PlayerState) -> CombatActor:
    return CombatActor(
        code="player",
        name=player.name,
        stats=player.stats,
        hp=player.hp,
        mp=player.mp,
        max_hp=player.max_hp,
        max_mp=player.max_mp,
        is_player=True,
    )


def calculate_damage(stats: Stats, rng: rng_service.Mulberry32, repeat_stacks: int) -> int:
    jitter = rng.rand_int(-2, 2)
    base = math.floor(stats.force * 2 + stats.inner * 0.5 + jitter)
    base = max(1, base)
    penalty = min(0.4, max(0, repeat_stacks) * 0.1)
    adjusted = max(1, math.floor(base * (1 - penalty)))
    return adjusted


def start_combat(run: RunState, content: WorldContent, enemy_code: str) -> CombatState:
    template = get_enemy_template(content, enemy_code)
    player_actor = _player_actor(run.player)
    enemy_actor = CombatActor(
        code=f"{template.code}-0",
        name=template.name,
        stats=template.stats,
        hp=template.max_hp,
        mp=template.max_mp,
        max_hp=template.max_hp,
        max_mp=template.max_mp,
    )
    turn_order = _build_turn_order(player_actor, [enemy_actor])
    combat = CombatState(
        player=player_actor,
        enemies=[enemy_actor],
        turn_order=turn_order,
        current_index=0,
        log=["遭遇战斗：" + template.name],
    )
    run.combat = combat
    return combat


def _build_turn_order(player: CombatActor, enemies: List[CombatActor]) -> List[str]:
    entries = [(player.stats.agility, "player")]
    for enemy in enemies:
        entries.append((enemy.stats.agility, enemy.code))
    entries.sort(key=lambda item: (-item[0], item[1]))
    return [code for _, code in entries]


def _get_actor(combat: CombatState, actor_id: str) -> Optional[CombatActor]:
    if actor_id == "player":
        return combat.player
    for enemy in combat.enemies:
        if enemy.code == actor_id:
            return enemy
    return None


def _alive_enemies(combat: CombatState) -> List[CombatActor]:
    return [enemy for enemy in combat.enemies if enemy.hp > 0]


def _apply_statuses(run: RunState, actor: CombatActor, log: List[str]) -> bool:
    skip = False
    rng = rng_service.advance(run)
    updated: List[StatusEffect] = []
    for status in actor.statuses:
        status.duration -= 1
        if status.type == "bleed" and actor.hp > 0:
            dmg = status.potency or rng.rand_int(1, 2)
            actor.hp = max(0, actor.hp - dmg)
            log.append(f"{actor.name} 因流血失去 {dmg} 点气血。")
        if status.type == "slow":
            toggled = not bool(status.data.get("toggle", False))
            status.data["toggle"] = toggled
            if toggled:
                skip = True
        if status.duration > 0:
            updated.append(status)
    actor.statuses = updated
    rng_service.commit(run, rng)
    if skip:
        log.append(f"{actor.name} 身形迟缓，错失良机。")
    if actor.hp <= 0:
        log.append(f"{actor.name} 倒下了。")
    return skip


def _record_move(actor: CombatActor, move_id: str) -> int:
    if actor.last_move == move_id:
        actor.repeat_count += 1
    else:
        actor.last_move = move_id
        actor.repeat_count = 1
    return max(0, actor.repeat_count - 2)


def _deal_damage(
    run: RunState,
    attacker: CombatActor,
    defender: CombatActor,
    move_id: str,
    log: List[str],
) -> None:
    rng = rng_service.advance(run)
    repeat_stacks = _record_move(attacker, move_id)
    damage = calculate_damage(attacker.stats, rng, repeat_stacks)
    rng_service.commit(run, rng)
    defender.hp = max(0, defender.hp - damage)
    log.append(f"{attacker.name} 对 {defender.name} 造成 {damage} 点伤害。")
    if defender.hp <= 0:
        log.append(f"{defender.name} 被击败。")


def _advance_turn(combat: CombatState) -> None:
    if not combat.turn_order:
        return
    total = len(combat.turn_order)
    for _ in range(total):
        combat.current_index = (combat.current_index + 1) % total
        actor = _get_actor(combat, combat.turn_order[combat.current_index])
        if actor and actor.hp > 0:
            return
    combat.current_index = 0


def _check_outcome(run: RunState, combat: CombatState) -> None:
    if combat.player.hp <= 0:
        combat.finished = True
        combat.log.append("你败下阵来。")
        run.player.hp = 0
        return
    if not _alive_enemies(combat):
        combat.finished = True
        combat.rewards = ["内功心得"]
        combat.log.append("战斗胜利，获得内功心得。")
        run.player.hp = min(run.player.max_hp, combat.player.hp)
        run.player.mp = min(run.player.max_mp, combat.player.mp)


def player_turn(run: RunState, action: CombatTurnAction) -> CombatState:
    combat = run.combat
    if not combat:
        raise ValueError("No active combat")
    current_id = combat.turn_order[combat.current_index]
    if current_id != "player":
        raise ValueError("Not player turn")
    actor = combat.player
    log: List[str] = []
    skip = _apply_statuses(run, actor, log)
    if actor.hp <= 0:
        combat.log.extend(log)
        _check_outcome(run, combat)
        return combat
    if not skip:
        if action.type in ("attack", "skill"):
            target = next((enemy for enemy in combat.enemies if enemy.hp > 0), None)
            if not target:
                combat.finished = True
                combat.log.extend(log)
                _check_outcome(run, combat)
                return combat
            move_id = "basic" if action.type == "attack" else action.skill_id or "skill"
            if action.type == "skill":
                if actor.mp <= 0:
                    log.append("真气不足，施展失败。")
                else:
                    actor.mp -= 1
                    log.append("施展武学。")
            _deal_damage(run, actor, target, move_id, log)
        elif action.type == "meditate":
            heal = 1
            actor.hp = min(actor.max_hp, actor.hp + heal)
            actor.mp = min(actor.max_mp, actor.mp + 2)
            log.append("调息片刻，恢复气血与真气。")
        elif action.type == "wait":
            log.append("凝神观敌。")
    combat.log.extend(log)
    _check_outcome(run, combat)
    if combat.finished:
        run.combat = combat
        run.player.hp = combat.player.hp
        run.player.mp = combat.player.mp
        return combat
    _advance_turn(combat)
    _enemy_turns(run, combat)
    run.player.hp = combat.player.hp
    run.player.mp = combat.player.mp
    _check_outcome(run, combat)
    if combat.finished:
        run.combat = combat
    return combat


def _enemy_turns(run: RunState, combat: CombatState) -> None:
    for _ in range(len(combat.turn_order)):
        current_id = combat.turn_order[combat.current_index]
        if current_id == "player":
            return
        enemy = _get_actor(combat, current_id)
        if not enemy or enemy.hp <= 0:
            _advance_turn(combat)
            continue
        log: List[str] = []
        skip = _apply_statuses(run, enemy, log)
        if enemy.hp > 0 and not skip:
            _deal_damage(run, enemy, combat.player, "enemy_attack", log)
        combat.log.extend(log)
        if combat.player.hp <= 0:
            return
        _advance_turn(combat)


def ensure_combat(run: RunState, content: WorldContent, enemy_code: str) -> CombatState:
    if run.combat and not run.combat.finished:
        return run.combat
    return start_combat(run, content, enemy_code)
