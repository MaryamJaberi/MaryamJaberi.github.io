// Optional procedural cosmic/ambient sound generator using Web Audio API
class AudioAmbientEngine {
  private ctx: AudioContext | null = null;
  private osc1: OscillatorNode | null = null;
  private osc2: OscillatorNode | null = null;
  private gainNode: GainNode | null = null;
  private isPlaying: boolean = false;

  public init() {
    if (this.ctx) return;
    try {
      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
      if (!AudioCtx) return;
      this.ctx = new AudioCtx();
    } catch {
      // Audio not supported or blocked
    }
  }

  public toggle(): boolean {
    if (this.isPlaying) {
      this.stop();
      return false;
    } else {
      this.start();
      return true;
    }
  }

  public start() {
    this.init();
    if (!this.ctx) return;

    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }

    try {
      const now = this.ctx.currentTime;
      this.gainNode = this.ctx.createGain();
      this.gainNode.gain.setValueAtTime(0.001, now);
      this.gainNode.gain.exponentialRampToValueAtTime(0.04, now + 1.5);
      this.gainNode.connect(this.ctx.destination);

      // Low harmonic cosmic drone
      this.osc1 = this.ctx.createOscillator();
      this.osc1.type = 'sine';
      this.osc1.frequency.setValueAtTime(65.41, now); // C2 drone

      this.osc2 = this.ctx.createOscillator();
      this.osc2.type = 'triangle';
      this.osc2.frequency.setValueAtTime(98.0, now); // G2 fifth

      this.osc1.connect(this.gainNode);
      this.osc2.connect(this.gainNode);

      this.osc1.start();
      this.osc2.start();
      this.isPlaying = true;
    } catch {
      // Graceful fallback
    }
  }

  public stop() {
    if (!this.ctx || !this.gainNode) return;
    try {
      const now = this.ctx.currentTime;
      this.gainNode.gain.setValueAtTime(this.gainNode.gain.value, now);
      this.gainNode.gain.exponentialRampToValueAtTime(0.0001, now + 0.5);
      setTimeout(() => {
        if (this.osc1) { this.osc1.stop(); this.osc1.disconnect(); this.osc1 = null; }
        if (this.osc2) { this.osc2.stop(); this.osc2.disconnect(); this.osc2 = null; }
        this.isPlaying = false;
      }, 550);
    } catch {
      this.isPlaying = false;
    }
  }

  public playEpochTick(isMassExtinction: boolean = false) {
    this.init();
    if (!this.ctx) return;
    try {
      if (this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      const now = this.ctx.currentTime;
      const tickGain = this.ctx.createGain();
      tickGain.gain.setValueAtTime(0.02, now);
      tickGain.gain.exponentialRampToValueAtTime(0.0001, now + (isMassExtinction ? 0.35 : 0.08));
      tickGain.connect(this.ctx.destination);

      const tickOsc = this.ctx.createOscillator();
      tickOsc.type = isMassExtinction ? 'sawtooth' : 'sine';
      tickOsc.frequency.setValueAtTime(isMassExtinction ? 180 : 540, now);
      if (isMassExtinction) {
        tickOsc.frequency.exponentialRampToValueAtTime(45, now + 0.3);
      }
      tickOsc.connect(tickGain);
      tickOsc.start(now);
      tickOsc.stop(now + (isMassExtinction ? 0.35 : 0.08));
    } catch {
      // ignore
    }
  }

  public getStatus(): boolean {
    return this.isPlaying;
  }
}

export const ambientSound = new AudioAmbientEngine();
