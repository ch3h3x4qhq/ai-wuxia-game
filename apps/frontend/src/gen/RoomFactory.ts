export interface RoomTemplate {
  code: string;
  tag: string;
  layout: string[];
}

export interface RoomTile {
  x: number;
  y: number;
  glyph: string;
}

export function parseRoom(template: RoomTemplate): RoomTile[] {
  const tiles: RoomTile[] = [];
  template.layout.forEach((row, y) => {
    row.split('').forEach((glyph, x) => {
      tiles.push({ x, y, glyph });
    });
  });
  return tiles;
}
