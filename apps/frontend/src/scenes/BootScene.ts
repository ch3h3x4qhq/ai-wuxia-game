import Phaser from 'phaser';

import PreloadScene from './PreloadScene';

export default class BootScene extends Phaser.Scene {
  constructor() {
    super({ key: 'BootScene' });
  }

  preload(): void {
    this.createSolid('tile-wall', 12, 12, 0x1f2937);
    this.createSolid('tile-floor', 12, 12, 0x334155);
    this.createSolid('tile-player', 12, 12, 0xfbbf24);
    this.createSolid('tile-enemy', 12, 12, 0xf97316);
  }

  create(): void {
    this.scene.start(PreloadScene.KEY);
  }

  private createSolid(key: string, width: number, height: number, color: number): void {
    const gfx = this.make.graphics({ x: 0, y: 0, add: false });
    gfx.fillStyle(color, 1);
    gfx.fillRect(0, 0, width, height);
    gfx.generateTexture(key, width, height);
    gfx.destroy();
  }
}
