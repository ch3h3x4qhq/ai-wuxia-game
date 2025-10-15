import { CombatActor } from '../types';

export function sortTurnOrder(actors: CombatActor[]): string[] {
  return [...actors]
    .sort((a, b) => {
      if (a.stats.agility === b.stats.agility) {
        return a.code.localeCompare(b.code);
      }
      return b.stats.agility - a.stats.agility;
    })
    .map((actor) => actor.code);
}

export function applyBleed(actor: CombatActor): number {
  const bleed = actor.statuses.find((status) => status.type === 'bleed');
  if (!bleed) {
    return 0;
  }
  const damage = bleed.potency ?? 1;
  actor.hp = Math.max(0, actor.hp - damage);
  bleed.duration -= 1;
  if (bleed.duration <= 0) {
    actor.statuses = actor.statuses.filter((status) => status !== bleed);
  }
  return damage;
}
