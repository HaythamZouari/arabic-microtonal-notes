#!/usr/bin/env python3
"""Pré-rend les 49 notes par pitch-shift à FORMANTS PRÉSERVÉS (TD-PSOLA).

On part d'un seul enregistrement clair (sans titre-24.wav, recadré sur l'attaque)
et on transpose sa hauteur vers chaque note de la gamme SANS rééchantillonner les
grains → l'enveloppe spectrale (formants) est conservée, contrairement au simple
playbackRate. Sortie : notes/voix/note-<i>.wav (mono, 22050 Hz).

Méthode :
  - détection de f0 de la source par autocorrélation
  - grains de 2 périodes, fenêtrés Hann, centrés sur des marques d'analyse (k*T0)
  - re-synthèse : marques espacées de la période cible T1 = sr/f_cible
  - overlap-add normalisé par la somme des fenêtres (gain constant)
"""
import os, wave, audioop, math

DST = "notes/voix"
TOTAL = 49
G2 = 98.0
OUT_RATE = 22050

# Une seule référence (Sol grave ~98 Hz) pour toutes les notes, en UPSHIFT.
#   (fichier source, plage de notes rendues)
REFS = [
    ("solsolsol/sans titre.wav", range(0, 49)),  # ~98 Hz -> toutes les notes (transposition vers l'aigu)
]


def read_mono(path):
    with wave.open(path, "rb") as w:
        ch, wd, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        data = w.readframes(n)
    if ch == 2:
        data = audioop.tomono(data, wd, 0.5, 0.5)
    # -> liste de floats [-1,1]
    import struct
    cnt = len(data) // wd
    ints = struct.unpack("<%dh" % cnt, data) if wd == 2 else struct.unpack("<%db" % cnt, data)
    scale = float(1 << (8 * wd - 1))
    return [s / scale for s in ints], sr


def trim_onset(x, sr):
    peak = max(abs(v) for v in x) or 1.0
    thr = peak * 0.12
    win = int(sr * 0.01)
    onset = 0
    for s in range(0, len(x) - win, win):
        if max(abs(v) for v in x[s:s + win]) > thr:
            onset = max(0, s - int(sr * 0.03)); break
    end = min(len(x), onset + int(sr * 1.4))
    return x[onset:end]


def detect_f0(x, sr):
    # autocorrélation sur une fenêtre médiane
    mid = len(x) // 2
    w = x[max(0, mid - int(sr * 0.02)):mid + int(sr * 0.02)]
    lo, hi = int(sr / 400), int(sr / 80)
    best_lag, best = lo, -1e9
    for lag in range(lo, hi):
        s = 0.0
        for n in range(0, len(w) - lag):
            s += w[n] * w[n + lag]
        if s > best:
            best, best_lag = s, lag
    return sr / best_lag


def psola(x, sr, f0, f1):
    T0 = sr / f0
    T1 = sr / f1
    N = len(x)
    L = int(round(2 * T0))
    half = L // 2
    hann = [0.5 - 0.5 * math.cos(2 * math.pi * n / (L - 1)) for n in range(L)]
    out = [0.0] * N
    norm = [0.0] * N
    pos = float(half)
    while pos < N:
        center = int(round(pos))
        k = round(center / T0)                 # marque d'analyse la plus proche
        a = int(round(k * T0))
        base_o = center - half
        base_x = a - half
        for n in range(L):
            oi = base_o + n
            xi = base_x + n
            if 0 <= oi < N and 0 <= xi < N:
                out[oi] += x[xi] * hann[n]
                norm[oi] += hann[n]
        pos += T1
    for i in range(N):
        if norm[i] > 1e-6:
            out[i] /= norm[i]
    return out


def write_wav(path, x, sr):
    import struct
    # normalise légèrement pour éviter tout dépassement
    peak = max(1e-9, max(abs(v) for v in x))
    g = min(1.0, 0.97 / peak)
    ints = [max(-32768, min(32767, int(v * g * 32767))) for v in x]
    data = struct.pack("<%dh" % len(ints), *ints)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(data)


def main():
    os.makedirs(DST, exist_ok=True)
    import struct
    total = 0
    for src, rng in REFS:
        x, sr = read_mono(src)
        x = trim_onset(x, sr)
        f0 = detect_f0(x, sr)
        print(f"{src}: f0 = {f0:.1f} Hz -> notes {rng.start+1}..{rng.stop}")
        for i in rng:
            f1 = G2 * (2 ** (i / 24))
            y = psola(x, sr, f0, f1)  # upshift : f1 >= f0
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
