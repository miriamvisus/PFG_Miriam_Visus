import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


audio_file = "C:\\Users\miria.PORMIR\PFG_Miriam_Visus_Martin\AUDIOS\Audio2.mp3"
# Cargar el audio
y, sr = librosa.load(audio_file)

# Calcular el espectrograma
spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

# Mostrar el espectrograma
plt.figure(figsize=(10, 4))
librosa.display.specshow(librosa.power_to_db(spectrogram, ref=np.max), y_axis='mel', fmax=8000, x_axis='time')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel spectrogram')
plt.show()