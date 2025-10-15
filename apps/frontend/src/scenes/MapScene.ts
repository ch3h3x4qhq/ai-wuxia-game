import Phaser from 'phaser';

import RoomScene from './RoomScene';
import { RunState } from '../types';

interface MapSceneData {
  runId: string;
}

export default class MapScene extends Phaser.Scene {
  static KEY = 'MapScene';
  private run?: RunState;
  private selected = 0;
  private nodes: Phaser.GameObjects.Graphics[] = [];
  private labels: Phaser.GameObjects.Text[] = [];

  constructor() {
    super({ key: MapScene.KEY });
  }

  create(data: MapSceneData): void {
    this.run = this.registry.get('run') as RunState | undefined;
    if (!this.run) {
      this.scene.start('TitleScene');
      return;
    }
    this.selected = this.run.node_index;
    this.drawMap();

    this.input.keyboard?.on('keydown-LEFT', () => this.shiftSelection(-1));
    this.input.keyboard?.on('keydown-RIGHT', () => this.shiftSelection(1));
    this.input.keyboard?.on('keydown-ENTER', () => {
      if (!this.run) return;
      this.run.node_index = this.selected;
      this.registry.set('run', this.run);
      this.scene.start(RoomScene.KEY, { runId: data.runId, nodeIndex: this.selected });
    });
  }

  private shiftSelection(delta: number): void {
    if (!this.run) return;
    const total = this.run.node_map.nodes.length;
    this.selected = (this.selected + delta + total) % total;
    this.drawMap();
  }

  private drawMap(): void {
    this.nodes.forEach((node) => node.destroy());
    this.labels.forEach((label) => label.destroy());
    this.nodes = [];
    this.labels = [];
    if (!this.run) return;

    const width = this.scale.width;
    const height = this.scale.height;
    const spacing = width / (this.run.node_map.nodes.length + 1);

    this.run.node_map.nodes.forEach((node, idx) => {
      const gfx = this.add.graphics();
      const x = spacing * (idx + 1);
      const y = height / 2;
      const radius = idx === this.selected ? 28 : 18;
      const color = node.tag === 'boss' ? 0xdc2626 : 0x38bdf8;
      gfx.fillStyle(color, idx === this.selected ? 1 : 0.6);
      gfx.fillCircle(x, y, radius);
      gfx.lineStyle(2, 0xfacc15, idx === this.selected ? 1 : 0.4);
      gfx.strokeCircle(x, y, radius + 4);
      const label = this.add
        .text(x, y + radius + 10, node.tag, { fontSize: '16px', color: '#f8fafc' })
        .setOrigin(0.5);
      this.nodes.push(gfx);
      this.labels.push(label);
    });
  }
}
