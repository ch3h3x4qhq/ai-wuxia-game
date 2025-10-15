import { Mulberry32 } from '../core/RNG';
import { DungeonMap, DungeonNode } from '../types';

const NODE_TAGS = ['road', 'ruin', 'town'];

export function generateDungeon(seed: number): DungeonMap {
  const rng = new Mulberry32(seed);
  const nodeTotal = Math.max(4, rng.randInt(4, 6));
  const nodes: DungeonNode[] = [{ index: 0, tag: 'start', connections: [1] }];

  for (let index = 1; index < nodeTotal - 1; index += 1) {
    const tag = NODE_TAGS[rng.randInt(0, NODE_TAGS.length - 1)];
    const connections = new Set<number>([index - 1, index + 1]);
    if (index > 1 && index < nodeTotal - 2) {
      const branch = rng.randInt(0, index - 1);
      connections.add(branch);
    }
    nodes.push({ index, tag, connections: Array.from(connections).sort((a, b) => a - b) });
  }

  nodes.push({ index: nodeTotal - 1, tag: 'boss', connections: [nodeTotal - 2] });
  nodes[0].connections = [1];
  return { nodes };
}
