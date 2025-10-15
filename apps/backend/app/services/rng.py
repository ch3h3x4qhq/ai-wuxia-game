from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple, TypeVar

from ..schemas import RunState

T = TypeVar("T")


@dataclass
class Mulberry32:
    """Deterministic Mulberry32 RNG."""

    state: int

    def __post_init__(self) -> None:
        self.state &= 0xFFFFFFFF

    def random(self) -> float:
        self.state = (self.state + 0x6D2B79F5) & 0xFFFFFFFF
        t = self.state
        t = (t ^ (t >> 15)) * (t | 1)
        t &= 0xFFFFFFFF
        t ^= t + ((t ^ (t >> 7)) * (t | 61) & 0xFFFFFFFF)
        t &= 0xFFFFFFFF
        result = ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
        return result

    def rand_int(self, minimum: int, maximum: int) -> int:
        if minimum > maximum:
            minimum, maximum = maximum, minimum
        span = maximum - minimum + 1
        value = int(self.random() * span)
        if value >= span:
            value = span - 1
        return minimum + value


def from_seed(seed: int) -> Mulberry32:
    return Mulberry32(seed)


def advance(run: RunState) -> Mulberry32:
    rng = Mulberry32(run.rng_state)
    return rng


def commit(run: RunState, rng: Mulberry32) -> None:
    run.rng_state = rng.state & 0xFFFFFFFF


def rand_int(run: RunState, minimum: int, maximum: int) -> int:
    rng = advance(run)
    value = rng.rand_int(minimum, maximum)
    commit(run, rng)
    return value


def choose_weighted(run: RunState, items: Sequence[Tuple[int, T]]) -> T:
    total = sum(weight for weight, _ in items)
    if total <= 0:
        raise ValueError("No positive weights provided")
    rng = advance(run)
    roll = rng.rand_int(1, total)
    commit(run, rng)
    cumulative = 0
    for weight, value in items:
        cumulative += weight
        if roll <= cumulative:
            return value
    return items[-1][1]


def shuffle(run: RunState, values: Sequence[T]) -> list[T]:
    rng = advance(run)
    items = list(values)
    for i in range(len(items) - 1, 0, -1):
        j = rng.rand_int(0, i)
        items[i], items[j] = items[j], items[i]
    commit(run, rng)
    return items
