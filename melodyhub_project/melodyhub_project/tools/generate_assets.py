"""
Generates every media file used by the demo website (100% original, copyright-free):

  static/audio/<slug>.mp3        synthesized instrumental track
  static/images/songs/<slug>.jpg procedurally drawn cover art
  static/video/<slug>.mp4        music-visualizer video (silent, synced by JavaScript)
  static/images/logo.svg         site logo

Run (optional - the files are already included):
    pip install numpy pillow
    python tools/generate_assets.py            # needs ffmpeg installed
"""
import importlib.util
import math
import os
import random
import subprocess
import sys
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC = os.path.join(ROOT, "static")
SR = 44100

# ---------------------------------------------------------------- catalogue
spec = importlib.util.spec_from_file_location("songs", os.path.join(ROOT, "player", "songs.py"))
songs_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(songs_mod)
SONGS = songs_mod.SONGS

# ------------------------------------------------------------ music theory
SCALES = {
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "major": [0, 2, 4, 5, 7, 9, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygdom": [0, 1, 4, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
}

# musical recipe for every song (keyed by slug)
CONFIG = {
    "neon-skyline":   dict(bpm=108, beats=4, root=57, scale="minor",   prog=[0, 5, 2, 6], chords="arp",   bass="eighths", drums="pop",   lead="saw",   seed=1),
    "monsoon-lofi":   dict(bpm=78,  beats=4, root=53, scale="major",   prog=[1, 4, 0, 5], chords="piano", bass="root",    drums="lofi",  lead="pluck", seed=2),
    "golden-hour":    dict(bpm=100, beats=4, root=55, scale="major",   prog=[0, 4, 5, 3], chords="stab",  bass="eighths", drums="pop",   lead="pluck", seed=3),
    "desert-caravan": dict(bpm=96,  beats=4, root=50, scale="phrygdom", prog=[0, 0, 3, 0], chords="pad",   bass="root",    drums="perc",  lead="flute", seed=4),
    "cosmic-drift":   dict(bpm=70,  beats=4, root=48, scale="lydian",  prog=[0, 1, 0, 4], chords="pad",   bass="root",    drums="none",  lead="bell",  seed=5),
    "rooftop-groove": dict(bpm=122, beats=4, root=52, scale="dorian",  prog=[0, 3, 0, 4], chords="stab",  bass="funk",    drums="funk",  lead="square", seed=6),
    "temple-bells":   dict(bpm=84,  beats=4, root=50, scale="dorian",  prog=[0, 6, 4, 0], chords="bell",  bass="root",    drums="perc",  lead="flute", seed=7),
    "sunrise-waltz":  dict(bpm=96,  beats=3, root=50, scale="major",   prog=[0, 4, 5, 3], chords="piano", bass="root",    drums="waltz", lead="pluck", seed=8),
    "thunder-run":    dict(bpm=140, beats=4, root=48, scale="minor",   prog=[0, 5, 6, 4], chords="arp",   bass="eighths", drums="rock",  lead="saw",   seed=9),
    "ocean-breeze":   dict(bpm=100, beats=4, root=58, scale="major",   prog=[0, 5, 3, 4], chords="stab",  bass="root",    drums="lofi",  lead="bell",  seed=10),
}

RHYTHMS_4 = [
    [(0, 4), (4, 2), (6, 2), (8, 4), (12, 4)],
    [(0, 2), (2, 2), (4, 4), (8, 2), (10, 2), (12, 4)],
    [(0, 6), (6, 2), (8, 4), (12, 2), (14, 2)],
    [(0, 4), (4, 4), (8, 8)],
    [(0, 3), (3, 3), (6, 2), (8, 3), (11, 3), (14, 2)],
    [(0, 2), (2, 2), (4, 2), (6, 2), (8, 4), (12, 4)],
]
RHYTHMS_3 = [[(0, 4), (4, 4), (8, 4)], [(0, 6), (6, 3), (9, 3)], [(0, 3), (3, 3), (6, 6)], [(0, 2), (2, 2), (4, 4), (8, 4)]]


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def degree_to_midi(cfg, degree):
    sc = SCALES[cfg["scale"]]
    octave, idx = divmod(degree, 7)
    return cfg["root"] + sc[idx] + 12 * octave


# ------------------------------------------------------------------ voices
def _t(dur):
    return np.arange(int(dur * SR)) / SR


def _release(sig, tail=0.02):
    n = min(len(sig), int(tail * SR))
    if n > 0:
        sig[-n:] *= np.linspace(1, 0, n)
    return sig


def v_pad(f, dur):
    t = _t(dur)
    s = 0
    for d in (-0.5, 0, 0.5):
        ff = f * (1 + d / 100)
        s = s + np.sin(2 * np.pi * ff * t) + 0.3 * np.sin(4 * np.pi * ff * t) + 0.12 * np.sin(6 * np.pi * ff * t)
    e = np.minimum(1, t / 0.25) * np.clip((dur - t) / 0.35, 0, 1)
    return s * e / 3


def v_saw(f, dur, vib=True):
    t = _t(dur)
    ph = 2 * np.pi * f * t + (0.02 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.3) if vib else 0)
    s = sum(np.sin(h * ph) / h for h in range(1, 9))
    e = np.minimum(1, t / 0.01) * np.exp(-t * 1.2) * np.clip((dur - t) / 0.08, 0, 1)
    return s * e * 0.6


def v_square(f, dur):
    t = _t(dur)
    ph = 2 * np.pi * f * t
    s = sum(np.sin(h * ph) / h for h in (1, 3, 5, 7))
    e = np.minimum(1, t / 0.005) * np.exp(-t * 5) * np.clip((dur - t) / 0.03, 0, 1)
    return s * e


def v_pluck(f, dur, decay=6.0):
    t = _t(dur)
    s = sum(np.sin(2 * np.pi * f * h * t) / h ** 1.3 * math.exp(-0.25 * h) ** 0 for h in range(1, 7))
    e = np.minimum(1, t / 0.003) * np.exp(-t * decay)
    return _release(s * e)


def v_piano(f, dur):
    t = _t(dur)
    s = sum(np.sin(2 * np.pi * f * h * t) * a * np.exp(-t * (2.5 + h * 1.2)) for h, a in ((1, 1), (2, .5), (3, .3), (4, .18), (5, .1)))
    e = np.minimum(1, t / 0.004)
    return _release(s * e)


def v_bell(f, dur):
    t = _t(dur)
    s = 0
    for ratio, amp, dec in ((1, 1, 1.6), (2.76, .55, 2.4), (5.4, .3, 3.5), (8.93, .15, 5)):
        s = s + amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t * dec)
    return _release(s * np.minimum(1, t / 0.002))


def v_flute(f, dur, rng):
    t = _t(dur)
    vib = np.sin(2 * np.pi * 5 * t) * 0.012 * np.minimum(1, t / 0.2)
    ph = 2 * np.pi * f * t + vib * 6
    s = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    s += np.random.default_rng(rng.randint(0, 9999)).normal(0, 0.012, len(t))
    e = np.minimum(1, t / 0.06) * np.clip((dur - t) / 0.12, 0, 1) * (0.8 + 0.2 * np.exp(-t * 3))
    return s * e


def v_bass(f, dur, decay=4.0):
    t = _t(dur)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.1 * np.sin(6 * np.pi * f * t)
    e = np.minimum(1, t / 0.008) * np.exp(-t * decay) * np.clip((dur - t) / 0.03, 0, 1)
    return s * e


def d_kick(vol=1.0):
    t = _t(0.35)
    f = 45 + 90 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9) * vol


def d_snare(rng, vol=1.0):
    t = _t(0.25)
    noise = np.random.default_rng(rng.randint(0, 99999)).normal(0, 1, len(t))
    return (noise * 0.7 * np.exp(-t * 22) + np.sin(2 * np.pi * 185 * t) * 0.5 * np.exp(-t * 28)) * vol


def d_hat(rng, vol=1.0, decay=70):
    t = _t(0.08)
    noise = np.random.default_rng(rng.randint(0, 99999)).normal(0, 1, len(t))
    return np.diff(noise, prepend=0) * np.exp(-t * decay) * 0.5 * vol


def d_tom(f, vol=1.0):
    t = _t(0.3)
    fr = f * (1 + 0.6 * np.exp(-t * 25))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 10) * vol


def echo(sig, delay, fb, taps):
    out = sig.copy()
    d = int(delay * SR)
    for k in range(1, taps + 1):
        s = k * d
        if s >= len(out):
            break
        out[s:] += sig[: len(out) - s] * (fb ** k)
    return out


def place(buf, sig, start, gain=1.0, pan=0.0):
    if start >= len(buf) or len(sig) == 0:
        return
    end = min(len(buf), start + len(sig))
    seg = sig[: end - start] * gain
    buf[start:end, 0] += seg * (1 - max(0, pan))
    buf[start:end, 1] += seg * (1 + min(0, pan))


# -------------------------------------------------------------- song render
def render_song(cfg, target_seconds=34):
    rng = random.Random(cfg["seed"])
    beats = cfg["beats"]
    spb = beats * 4                       # steps (16ths) per bar
    step = 60.0 / cfg["bpm"] / 4
    bar_sec = step * spb
    bars = max(12, round(target_seconds / bar_sec))
    total = int((bars * bar_sec + 1.5) * SR)

    chords_b = np.zeros((total, 2))
    bass_b = np.zeros((total, 2))
    drums_b = np.zeros((total, 2))
    lead_b = np.zeros((total, 2))
    prog = cfg["prog"]

    # ---- pre-generate two 4-bar melody phrases (A, B)
    rhythms = RHYTHMS_4 if beats == 4 else RHYTHMS_3
    phrases = []
    for _ in range(2):
        slots = []
        offset = rng.choice([0, 2, 4])
        for _bar in range(4):
            notes = []
            for (st, ln) in rng.choice(rhythms):
                if rng.random() < 0.12:
                    continue
                offset = max(-1, min(9, offset + rng.choice([-2, -1, -1, 0, 1, 1, 2])))
                notes.append((st, ln, offset))
            slots.append(notes)
        phrases.append(slots)

    def at(bar, s):
        return int((bar * spb + s) * step * SR)

    for bar in range(bars):
        d = prog[bar % 4]
        tri = [d, d + 2, d + 4]
        # ---------------- chords
        mode = cfg["chords"]
        if mode == "pad":
            for deg in tri:
                place(chords_b, v_pad(mtof(degree_to_midi(cfg, deg + 7)), bar_sec + 0.1), at(bar, 0), 0.10)
        elif mode == "arp":
            order = [0, 1, 2, 3, 2, 1, 2, 1]
            notes = [d + 7, d + 9, d + 11, d + 14]
            for i in range(0, spb, 2):
                f = mtof(degree_to_midi(cfg, notes[order[(i // 2) % 8] % 4]))
                place(chords_b, v_pluck(f, step * 3, 9), at(bar, i), 0.20, pan=0.25 if (i // 2) % 2 else -0.25)
            for deg in tri:
                place(chords_b, v_pad(mtof(degree_to_midi(cfg, deg + 7)), bar_sec + 0.05), at(bar, 0), 0.05)
        elif mode == "stab":
            pat = [0, 3, 6, 10, 12] if beats == 4 else [0, 4, 8]
            for s in pat:
                for deg in tri:
                    place(chords_b, v_pluck(mtof(degree_to_midi(cfg, deg + 7)), step * 2.5, 14), at(bar, s), 0.10)
            place(chords_b, v_pad(mtof(degree_to_midi(cfg, d + 7)), bar_sec), at(bar, 0), 0.05)
        elif mode == "piano":
            place(chords_b, v_piano(mtof(degree_to_midi(cfg, d - 7)), bar_sec * 0.9), at(bar, 0), 0.28)
            hits = [4, 8, 12] if beats == 4 else [4, 8]
            if cfg["bass"] == "root" and beats == 4:
                hits = [2, 6, 10, 14] if cfg["drums"] == "lofi" else hits
            for s in hits:
                for deg in tri:
                    place(chords_b, v_piano(mtof(degree_to_midi(cfg, deg + 7)), step * 3), at(bar, s), 0.16)
        elif mode == "bell":
            for s in range(0, spb, 8 if beats == 4 else 6):
                for deg in (d + 7, d + 11):
                    place(chords_b, v_bell(mtof(degree_to_midi(cfg, deg)), 2.5), at(bar, s), 0.16)
            for deg in tri[:2]:
                place(chords_b, v_pad(mtof(degree_to_midi(cfg, deg + 7)), bar_sec + 0.1), at(bar, 0), 0.07)

        # ---------------- bass
        broot = mtof(degree_to_midi(cfg, d - 7))
        bm = cfg["bass"]
        if bm == "eighths":
            for i in range(0, spb, 2):
                f = broot * (2 if (i // 2) % 4 == 3 else 1)
                place(bass_b, v_bass(f, step * 1.8, 6), at(bar, i), 0.42)
        elif bm == "root":
            for s in range(0, spb, 8 if beats == 4 else 12):
                place(bass_b, v_bass(broot, step * 7.5, 2.5), at(bar, s), 0.45)
        elif bm == "funk":
            fifth = mtof(degree_to_midi(cfg, d - 3))
            for s, f in ((0, broot), (3, broot), (6, fifth), (8, broot), (11, broot * 2), (14, fifth)):
                place(bass_b, v_bass(f, step * 2, 7), at(bar, s), 0.45)

        # ---------------- drums (start after intro bar)
        dm = cfg["drums"]
        if dm != "none" and bar >= 1:
            if dm == "pop":
                for s in (0, 8): place(drums_b, d_kick(0.9), at(bar, s), 0.8)
                for s in (4, 12): place(drums_b, d_snare(rng, 0.8), at(bar, s), 0.5)
                for s in range(0, 16, 2): place(drums_b, d_hat(rng, 0.7), at(bar, s), 0.35)
            elif dm == "lofi":
                for s in (0, 10): place(drums_b, d_kick(0.8), at(bar, s), 0.7)
                for s in (4, 12): place(drums_b, d_snare(rng, 0.5), at(bar, s), 0.4)
                for s in range(0, 16, 2):
                    off = int(step * 0.35 * SR) if (s // 2) % 2 else 0
                    place(drums_b, d_hat(rng, 0.5, 90), at(bar, s) + off, 0.3)
            elif dm == "rock":
                for s in (0, 6, 8, 14): place(drums_b, d_kick(1.0), at(bar, s), 0.85)
                for s in (4, 12): place(drums_b, d_snare(rng, 1.0), at(bar, s), 0.6)
                for s in range(0, 16, 2): place(drums_b, d_hat(rng, 1.0, 55), at(bar, s), 0.35)
            elif dm == "funk":
                for s in (0, 7, 10): place(drums_b, d_kick(0.9), at(bar, s), 0.75)
                for s in (4, 12): place(drums_b, d_snare(rng, 0.9), at(bar, s), 0.5)
                for s in range(16): place(drums_b, d_hat(rng, 0.7 if s % 4 else 1.0, 80), at(bar, s), 0.28)
            elif dm == "perc":
                for s, f in ((0, 85), (6, 85), (10, 100), (4, 150), (12, 150), (14, 170)):
                    place(drums_b, d_tom(f, 0.9), at(bar, s), 0.55)
                for s in range(0, 16, 2): place(drums_b, d_hat(rng, 0.6, 110), at(bar, s), 0.3)
            elif dm == "waltz":
                place(drums_b, d_kick(0.6), at(bar, 0), 0.5)
                for s in (4, 8): place(drums_b, d_hat(rng, 0.8, 60), at(bar, s), 0.3)

        # ---------------- lead (starts after 2-bar intro)
        if bar >= 2:
            phrase = phrases[(bar // 4) % 2][bar % 4]
            for st, ln, off in phrase:
                f = mtof(degree_to_midi(cfg, d + 7 + off))
                dur = ln * step * (1.05 if cfg["lead"] in ("flute", "saw") else 1.6)
                lm = cfg["lead"]
                if lm == "saw": sig, g = v_saw(f, dur), 0.20
                elif lm == "square": sig, g = v_square(f, dur), 0.14
                elif lm == "pluck": sig, g = v_pluck(f, dur, 3.5), 0.38
                elif lm == "bell": sig, g = v_bell(f * 2, max(dur, 1.6)), 0.26
                else: sig, g = v_flute(f, dur, rng), 0.30
                place(lead_b, sig, at(bar, st), g, pan=0.15)

    lead_b = echo(lead_b, 60.0 / cfg["bpm"] * 0.75, 0.38, 4)
    mix = chords_b + bass_b + drums_b + lead_b
    # stereo width: tiny Haas delay on the right channel
    d = int(0.012 * SR)
    mix[d:, 1] = mix[d:, 1] * 0.8 + mix[:-d, 0] * 0.2
    mix = mix[: int((bars * bar_sec + 1.0) * SR)]
    # fade in / out
    n_in, n_out = int(0.05 * SR), int(2.5 * SR)
    mix[:n_in] *= np.linspace(0, 1, n_in)[:, None]
    mix[-n_out:] *= np.linspace(1, 0, n_out)[:, None]
    mix = np.tanh(mix / (np.max(np.abs(mix)) + 1e-9) * 1.6) * 0.85
    return mix


def write_mp3(samples, path):
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "x.wav")
        with wave.open(wav, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((samples * 32767).astype("<i2").tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-codec:a", "libmp3lame",
                        "-b:a", "112k", path], check=True)


# ---------------------------------------------------------------- cover art
def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def gradient(size, c1, c2):
    a, b = np.array(hex2rgb(c1), float), np.array(hex2rgb(c2), float)
    t = np.linspace(0, 1, size)[:, None, None]
    arr = (a * (1 - t) + b * t) * np.ones((size, size, 3))
    return Image.fromarray(arr.astype("uint8"), "RGB").convert("RGBA")


def wave_poly(d, size, y0, amp, freq, phase, fill):
    pts = [(x, y0 + amp * math.sin(x / size * freq * 2 * math.pi + phase)) for x in range(0, size + 20, 20)]
    d.polygon(pts + [(size, size), (0, size)], fill=fill)


def make_cover(song, out_path, size=1200):
    c1, c2, acc = song["colors"]
    img = gradient(size, c1, c2)
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    A = hex2rgb(acc)
    W = (255, 255, 255)
    rnd = random.Random(song["id"] * 7)
    slug = song["slug"]
    if slug == "neon-skyline":
        d.ellipse((300, 250, 900, 850), fill=A + (255,))
        for i in range(8):
            y = 520 + i * 48
            d.rectangle((250, y, 950, y + 8 + i * 4), fill=hex2rgb(c1) + (255,))
        d.rectangle((0, 850, size, size), fill=hex2rgb(c1) + (255,))
        for i in range(-12, 13):
            d.line((600 + i * 40, 850, 600 + i * 190, size), fill=A + (200,), width=5)
        for i in range(6):
            d.line((0, 850 + i * i * 12, size, 850 + i * i * 12), fill=A + (200,), width=5)
    elif slug == "monsoon-lofi":
        d.ellipse((780, 130, 1000, 350), fill=(255, 245, 210, 255))
        for _ in range(80):
            x, y = rnd.randint(0, size), rnd.randint(0, 800)
            d.line((x, y, x - 14, y + 50), fill=W + (110,), width=4)
        x = 0
        while x < size:
            w, h = rnd.randint(70, 150), rnd.randint(200, 520)
            d.rectangle((x, size - h, x + w, size), fill=(10, 20, 30, 255))
            for wy in range(size - h + 25, size - 20, 50):
                if rnd.random() < 0.5:
                    d.rectangle((x + 14, wy, x + 34, wy + 24), fill=(255, 214, 120, 255))
            x += w + 8
    elif slug == "golden-hour":
        for r, a in ((520, 60), (420, 90), (320, 140)):
            d.ellipse((600 - r, 520 - r, 600 + r, 520 + r), fill=(255, 255, 255, a))
        d.ellipse((380, 300, 820, 740), fill=(255, 250, 225, 255))
        wave_poly(d, size, 820, 60, 1.5, 0.5, (150, 70, 20, 255))
        wave_poly(d, size, 960, 50, 2.2, 2.0, (95, 40, 15, 255))
    elif slug == "desert-caravan":
        d.ellipse((700, 180, 960, 440), fill=(255, 235, 190, 255))
        wave_poly(d, size, 640, 90, 1.2, 0.3, (200, 120, 60, 255))
        wave_poly(d, size, 800, 110, 1.6, 2.2, (150, 80, 35, 255))
        wave_poly(d, size, 980, 80, 2.0, 4.0, (95, 45, 20, 255))
        for i in range(4):
            x = 250 + i * 110
            d.ellipse((x, 705, x + 70, 745), fill=(40, 20, 10, 255))
            d.rectangle((x + 28, 745, x + 38, 800), fill=(40, 20, 10, 255))
    elif slug == "cosmic-drift":
        for _ in range(160):
            x, y, r = rnd.randint(0, size), rnd.randint(0, size), rnd.randint(2, 6)
            d.ellipse((x, y, x + r, y + r), fill=W + (rnd.randint(120, 255),))
        d.ellipse((330, 330, 870, 870), fill=A + (255,))
        d.ellipse((380, 380, 700, 700), fill=(255, 255, 255, 70))
        d.arc((150, 520, 1050, 760), 0, 360, fill=(255, 255, 255, 230), width=14)
        d.arc((190, 540, 1010, 740), 0, 360, fill=(255, 255, 255, 140), width=8)
    elif slug == "rooftop-groove":
        for i in range(-3, 9):
            x = i * 190
            d.polygon([(x, size), (x + 90, size), (x + 90 + 600, 0), (x + 600, 0)], fill=A + (120 if i % 2 else 220,))
        d.ellipse((420, 420, 780, 780), fill=hex2rgb(c1) + (255,))
        d.ellipse((470, 470, 730, 730), fill=A + (255,))
        d.ellipse((580, 580, 620, 620), fill=hex2rgb(c1) + (255,))
    elif slug == "temple-bells":
        cx = cy = size // 2
        for k in range(12):
            a = k * math.pi / 6
            pts = []
            for t in range(0, 360, 20):
                tr = math.radians(t)
                rx, ry = 120, 300
                x, y = rx * math.cos(tr), ry * math.sin(tr) + 300
                pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
            d.polygon(pts, fill=A + (90,), outline=W + (200,))
        for r in (120, 80, 40):
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=A + (255,) if r == 40 else None, outline=W + (255,), width=6)
    elif slug == "sunrise-waltz":
        cx, cy = 600, 760
        for k in range(18):
            a1, a2 = math.pi + k * math.pi / 18, math.pi + (k + 0.5) * math.pi / 18
            d.polygon([(cx, cy), (cx + 1100 * math.cos(a1), cy + 1100 * math.sin(a1)),
                       (cx + 1100 * math.cos(a2), cy + 1100 * math.sin(a2))], fill=W + (60,))
        d.ellipse((cx - 230, cy - 230, cx + 230, cy + 230), fill=(255, 245, 220, 255))
        wave_poly(d, size, 880, 40, 1.0, 1.0, hex2rgb(c1) + (255,))
    elif slug == "thunder-run":
        d.polygon([(220, 1100), (600, 0), (1000, 1100), (880, 1100), (600, 260), (340, 1100)], fill=(255, 255, 255, 40))
        d.polygon([(700, 80), (380, 640), (560, 640), (470, 1120), (850, 480), (650, 480)], fill=A + (255,), outline=W + (255,))
    elif slug == "ocean-breeze":
        d.ellipse((760, 150, 1000, 390), fill=(255, 250, 220, 255))
        for i, col in enumerate(((255, 255, 255, 60), (255, 255, 255, 90), (6, 90, 110, 200), (3, 60, 85, 255))):
            wave_poly(d, size, 560 + i * 150, 55 - i * 5, 2.0 + i * 0.4, i * 1.3, col)
    img = Image.alpha_composite(img, layer).convert("RGB").resize((600, 600), Image.LANCZOS)
    img.save(out_path, quality=86, optimize=True)
    return img


# ---------------------------------------------------------------- video
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def make_video(song, cover, mp3, out_path):
    c1, c2, acc = song["colors"]
    W_, H_ = 640, 360
    bg = gradient(W_, "#000000", "#000000").resize((W_, H_))
    g1, g2 = np.array(hex2rgb(c1), float), np.array(hex2rgb(c2), float)
    t = np.linspace(0, 1, W_)[None, :, None]
    arr = (g1 * (1 - t) + g2 * t * 0.55) * np.ones((H_, W_, 3))
    bg = Image.fromarray(arr.astype("uint8"), "RGB")
    # rounded cover
    cv = cover.resize((220, 220), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (220, 220), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 219, 219), 22, fill=255)
    bg.paste(cv, (36, 70), mask)
    d = ImageDraw.Draw(bg)
    d.text((290, 44), song["title"], font=ImageFont.truetype(FONT_B, 28), fill=(255, 255, 255))
    d.text((290, 82), f'{song["singer"]}  -  {song["movie"]}', font=ImageFont.truetype(FONT_R, 15), fill=(235, 235, 235))
    d.text((36, 312), "MelodyHub  -  Now playing", font=ImageFont.truetype(FONT_R, 14), fill=(235, 235, 235))
    with tempfile.TemporaryDirectory() as tmp:
        bgp = os.path.join(tmp, "bg.png")
        bg.save(bgp)
        accent = "0x" + acc.lstrip("#")
        fc = (f"[1:a]showfreqs=s=330x190:mode=bar:fscale=log:ascale=sqrt:colors={accent}:win_size=1024:rate=15,"
              f"colorkey=0x000000:0.25:0.1[fx];[0:v][fx]overlay=290:122:format=auto,format=yuv420p[v]")
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3],
                             capture_output=True, text=True, check=True).stdout.strip()
        subprocess.run(["ffmpeg", "-y", "-nostdin", "-loglevel", "error", "-loop", "1", "-framerate", "15", "-i", bgp, "-i", mp3,
                        "-filter_complex", fc, "-map", "[v]", "-t", dur, "-r", "15", "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "31", "-an", "-movflags", "+faststart", out_path], check=True)


LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="MelodyHub logo">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#ec4899"/></linearGradient></defs>
  <rect width="64" height="64" rx="16" fill="url(#g)"/>
  <path d="M42 14v26.5a7.5 7.5 0 1 1-4-6.6V22l-14 3v20.5a7.5 7.5 0 1 1-4-6.6V21z" fill="#fff"/>
</svg>
"""


def main():
    for sub in ("audio", "video", "images/songs"):
        os.makedirs(os.path.join(STATIC, sub), exist_ok=True)
    with open(os.path.join(STATIC, "images", "logo.svg"), "w") as f:
        f.write(LOGO)
    for song in SONGS:
        slug = song["slug"]
        print("->", slug, flush=True)
        mp3 = os.path.join(STATIC, "audio", f"{slug}.mp3")
        write_mp3(render_song(CONFIG[slug]), mp3)
        cover = make_cover(song, os.path.join(STATIC, "images", "songs", f"{slug}.jpg"))
        make_video(song, cover, mp3, os.path.join(STATIC, "video", f"{slug}.mp4"))
    print("done")


if __name__ == "__main__":
    sys.exit(main())
