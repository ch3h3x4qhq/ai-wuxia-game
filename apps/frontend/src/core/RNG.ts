export class Mulberry32 {
  private state: number;

  constructor(seed: number) {
    this.state = seed >>> 0;
  }

  random(): number {
    this.state = (this.state + 0x6d2b79f5) >>> 0;
    let t = this.state;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }

  randInt(min: number, max: number): number {
    if (min > max) {
      [min, max] = [max, min];
    }
    const span = max - min + 1;
    const value = Math.floor(this.random() * span);
    return min + Math.min(span - 1, value);
  }
}
