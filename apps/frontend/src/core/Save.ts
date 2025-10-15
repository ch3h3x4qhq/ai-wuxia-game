import { RunState } from '../types';

const STORAGE_KEY = 'wuxia-last-run';

export function saveSnapshot(run: RunState | null): void {
  if (!run) {
    window.localStorage.removeItem(STORAGE_KEY);
    return;
  }
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(run));
}

export function loadSnapshot(): RunState | null {
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw) as RunState;
  } catch (error) {
    console.warn('Failed to parse local snapshot', error);
    return null;
  }
}
