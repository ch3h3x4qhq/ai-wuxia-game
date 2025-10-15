import { API_BASE } from './Constants';
import {
  CombatAction,
  CombatState,
  EventPayload,
  RunState
} from '../types';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(`请求失败: ${response.status} ${message}`);
  }
  return (await response.json()) as T;
}

export function createRun(seed?: number, name?: string): Promise<RunState> {
  return request<RunState>('/runs/new', {
    method: 'POST',
    body: JSON.stringify({ seed, name })
  });
}

export function fetchRun(runId: string): Promise<RunState> {
  return request<RunState>(`/runs/${runId}`);
}

export function saveRun(runId: string): Promise<{ ok: boolean }> {
  return request<{ ok: boolean }>(`/runs/${runId}/save`, {
    method: 'POST'
  });
}

export function fetchNextEvent(runId: string): Promise<EventPayload> {
  return request<EventPayload>('/events/next', {
    method: 'POST',
    body: JSON.stringify({ run_id: runId })
  });
}

export function chooseEvent(
  runId: string,
  eventCode: string,
  choiceIndex: number
): Promise<Record<string, unknown>> {
  return request<Record<string, unknown>>('/events/choose', {
    method: 'POST',
    body: JSON.stringify({ run_id: runId, event_code: eventCode, choice_index: choiceIndex })
  });
}

export function startCombat(runId: string, enemyCode: string): Promise<{ combat: CombatState }> {
  return request<{ combat: CombatState }>('/combat/start', {
    method: 'POST',
    body: JSON.stringify({ run_id: runId, enemy_code: enemyCode })
  });
}

export function takeCombatTurn(
  runId: string,
  action: CombatAction
): Promise<{ combat: CombatState; log: string[] }> {
  return request<{ combat: CombatState; log: string[] }>('/combat/turn', {
    method: 'POST',
    body: JSON.stringify({ run_id: runId, action })
  });
}
