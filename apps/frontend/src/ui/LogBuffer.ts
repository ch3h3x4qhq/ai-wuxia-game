export class LogBuffer {
  private lines: string[] = [];
  constructor(private readonly limit = 8) {}

  push(entries: string[]): void {
    this.lines.push(...entries);
    if (this.lines.length > this.limit) {
      this.lines = this.lines.slice(this.lines.length - this.limit);
    }
  }

  snapshot(): string {
    return this.lines.join('\n');
  }
}
