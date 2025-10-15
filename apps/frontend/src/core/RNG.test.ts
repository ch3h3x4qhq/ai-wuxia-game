import { describe, expect, it } from 'vitest';

import { Mulberry32 } from './RNG';

describe('Mulberry32', () => {
  it('produces deterministic sequence', () => {
    const a = new Mulberry32(42);
    const b = new Mulberry32(42);
    const sequenceA = [a.randInt(0, 10), a.randInt(0, 10), a.randInt(0, 10)];
    const sequenceB = [b.randInt(0, 10), b.randInt(0, 10), b.randInt(0, 10)];
    expect(sequenceA).toEqual(sequenceB);
  });
});
