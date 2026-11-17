"""Procedural sound effects for the Marble Tilt Maze (Task 4).

The tones are synthesised at start-up, so the game ships without binary audio
assets and still works if the machine has no sound card: if the mixer cannot be
opened the bank simply stays disabled and the game runs silently.
"""
import array
import math

import pygame

RATE = 44100


def _envelope(i, n, attack=0.01, release=0.35):
    """Simple attack/release envelope so tones do not click."""
    t = i / float(n)
    a = min(1.0, t / attack) if attack > 0 else 1.0
    r = min(1.0, (1.0 - t) / release) if release > 0 else 1.0
    return a * r


def _tone(freq, ms, volume=0.35, harmonics=((1, 1.0),), sweep_to=None):
    """Build stereo 16-bit PCM for one note (optionally frequency-swept)."""
    n = int(RATE * ms / 1000.0)
    buf = array.array("h", bytes(4 * n))
    phase = 0.0
    for i in range(n):
        t = i / float(n)
        f = freq if sweep_to is None else freq + (sweep_to - freq) * t
        phase += 2.0 * math.pi * f / RATE
        sample = 0.0
        for mult, amp in harmonics:
            sample += amp * math.sin(phase * mult)
        sample *= _envelope(i, n) * volume
        sample = max(-1.0, min(1.0, sample))
        v = int(sample * 32767)
        buf[2 * i] = v
        buf[2 * i + 1] = v
    return buf


def _sequence(notes):
    out = array.array("h")
    for buf in notes:
        out.extend(buf)
    return out


class SoundBank:
    """Holds the three effects and degrades gracefully to silence."""

    def __init__(self, enabled=True):
        self.enabled = False
        self.muted = not enabled
        self.bounce_sound = None
        self.goal_sound = None
        self.timeout_sound = None
        if not enabled:
            return
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=RATE, size=-16, channels=2, buffer=512)

            # bounce: short, low "thud" with a couple of harmonics
            bounce = _tone(150, 80, volume=0.45,
                           harmonics=((1, 1.0), (2, 0.45), (3, 0.2)))
            # goal: rising arpeggio C5 - E5 - G5 - C6
            goal = _sequence([_tone(f, 110, volume=0.35, release=0.5)
                              for f in (523.25, 659.25, 783.99, 1046.5)])
            # timeout: descending buzz
            timeout = _tone(320, 550, volume=0.4, harmonics=((1, 1.0), (2, 0.5)),
                            sweep_to=90)

            self.bounce_sound = pygame.mixer.Sound(buffer=bounce.tobytes())
            self.goal_sound = pygame.mixer.Sound(buffer=goal.tobytes())
            self.timeout_sound = pygame.mixer.Sound(buffer=timeout.tobytes())
            self.enabled = True
        except Exception:
            # No audio device (CI, headless capture, no sound card): stay silent.
            self.enabled = False

    def _play(self, sound, volume=0.8):
        if not self.enabled or self.muted or sound is None:
            return
        try:
            sound.set_volume(volume)
            sound.play()
        except Exception:
            self.enabled = False

    def bounce(self, strength=1.0):
        self._play(self.bounce_sound, min(1.0, 0.35 + 0.5 * strength))

    def goal(self):
        self._play(self.goal_sound, 0.9)

    def timeout(self):
        self._play(self.timeout_sound, 0.9)
