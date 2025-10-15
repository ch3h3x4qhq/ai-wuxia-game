import Phaser from 'phaser';

import { chooseEvent, fetchNextEvent, fetchRun, saveRun, takeCombatTurn } from '../core/Api';
import { CombatAction, CombatState, EventPayload, RunState } from '../types';

interface RoomSceneData {
  runId: string;
  nodeIndex: number;
}

export default class RoomScene extends Phaser.Scene {
  static KEY = 'RoomScene';
  private runId!: string;
  private run?: RunState;
  private currentEvent?: EventPayload;
  private info?: Phaser.GameObjects.Text;
  private combat?: CombatState;

  constructor() {
    super({ key: RoomScene.KEY });
  }

  init(data: RoomSceneData): void {
    this.runId = data.runId;
  }

  create(): void {
    const { width, height } = this.scale;
    this.add.rectangle(width / 2, height / 2, width - 40, height - 40, 0x111827, 0.9);
    this.info = this.add
      .text(40, 60, '探索中...', {
        fontSize: '18px',
        color: '#f8fafc',
        wordWrap: { width: width - 80 }
      })
      .setOrigin(0, 0);

    this.registerControls();
    void this.refreshState();
  }

  private registerControls(): void {
    this.input.keyboard?.on('keydown-ONE', () => this.handleNumberKey(0));
    this.input.keyboard?.on('keydown-TWO', () => this.handleNumberKey(1));
    this.input.keyboard?.on('keydown-THREE', () => this.handleNumberKey(2));
    this.input.keyboard?.on('keydown-F', () => this.performAction({ type: 'attack' }));
    this.input.keyboard?.on('keydown-R', () => this.performAction({ type: 'meditate' }));
    this.input.keyboard?.on('keydown-Q', () => this.performAction({ type: 'wait' }));
    this.input.keyboard?.on('keydown-S', () => void this.save());
  }

  private handleNumberKey(index: number): void {
    if (this.combat && !this.combat.finished) {
      const skillId = (index + 1).toString();
      void this.performAction({ type: 'skill', skill_id: skillId });
    } else {
      void this.chooseOption(index);
    }
  }

  private async refreshState(): Promise<void> {
    try {
      this.run = await fetchRun(this.runId);
      this.registry.set('run', this.run);
      this.events.emit('run-update', this.run);
      await this.loadEvent();
    } catch (error) {
      this.showMessage(`同步失败: ${(error as Error).message}`);
    }
  }

  private async loadEvent(): Promise<void> {
    try {
      this.currentEvent = await fetchNextEvent(this.runId);
      const lines = [
        `【${this.currentEvent.event.name}】`,
        this.currentEvent.event.description,
        ...this.currentEvent.choices.map((choice, index) => `${index + 1}. ${choice.text}`)
      ];
      this.showMessage(lines.join('\n'));
      this.events.emit('log', [`遭遇 ${this.currentEvent.event.name}`]);
    } catch (error) {
      this.showMessage(`事件生成失败: ${(error as Error).message}`);
    }
  }

  private async chooseOption(index: number): Promise<void> {
    if (!this.currentEvent) return;
    if (index < 0 || index >= this.currentEvent.choices.length) {
      return;
    }
    try {
      const outcome = await chooseEvent(this.runId, this.currentEvent.event.code, index);
      const log = outcome.log as string[] | undefined;
      if (log) {
        this.events.emit('log', log);
      }
      if (outcome.combat) {
        this.combat = outcome.combat as CombatState;
        this.showMessage('战斗开始！按 F 攻击。');
      } else {
        await this.refreshState();
      }
    } catch (error) {
      this.showMessage(`抉择失败: ${(error as Error).message}`);
    }
  }

  private async performAction(action: CombatAction): Promise<void> {
    if (!this.combat || this.combat.finished) {
      return;
    }
    try {
      const response = await takeCombatTurn(this.runId, action);
      this.combat = response.combat;
      this.events.emit('log', response.log);
      this.showMessage(response.combat.log.slice(-5).join('\n'));
      if (this.combat.finished) {
        await this.refreshState();
      } else {
        this.run = await fetchRun(this.runId);
        this.registry.set('run', this.run);
        this.events.emit('run-update', this.run);
      }
    } catch (error) {
      this.showMessage(`战斗指令失败: ${(error as Error).message}`);
    }
  }

  private async save(): Promise<void> {
    try {
      const result = await saveRun(this.runId);
      if (result.ok) {
        this.events.emit('log', ['存档成功。']);
      }
    } catch (error) {
      this.events.emit('log', [`存档失败: ${(error as Error).message}`]);
    }
  }

  private showMessage(message: string): void {
    this.info?.setText(message);
  }
}
