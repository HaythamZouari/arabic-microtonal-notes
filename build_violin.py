#!/usr/bin/env python3
"""Pré-rend les 49 notes du violon par PSOLA depuis un seul enregistrement de référence
(refs/violon.wav, ~294 Hz). Sortie : notes/violon/note-<i>.wav (mono 22050 Hz)."""
import os, wave, audioop, struct
from build_pitch import read_mono, detect_f0, psola, G2, OUT_RATE, TOTAL

SRC = "refs/violon.wav"
DST = "notes/violon"
TARGET_SEC = 2.0  # durée voulue de chaque note


def trim_onset_full(x, sr):
    peak = max(abs(v) for v in x) or 1.0
    thr = peak * 0.1
    win = int(sr * 0.01)
    onset = next((s for s in range(0, len(x) - win, win)
                  if max(abs(v) for v in x[s:s + win]) > thr), 0)
    onset = max(0, onset - int(sr * 0.02))
    # fin utile
    end = next((s for s in range(len(x) - win, 0, -win)
                if max(abs(v) for v in x[s:s + win]) > thr), len(x))
    return x[onset:min(len(x), end + int(sr * 0.02))]


def main():
    os.makedirs(DST, exist_ok=True)
    x, sr = read_mono(SRC)
    x = trim_onset_full(x, sr)
    f0 = detect_f0(x, sr)
    stretch = TARGET_SEC / (len(x) / sr)
    print(f"violon : f0 = {f0:.1f} Hz | {len(x)/sr:.2f}s -> {TARGET_SEC}s (x{stretch:.2f})")
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
