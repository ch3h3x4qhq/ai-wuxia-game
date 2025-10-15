export interface Stats {
  force: number;
  agility: number;
  inner: number;
  mind: number;
}

export type StatusType = 'slow' | 'bleed';

export interface StatusEffect {
  type: StatusType;
  duration: number;
  potency?: number;
  data?: Record<string, unknown>;
}

export interface PlayerState {
  name: string;
  stats: Stats;
  hp: number;
  mp: number;
  max_hp: number;
  max_mp: number;
  arts: string[];
  location_tag: string;
}

export interface CombatActor {
  code: string;
  name: string;
  stats: Stats;
  hp: number;
  mp: number;
  max_hp: number;
  max_mp: number;
  statuses: StatusEffect[];
  is_player: boolean;
  last_move?: string | null;
  repeat_count?: number;
  slow_toggle?: boolean;
}

export interface CombatState {
  player: CombatActor;
  enemies: CombatActor[];
  turn_order: string[];
  current_index: number;
  log: string[];
  finished: boolean;
  rewards?: string[] | null;
}

export interface DungeonNode {
  index: number;
  tag: string;
  connections: number[];
}

export interface DungeonMap {
  nodes: DungeonNode[];
}

export interface RunState {
  run_id: string;
  seed: number;
  rng_state: number;
  node_index: number;
  player: PlayerState;
  backpack: string[];
  flags: Record<string, unknown>;
  timestamp: number;
  node_map: DungeonMap;
  combat?: CombatState | null;
  log: string[];
  pending_event?: string | null;
}

export interface EventChoice {
  text: string;
  effects: Record<string, unknown>;
}

export interface EventDefinition {
  code: string;
  name: string;
  description: string;
  tags: string[];
  weight: number;
  choices: EventChoice[];
}

export interface EventPayload {
  event: EventDefinition;
  choices: EventChoice[];
}

export interface CombatAction {
  type: 'move' | 'attack' | 'skill' | 'meditate' | 'wait';
  dir?: string;
  skill_id?: string;
}
