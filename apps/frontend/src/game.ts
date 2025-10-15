import Phaser from 'phaser';

import BootScene from './scenes/BootScene';
import PreloadScene from './scenes/PreloadScene';
import TitleScene from './scenes/TitleScene';
import MapScene from './scenes/MapScene';
import RoomScene from './scenes/RoomScene';
import UIScene from './scenes/UIScene';
import { GAME_HEIGHT, GAME_WIDTH } from './core/Constants';

export function createGameConfig(): Phaser.Types.Core.GameConfig {
  return {
    type: Phaser.AUTO,
    width: GAME_WIDTH,
    height: GAME_HEIGHT,
    parent: 'app',
    backgroundColor: '#0d0f1a',
    physics: {
      default: 'arcade'
    },
    scene: [BootScene, PreloadScene, TitleScene, MapScene, RoomScene, UIScene]
  };
}
