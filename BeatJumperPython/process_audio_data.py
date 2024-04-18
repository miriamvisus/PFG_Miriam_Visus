import socket
import librosa
import numpy as np
import scipy.signal as signal
import requests
import os
import tempfile
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, Dense, Activation, Flatten, Reshape, UpSampling2D, MaxPooling2D, BatchNormalization, Dropout, LeakyReLU, Concatenate
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.layers import concatenate
from io import BytesIO
import struct
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment

#Calcular tempo y energía
def process_audio_data(audio_file):
    try:
        # Cargar los datos de audio utilizando librosa.load()
        y, sr = librosa.load(audio_file)

        # Calcular el tempo
        tempo = calculate_tempo(y, sr)

        # Calcular la energía
        energy = librosa.feature.rms(y=y)

        print("Tempo:", tempo)
        print("Energía:", energy)

        return tempo, energy

    except Exception as e:
        print(f"Error al procesar datos de audio: {e}")


def calculate_tempo(y, sr):
    # Calcular la autocorrelación del audio
    autocorr = np.correlate(y, y, mode='full')

    # Tomar solo la parte positiva de la autocorrelación (lado derecho del eje)
    autocorr = autocorr[len(autocorr) // 2:]

    # Encontrar los picos en la autocorrelación
    peaks, _ = signal.find_peaks(autocorr, height=0)

    # Calcular el tempo en beats por minuto (BPM)
    if len(peaks) > 1:
        tempo = sr / (peaks[1] - peaks[0]) * 60
        return tempo
    else:
        return None


# Cargar las imágenes desde el repositorio Git
def load_audios_from_git(git_repo_url, audio_folder, num_audios):
    tempos = []
    energias = []
    base_url = git_repo_url.rstrip('/')  + '/raw/main'

    for i in range(num_audios):
        audio_path = f"{audio_folder}/Audio{i+1}.mp3"
        audio_url = f"{base_url}/{audio_path}"

        response_audio = requests.get(audio_url)

        if response_audio.status_code == 200:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio_file:
                temp_audio_file.write(response_audio.content)
                temp_audio_file.close()
                audio_file_path = temp_audio_file.name

                try:
                    # Procesar los datos de audio
                    print(f"Procesando audio {i+1}")
                    tempo, energy = process_audio_data(audio_file_path)

                    # Agregar los datos a las listas acumuladas
                    tempos.append(np.array(tempo))
                    energias.append(np.array(energy))

                finally:
                    # Eliminar el archivo temporal después de usarlo
                    os.unlink(audio_file_path)
        else:
            print(f"Failed to fetch audio from {audio_url}. Status code: {response_audio.status_code}")

    return np.array(tempos), np.array(energias)


# Especifica los nombres de las carpetas y la cantidad de imágenes por carpeta en el repositorio Git
git_repo_url = 'https://github.com/miriamvisus/PFG_Miriam_Visus_Martin'
audio_folder = 'AUDIOS'
num_audios = 20


# Carga los audios desde el repositorio Git
tempos, energias = load_audios_from_git(git_repo_url, audio_folder, num_audios)

# Dividir los datos en conjuntos de entrenamiento y prueba
tempos_train, tempos_test, energias_train, energias_test = train_test_split(tempos, energias, test_size=0.2, random_state=42)

# Definir la arquitectura del modelo CNN
model = Sequential([
    Conv1D(64, 3, activation='relu', input_shape=(None, 1)),
    MaxPooling1D(2),
    Conv1D(128, 3, activation='relu'),
    MaxPooling1D(2),
    Conv1D(256, 3, activation='relu'),
    MaxPooling1D(2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    Dense(2)  # Dos salidas: tempo y energía
])

# Compilar el modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(energias_train, tempos_train, epochs=10, batch_size=32, validation_data=(energias_test, tempos_test))

# Evaluar el modelo en el conjunto de prueba
loss = model.evaluate(energias_test, tempos_test)
print("Loss:", loss)



