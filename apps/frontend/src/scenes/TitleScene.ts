import Phaser from 'phaser';

import { createRun } from '../core/Api';
import MapScene from './MapScene';
import UIScene from './UIScene';
import { RunState } from '../types';

export default class TitleScene extends Phaser.Scene {
  static KEY = 'TitleScene';
  private info?: Phaser.GameObjects.Text;

  constructor() {
    super({ key: TitleScene.KEY });
  }

  create(): void {
    const { width, height } = this.scale;
    this.add
      .text(width / 2, height / 2 - 40, '江湖试炼', {
        fontFamily: 'serif',
        fontSize: '48px',
        color: '#facc15'
      })
      .setOrigin(0.5);

    this.info = this.add
      .text(width / 2, height / 2 + 20, '按 Enter 开启试炼', {
        fontFamily: 'sans-serif',
        fontSize: '20px',
        color: '#f8fafc'
      })
      .setOrigin(0.5);

    this.input.keyboard?.once('keydown-ENTER', () => {
      void this.startRun();
    });
  }

  private async startRun(): Promise<void> {
    if (!this.info) return;
    this.info.setText('生成江湖中...');
    try {
      const run = await createRun();
      this.registry.set('run', run as RunState);
      this.scene.start(MapScene.KEY, { runId: run.run_id });
      this.scene.launch(UIScene.KEY, { runId: run.run_id });
    } catch (error) {
      this.info.setText(`启动失败: ${(error as Error).message}`);
      this.input.keyboard?.once('keydown-ENTER', () => {
        void this.startRun();
      });
    }
  }
}
