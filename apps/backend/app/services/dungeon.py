from __future__ import annotations

from typing import List

from ..schemas import DungeonMap, DungeonNode
from .rng import Mulberry32

NODE_TAGS = ["road", "ruin", "town"]


def generate_dungeon(seed: int) -> DungeonMap:
    rng = Mulberry32(seed)
    node_total = max(4, rng.rand_int(4, 6))

    nodes: List[DungeonNode] = [DungeonNode(index=0, tag="start", connections=[1])]
    for idx in range(1, node_total - 1):
        tag = NODE_TAGS[rng.rand_int(0, len(NODE_TAGS) - 1)]
        connections = [idx - 1, idx + 1]
        if idx > 1 and idx < node_total - 2:
            branch_target = rng.rand_int(0, idx - 1)
            if branch_target not in connections:
                connections.append(branch_target)
        nodes.append(DungeonNode(index=idx, tag=tag, connections=sorted(set(connections))))
    nodes.append(
        DungeonNode(
            index=node_total - 1,
            tag="boss",
            connections=[node_total - 2],
        )
    )
    nodes[0].connections = [1]
    return DungeonMap(nodes=nodes)
