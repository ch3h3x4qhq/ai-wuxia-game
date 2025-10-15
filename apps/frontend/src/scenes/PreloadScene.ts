import Phaser from 'phaser';

import TitleScene from './TitleScene';

export default class PreloadScene extends Phaser.Scene {
  static KEY = 'PreloadScene';

  constructor() {
    super({ key: PreloadScene.KEY });
  }

  create(): void {
    this.scene.start(TitleScene.KEY);
  }
}
