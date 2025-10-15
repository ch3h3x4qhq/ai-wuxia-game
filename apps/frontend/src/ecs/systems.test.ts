import { describe, expect, it } from 'vitest';

import { sortTurnOrder } from './systems';
import { CombatActor } from '../types';

const stubActor = (code: string, agility: number): CombatActor => ({
  code,
  name: code,
  stats: { force: 1, agility, inner: 1, mind: 1 },
  hp: 1,
  mp: 0,
  max_hp: 1,
  max_mp: 0,
  statuses: [],
  is_player: code === 'player'
});

describe('systems', () => {
  it('sorts actors by agility desc', () => {
    const order = sortTurnOrder([
      stubActor('enemy', 2),
      stubActor('player', 5),
      stubActor('ambusher', 3)
    ]);
    expect(order[0]).toBe('player');
    expect(order).toEqual(['player', 'ambusher', 'enemy']);
  });
});
