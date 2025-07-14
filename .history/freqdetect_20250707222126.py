# === Traitement de chaque fichier ===
with open(output_file, 'w', encoding='utf-8') as out_file:
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav'):
            file_path = os.path.join(folder_path, filename)
            print(f"Traitement : {filename}")

            freq_librosa = detect_pitch_librosa(file_path)
            freq_parsel = detect_pitch_parselmouth(file_path)

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
