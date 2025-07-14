import librosa
import parselmouth
import numpy as np
import os

# === Config ===
folder_path = 'solsolsol'
output_file = 'frequences_hybride.txt'
fmin = 50
fmax = 1000

# === Fonction de détection avec librosa ===
def detect_pitch_librosa(file_path):
    try:
        y, sr = librosa.load(file_path)
        f0 = librosa.yin(y, fmin=fmin, fmax=fmax, sr=sr, frame_length=512)
        f0_valid = f0[~np.isnan(f0)]
        return np.median(f0_valid) if len(f0_valid) > 0 else None
    except:
        return None

# === Fonction de détection avec parselmouth ===
def detect_pitch_parselmouth(file_path):
    try:
        snd = parselmouth.Sound(file_path)
        pitch = snd.to_pitch()
        freqs = pitch.selected_array['frequency']
        freqs = freqs[freqs > 0]
        return np.median(freqs) if len(freqs) > 0 else None
    except:
        return None

# === Traitement de chaque fichier ===
with open(output_file, 'w') as out_file:
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav'):
            file_path = os.path.join(folder_path, filename)
            print(f"Traitement : {filename}")

            freq_librosa = detect_pitch_librosa(file_path)
            freq_parsel = detect_pitch_parselmouth(file_path)

            # Fusion logique :
            if freq_librosa and freq_parsel:
                diff_ratio = abs(freq_librosa - freq_parsel) / max(freq_librosa, freq_parsel)
                if diff_ratio < 0.2:
                    freq_final = np.mean([freq_librosa, freq_parsel])
                    note = f"{filename} : {freq_final:.2f} Hz (✓)"
                else:
                    note = f"{filename} : INCERTAIN — librosa={freq_librosa:.2f}, parselmouth={freq_parsel:.2f}"
            elif freq_parsel:
                note = f"{filename} : {freq_parsel:.2f} Hz (parselmouth seul)"
            elif freq_librosa:
                note = f"{filename} : {freq_librosa:.2f} Hz (librosa seul)"
            else:
                note = f"{filename} : aucune fréquence détectée"

            out_file.write(note + "\n")
