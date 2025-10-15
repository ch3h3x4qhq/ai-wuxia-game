import Phaser from 'phaser';

import { createGameConfig } from './game';

function bootstrap(): void {
  // eslint-disable-next-line no-new
  new Phaser.Game(createGameConfig());
}

document.addEventListener('DOMContentLoaded', bootstrap);
