import Phaser from 'phaser';

import RoomScene from './RoomScene';
import { COLORS } from '../core/Constants';
import { RunState } from '../types';
import { LogBuffer } from '../ui/LogBuffer';
import { drawBar } from '../ui/UIHelpers';

interface UISceneData {
  runId: string;
}

export default class UIScene extends Phaser.Scene {
  static KEY = 'UIScene';
  private logText?: Phaser.GameObjects.Text;
  private hpBar?: Phaser.GameObjects.Graphics;
  private mpBar?: Phaser.GameObjects.Graphics;
  private statsText?: Phaser.GameObjects.Text;
  private logBuffer = new LogBuffer(8);

  constructor() {
    super({ key: UIScene.KEY });
  }

  create(): void {
    const { width } = this.scale;
    this.add.rectangle(width - 220, 270, 200, 520, COLORS.uiBg, 0.9).setOrigin(0.5);
    this.statsText = this.add
      .text(width - 320, 40, '侠客状态', { color: COLORS.text, fontSize: '16px' })
      .setOrigin(0, 0);
    this.logText = this.add
      .text(width - 320, 160, '', { color: COLORS.text, fontSize: '14px', wordWrap: { width: 200 } })
      .setOrigin(0, 0);
    this.add
      .text(width - 320, 420, '操作提示:\n方向选择节点\nEnter 进入\nF 攻击  R 调息\n1-3 施展武学\nQ 原地等待\nS 存档', {
        color: '#94a3b8',
        fontSize: '12px'
      })
      .setOrigin(0, 0);

    const room = this.scene.get(RoomScene.KEY);
    room.events.on('run-update', (run: RunState) => this.updateRun(run));
    room.events.on('log', (entries: string[]) => this.appendLog(entries));
  }

  private updateRun(run: RunState): void {
    const { player } = run;
    this.statsText?.setText(
      `侠客：${player.name}\n气血：${player.hp}/${player.max_hp}\n真气：${player.mp}/${player.max_mp}\n武学：${player.arts.join('、') || '无'}\n节点：${run.node_map.nodes[run.node_index]?.tag ?? ''}`
    );
    this.hpBar?.destroy();
    this.mpBar?.destroy();
    this.hpBar = drawBar(this, this.scale.width - 320, 110, 180, 18, player.hp / player.max_hp, COLORS.hp);
    this.mpBar = drawBar(this, this.scale.width - 320, 132, 180, 18, player.mp / Math.max(1, player.max_mp), COLORS.mp);
  }

  private appendLog(entries: string[]): void {
    this.logBuffer.push(entries);
    this.logText?.setText(this.logBuffer.snapshot());
  }
}
