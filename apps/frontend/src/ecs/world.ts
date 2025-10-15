import { CombatActor } from '../types';

export class World {
  private actors: Map<string, CombatActor> = new Map();

  addActor(actor: CombatActor): void {
    this.actors.set(actor.code, actor);
  }

  removeActor(code: string): void {
    this.actors.delete(code);
  }

  getActor(code: string): CombatActor | undefined {
    return this.actors.get(code);
  }

  listActors(): CombatActor[] {
    return Array.from(this.actors.values());
  }

  clear(): void {
    this.actors.clear();
  }
}
