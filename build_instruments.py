#!/usr/bin/env python3
"""Pré-rend les 49 notes de plusieurs instruments par PSOLA depuis une note de référence.
Durée cible 2 s. Sortie : notes/<nom>/note-<i>.wav (mono 22050 Hz)."""
import os, wave, audioop, struct
from build_pitch import read_mono, detect_f0, psola, G2, OUT_RATE, TOTAL
from build_violin import trim_onset_full

# target = None -> durée naturelle (pincé/frappé) ; sinon durée cible en secondes (tenu)
JOBS = [
    ("refs/oud.wav",   "notes/oud",   None),  # oud pincé -> naturel
    ("refs/nai.wav",   "notes/ney",   2.0),   # ney tenu -> 2 s
    ("refs/piano.wav", "notes/piano", None),  # piano frappé -> naturel
]


def render(src, dst, target):
    os.makedirs(dst, exist_ok=True)
    x, sr = read_mono(src)
    x = trim_onset_full(x, sr)
    f0 = detect_f0(x, sr)
    stretch = 1.0 if target is None else target / (len(x) / sr)
    print(f"{dst}: f0 = {f0:.1f} Hz | {len(x)/sr:.2f}s -> x{stretch:.2f}")
    total = 0
    for i in range(TOTAL):
        f1 = G2 * (2 ** (i / 24))
        y = psola(x, sr, f0, f1, stretch=stretch)
        raw = struct.pack("<%dh" % len(y), *[max(-32768, min(32767, int(v * 32767))) for v in y])
        raw, _ = audioop.ratecv(raw, 2, 1, sr, OUT_RATE, None)
        with wave.open(dst + f"/note-{i}.wav", "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(OUT_RATE)
            w.writeframes(raw)
        total += os.path.getsize(dst + f"/note-{i}.wav")
    print(f"  {TOTAL} notes -> {dst}/ ({total // 1024} Ko)")


if __name__ == "__main__":
    for s, d, tgt in JOBS:
        render(s, d, tgt)
