import parselmouth
import os
import numpy as np

# === Dossier contenant les fichiers ===
folder_path = 'solsolsol'
output_file = 'frequences_parselmouth.txt'

# === Ouvrir le fichier texte en écriture ===
with open(output_file, 'w') as out_file:
    # === Parcourir tous les fichiers wav ===
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav'):
            file_path = os.path.join(folder_path, filename)
            print(f"Traitement : {filename}")

            try:
                # Charger l'audio avec parselmouth
                snd = parselmouth.Sound(file_path)

                # Extraire la hauteur (pitch)
                pitch = snd.to_pitch()

                # Récupérer les fréquences détectées (en Hz)
                frequencies = pitch.selected_array['frequency']

                # Garder uniquement les valeurs valides (> 0 Hz)
                frequencies = frequencies[frequencies > 0]

                # Calcul de la fréquence fondamentale
                if len(frequencies) > 0:
                    fundamental_freq = np.median(frequencies)
                    out_file.write(f"{filename} : {fundamental_freq:.2f} Hz\n")
                else:
                    out_file.write(f"{filename} : aucune fréquence détectée\n")
            except Exception as e:
                out_file.write(f"{filename} : erreur ({e})\n")
