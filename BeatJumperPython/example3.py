import librosa
import numpy as np
import requests
import os
import tempfile
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam


# Calcular espectrogramas y tempo/energía
def process_audio_data(audio_file, target_shape):
    try:
        y, sr = librosa.load(audio_file, sr=None)  # Especifica sr=None para evitar remuestreo

        # Corregir la longitud del audio si es necesario
        y = librosa.util.fix_length(y, size=target_shape[0])

        # Imprimir la longitud del audio cargado
        print(f"Longitud del audio cargado: {len(y)}")

        # Calcular el espectrograma
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

        # Calcular el tempo
        tempo = librosa.beat.tempo(y=y, sr=sr)

        # Calcular la energía
        energy = librosa.feature.rms(y=y)

        return spectrogram, tempo, energy

    except Exception as e:
        print(f"Error al procesar datos de audio: {e}")



# Cargar audios desde un repositorio Git
def load_audios_from_git(git_repo_url, audio_folder, num_audios, target_shape):
    spectrograms = []
    tempos = []
    energies = []
    base_url = git_repo_url.rstrip('/') + '/raw/main'

    for i in range(num_audios):
        audio_path = f"{audio_folder}/Audio{i + 1}.mp3"
        audio_url = f"{base_url}/{audio_path}"

        response_audio = requests.get(audio_url)

        if response_audio.status_code == 200:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio_file:
                temp_audio_file.write(response_audio.content)
                temp_audio_file.close()
                audio_file_path = temp_audio_file.name

                try:
                    # Procesar los datos de audio
                    print(f"Procesando audio {i + 1}")
                    spectrogram, tempo, energy = process_audio_data(audio_file_path, target_shape)

                    # Agregar los datos a las listas acumuladas
                    spectrograms.append(spectrogram)
                    tempos.append(tempo)
                    energies.append(energy)

                finally:
                    # Eliminar el archivo temporal después de usarlo
                    os.unlink(audio_file_path)
        else:
            print(f"Failed to fetch audio from {audio_url}. Status code: {response_audio.status_code}")

    return np.array(spectrograms), np.array(tempos), np.array(energies)


# Especifica los nombres de las carpetas y la cantidad de audios en el repositorio Git
git_repo_url = 'https://github.com/miriamvisus/PFG_Miriam_Visus_Martin'
audio_folder = 'AUDIOS'
num_audios = 3
target_shape = (128, 128)  # Especifica la forma deseada para los espectrogramas

# Cargar los audios desde el repositorio Git
spectrograms, tempos, energies = load_audios_from_git(git_repo_url, audio_folder, num_audios, target_shape)

# Dividir los datos en conjuntos de entrenamiento y prueba
spectrograms_train, spectrograms_test, tempos_train, tempos_test, energies_train, energies_test = train_test_split(
    spectrograms, tempos, energies, test_size=0.2, random_state=42
)

# Definir la arquitectura del modelo CNN
model = Sequential([
    Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=target_shape + (1,)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    Dense(2)  # Dos salidas: tempo y energía
])

# Compilar el modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(
    x=spectrograms_train[..., np.newaxis],  # Agregar una dimensión para el canal (escala de grises)
    y=np.stack((tempos_train, energies_train), axis=-1),  # Apilar tempo y energía como una sola matriz de salida
    epochs=10,
    batch_size=32,
    validation_data=(spectrograms_test[..., np.newaxis], np.stack((tempos_test, energies_test), axis=-1))
)

# Evaluar el modelo en el conjunto de prueba
loss = model.evaluate(spectrograms_test[..., np.newaxis], np.stack((tempos_test, energies_test), axis=-1))
print("Loss:", loss)
