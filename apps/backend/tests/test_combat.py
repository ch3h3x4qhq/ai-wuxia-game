from app.schemas import CombatActor, DungeonMap, DungeonNode, PlayerState, RunState, Stats, StatusEffect
from app.services import combat
from app.services.rng import Mulberry32


def _stub_run() -> RunState:
    return RunState(
        run_id="test",
        seed=1,
        rng_state=1,
        node_index=0,
        player=PlayerState(),
        node_map=DungeonMap(nodes=[DungeonNode(index=0, tag="start", connections=[])]),
    )


def test_damage_has_floor() -> None:
    stats = Stats(force=0, agility=1, inner=0, mind=1)
    rng = Mulberry32(123)
    damage = combat.calculate_damage(stats, rng, 0)
    assert damage >= 1


def test_repeat_penalty_reduces_damage() -> None:
    stats = Stats(force=5, agility=3, inner=2, mind=2)
    rng_base = Mulberry32(555)
    base_damage = combat.calculate_damage(stats, rng_base, 0)
    rng_repeat = Mulberry32(555)
    repeat_damage = combat.calculate_damage(stats, rng_repeat, 3)
    assert repeat_damage < base_damage
    assert repeat_damage <= base_damage * 0.9


def test_slow_status_skips_every_other_turn() -> None:
    run = _stub_run()
    actor = CombatActor(
        code="player",
        name="test",
        stats=Stats(force=3, agility=3, inner=2, mind=2),
        hp=10,
        mp=5,
        max_hp=10,
        max_mp=5,
        is_player=True,
        statuses=[StatusEffect(type="slow", duration=2)],
    )
    log: list[str] = []
    skip_first = combat._apply_statuses(run, actor, log)
    skip_second = combat._apply_statuses(run, actor, log)
    assert skip_first is True
    assert skip_second is False
