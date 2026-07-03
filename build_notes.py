#!/usr/bin/env python3
"""Génère des versions allégées des enregistrements pour une lecture web rapide.

Pour chaque note (sol -> sol -> sol, 49 fichiers) :
  - rogne 2 s au début et 1 s à la fin
  - convertit en mono
  - réduit l'échantillonnage à 22050 Hz
  - écrit dans le dossier notes/ sous le nom note-<i>.wav

Les fichiers d'origine dans solsolsol/ ne sont pas modifiés.
"""
import os, wave, audioop

SRC = "solsolsol"
DST = "notes"
TRIM_START = 0.0  # secondes coupées au début
TRIM_END = 0.0    # secondes coupées à la fin
TARGET_RATE = 22050
TOTAL = 49


def src_name(i):
    return "sans titre.wav" if i == 0 else f"sans titre-{i + 1}.wav"


def process(i):
    path = os.path.join(SRC, src_name(i))
    with wave.open(path, "rb") as w:
        ch, width, rate, nframes = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        data = w.readframes(nframes)

    # Rognage (en octets)
    start = min(int(TRIM_START * rate), nframes)
    end = max(start, nframes - int(TRIM_END * rate))
    bytes_per_frame = ch * width
    data = data[start * bytes_per_frame:end * bytes_per_frame]

    # Stéréo -> mono
    if ch == 2:
        data = audioop.tomono(data, width, 0.5, 0.5)
    ch = 1

    # Rééchantillonnage
    if rate != TARGET_RATE:
        data, _ = audioop.ratecv(data, width, ch, rate, TARGET_RATE, None)
        rate = TARGET_RATE

    out = os.path.join(DST, f"note-{i}.wav")
    with wave.open(out, "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(width)
        w.setframerate(rate)
        w.writeframes(data)
    return os.path.getsize(out)


def main():
    os.makedirs(DST, exist_ok=True)
    total = 0
    for i in range(TOTAL):
        total += process(i)
    print(f"{TOTAL} fichiers générés dans {DST}/ — total {total // 1024} Ko")


if __name__ == "__main__":
    main()
