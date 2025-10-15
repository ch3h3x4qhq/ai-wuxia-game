export interface PositionComponent {
  x: number;
  y: number;
}

export interface StatsComponent {
  force: number;
  agility: number;
  inner: number;
  mind: number;
  hp: number;
  maxHp: number;
}

export type ActorTag = 'player' | 'enemy' | 'npc';

export type AIState = 'idle' | 'patrol' | 'hostile';

export interface StatusComponent {
  status: 'normal' | 'slow' | 'bleed';
  duration: number;
}
