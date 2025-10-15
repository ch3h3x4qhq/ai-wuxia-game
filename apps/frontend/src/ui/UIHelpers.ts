import Phaser from 'phaser';

export function drawBar(
  scene: Phaser.Scene,
  x: number,
  y: number,
  width: number,
  height: number,
  percentage: number,
  color: number
): Phaser.GameObjects.Graphics {
  const gfx = scene.add.graphics();
  gfx.lineStyle(2, 0xfacc15, 1);
  gfx.strokeRect(x, y, width, height);
  gfx.fillStyle(color, 1);
  gfx.fillRect(x + 2, y + 2, (width - 4) * Phaser.Math.Clamp(percentage, 0, 1), height - 4);
  return gfx;
}
