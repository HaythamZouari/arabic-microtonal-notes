#!/usr/bin/env python3
"""Pré-rend les 49 notes du kanun par PSOLA depuis un seul enregistrement de référence
(refs/kanun.wav, ~329 Hz). Durée cible 2 s. Sortie : notes/kanun/note-<i>.wav (mono 22050 Hz)."""
import os, wave, audioop, struct
from build_pitch import read_mono, detect_f0, psola, G2, OUT_RATE, TOTAL
from build_violin import trim_onset_full

SRC = "refs/kanun.wav"
DST = "notes/kanun"
TARGET_SEC = 2.0


def main():
    os.makedirs(DST, exist_ok=True)
    x, sr = read_mono(SRC)
    x = trim_onset_full(x, sr)
    f0 = detect_f0(x, sr)
    stretch = 1.0  # kanun pincé -> durée naturelle (pas d'étirement)
    print(f"kanun : f0 = {f0:.1f} Hz | {len(x)/sr:.2f}s -> x{stretch:.2f}")
    total = 0
    for i in range(TOTAL):
        f1 = G2 * (2 ** (i / 24))
        y = psola(x, sr, f0, f1, stretch=stretch)
        raw = struct.pack("<%dh" % len(y), *[max(-32768, min(32767, int(v * 32767))) for v in y])
        raw, _ = audioop.ratecv(raw, 2, 1, sr, OUT_RATE, None)
        out = DST + f"/note-{i}.wav"
        with wave.open(out, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(OUT_RATE)
            w.writeframes(raw)
        total += os.path.getsize(out)
    print(f"{TOTAL} notes rendues dans {DST}/ — total {total // 1024} Ko")


if __name__ == "__main__":
    main()
