import librosa
import numpy as np
import os

# === Dossier contenant les fichiers ===
folder_path = 'solsolsol'
output_file = 'frequences.txt'

# === Paramètres YIN ===
fmin = 50
fmax = 1000

# === Ouvrir le fichier texte en écriture ===
with open(output_file, 'w') as out_file:
    # === Parcourir tous les fichiers wav ===
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav'):
            file_path = os.path.join(folder_path, filename)
            print(f"Traitement : {filename}")

            try:
                # Charger l'audio
                y, sr = librosa.load(file_path)

                # Détection de la fondamentale
                f0 = librosa.yin(y, fmin=fmin, fmax=fmax, sr=sr)

                # Nettoyer les valeurs NaN
                f0_valid = f0[~np.isnan(f0)]

                # Calcul de la médiane (fréquence fondamentale)
                if len(f0_valid) > 0:
                    fundamental_freq = np.median(f0_valid)
                    out_file.write(f"{filename} : {fundamental_freq:.2f} Hz\n")
                else:
                    out_file.write(f"{filename} : aucune fréquence détectée\n")
            except Exception as e:
                out_file.write(f"{filename} : erreur ({e})\n")
