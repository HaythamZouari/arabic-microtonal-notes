import librosa
import numpy as np
import matplotlib.pyplot as plt

# === Charger le fichier audio ===
file_path = '47_48.wav'  # Remplace par le nom de ton fichier
y, sr = librosa.load(file_path)

# === Détection de la fondamentale avec YIN ===
f0 = librosa.yin(y, fmin=50, fmax=1000, sr=sr)

# === Supprimer les valeurs invalides ===
f0_valid = f0[~np.isnan(f0)]

# === Calcul de la fréquence fondamentale moyenne ===
fundamental_freq = np.median(f0_valid)
print(f"Fréquence fondamentale estimée : {fundamental_freq:.2f} Hz")

# === Tracer les fréquences sur le temps ===
times = librosa.times_like(f0, sr=sr)
plt.plot(times, f0, label='Fréquence fondamentale (YIN)', color='darkgreen')
plt.xlabel('Temps (s)')
plt.ylabel('Fréquence (Hz)')
plt.title('Détection de la fréquence fondamentale')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
