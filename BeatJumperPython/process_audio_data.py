from typing import List, Any

import librosa
import numpy as np
import requests
import os
import tempfile
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Conv2D, Dense, Activation, Flatten, Reshape, UpSampling2D, MaxPooling2D, BatchNormalization, Dropout, LeakyReLU, Concatenate
from tensorflow.keras.optimizers import Adam

#Calcular duración máxima
def calculate_max_duration(git_repo_url, audio_folder, num_audios):
    base_url = git_repo_url.rstrip('/')  + '/raw/main'
    max_duration = 0

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

                    print(f"Calculando la duración del audio {i + 1}")

                    # Actualizar la duración máxima
                    duration = librosa.get_duration(filename=audio_file_path)
                    print("Duración:", duration)
                    if duration > max_duration:
                        max_duration = duration
                    print(f"Duración máxima hasta el audio {i + 1}:", max_duration)

                finally:
                    # Eliminar el archivo temporal después de usarlo
                    os.unlink(audio_file_path)
        else:
                print(f"Failed to fetch audio from {audio_url}. Status code: {response_audio.status_code}")

    return max_duration


#Calcular tempo y energía
def process_audio_data(audio_file, max_duration):
    try:
        # Cargar los datos de audio utilizando librosa.load()
        y, sr = librosa.load(audio_file, sr=None)

        # Asegurar que todos los audios tengan la misma duración
        y = librosa.util.fix_length(y, size=int(max_duration * sr))

        # Calcular el tempo
        tempo = librosa.beat.tempo(y=y, sr=sr)

        # Calcular la energía
        energy = librosa.feature.rms(y=y)

        print("Tempo:", tempo)
        print("Energía:", energy)

        return tempo, energy

    except Exception as e:
        print(f"Error al procesar datos de audio: {e}")


# Cargar los audios desde el repositorio Git
def load_audios_from_git(git_repo_url, audio_folder, num_audios, max_duration):
    tempos = []
    energies = []
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
                    tempo, energy = process_audio_data(audio_file_path, max_duration)

                    # Imprimir las formas de los datos
                    print("Forma del tempo:", tempo.shape)
                    print("Forma de la energía:", energy.shape)

                    # Convertir tempo y energía a arrays numpy de una sola fila y varias columnasç
                    tempos.append(tempo)
                    energies.append(energy)

                finally:
                    # Eliminar el archivo temporal después de usarlo
                    os.unlink(audio_file_path)
        else:
                print(f"Failed to fetch audio from {audio_url}. Status code: {response_audio.status_code}")

    return np.array(tempos), np.array(energies)

# Especifica los nombres de las carpetas y la cantidad de imágenes por carpeta en el repositorio Git
git_repo_url = 'https://github.com/miriamvisus/PFG_Miriam_Visus_Martin'
audio_folder = 'AUDIOS'
num_audios = 5

#Calcular duración máxima
max_duration = calculate_max_duration(git_repo_url, audio_folder, num_audios)

# Carga los audios desde el repositorio Git
tempos, energies = load_audios_from_git(git_repo_url, audio_folder, num_audios, max_duration)


# Ajustar la velocidad del personaje en base al tempo del audio
def adjust_character_speed(tempo):

    # Lógica para ajustar la velocidad del personaje en función del tempo
    if tempo < 100:
        return 5.0
    elif 100 <= tempo < 120:
        return 6.0
    else:
        return 7.0


#Generar frecuencia de generación de plataformas
def adjust_platform_frequency(tempo):

    # Frecuencia de generación de plataformas en segundos
    generation_frequency = 1.0 / (tempo / 60.0)
    return generation_frequency


#Generar altura de las plataformas
def adjust_platform_height(energies):

    # Factor de escala para ajustar la altura de las plataformas en función de la energía
    energy_scale_factor = 100

    # Altura base de las plataformas
    base_platform_height = 0.0  # Altura en unidades de Unity

    # Limitar la altura de las plataformas en la escena de Unity al rango de -3 a 10
    min_height = -3.0
    max_height = 10.0
    platform_heights = []  # Lista para almacenar las etiquetas correspondientes a las plataformas generadas

    # Iterar sobre las energías de cada audio y ajustar la altura de las plataformas
    for energy in energies:
        for energy_value in energy:

            # Ajustar la altura de las plataformas en función de la energía
            platform_height = base_platform_height + energy_value * energy_scale_factor

            # Limitar la altura al rango especificado
            platform_height = np.clip(platform_height, min_height, max_height)

            platform_heights.append(platform_height)

    return platform_heights


character_speeds = []
platform_frequencies = []
platform_heights: list[list[float | Any]] = []

# Iterar sobre los datos de audio y ajustar la velocidad del personaje y generar plataformas
for i in range(num_audios):

    # Ajustar la velocidad del personaje
    character_speed = adjust_character_speed(tempos[i])
    character_speeds.append(character_speed)

    # Generar frecuencia de generación de plataformas
    platform_frequency = adjust_platform_frequency(tempos[i])
    platform_frequencies.append(platform_frequencies)

    # Generar altura de las plataformas
    platform_heights_audio = adjust_platform_height(energies[i])
    platform_heights.append(platform_heights_audio)

character_speeds = np.array(character_speeds)
platform_frequencies = np.array(platform_frequencies)



# Dividir los datos de tempo y energía en conjuntos de entrenamiento y prueba
tempos_train, tempos_test, energies_train, energies_test = train_test_split(tempos, energies, test_size=0.2, random_state=42)

# Crear características adicionales para las plataformas!!!!!!!
avg_energy = [np.mean(energy) for energy in energies]  # Calcular la energía promedio para cada plataforma
avg_energy_np = np.array(avg_energy)

# Dividir energía promedio para cada plataforma en conjuntos de entrenamiento y prueba
avg_energy_train, avg_energy_test = train_test_split(avg_energy_np, test_size=0.2, random_state=42)

# Expandir tempos_train para que tenga dos dimensiones
tempos_train_expanded = np.expand_dims(tempos_train, axis=-1)

# Reemplazar la forma de tempos_train_expanded con la forma de energies_train
tempos_train_expanded = np.repeat(tempos_train_expanded, energies_train.shape[2], axis=-1)

# Utilizar np.column_stack para unir los datos de entrada!!!!!!
x_train = np.column_stack((tempos_train_expanded, energies_train))

# Unir las características de las plataformas con los datos de entrada existentes !!!!!
x_train_platforms = np.column_stack((tempos_train_expanded, energies_train, avg_energy_train))

# Expandir tempos_test para que tenga tres dimensiones
tempos_test_expanded = np.expand_dims(tempos_test, axis=-1)

# Reemplazar la forma de tempos_test_expanded con la forma de energies_test
tempos_test_expanded = np.repeat(tempos_test_expanded, energies_test.shape[2], axis=-1)

# Utilizar np.column_stack para unir los datos de entrada de prueba !!!!
x_test = np.column_stack((tempos_test_expanded, energies_test))

# Utilizar np.column_stack para unir los datos de entrada de prueba !!!!!
x_test_platforms = np.column_stack((tempos_test_expanded, energies_test, avg_energy_test))

# Dividir las etiquetas de velocidad en conjuntos de entrenamiento y prueba de manera consistente
character_speeds_train, character_speeds_test = train_test_split(character_speeds, test_size=0.2, random_state=42)

# Dividir las etiquetas de frecuencia plataformas en conjuntos de entrenamiento y prueba de manera consistente
platform_frequencies_train, platform_frequencies_test = train_test_split(platform_frequencies, test_size=0.2, random_state=42)

# Concatenar las velocidades del personaje con las etiquetas originales
y_train = np.column_stack((character_speeds_train, platform_frequencies_train))

# Concatenar las velocidades del personaje con las etiquetas originales
y_test = np.column_stack((character_speeds_test, platform_frequencies_test))

print("Forma de x_train:", x_train_platforms.shape)
print("Forma de x_test:", x_test_platforms.shape)
print("Forma de y_train:", y_train.shape)
print("Forma de y_test:", y_test.shape)


def create_model():
    model = Sequential([
        # Capa de entrada: concatena las características de tempo y energía
        Input(shape=(2, energies_train.shape[2])),  # 2 características: tempo y energía
        # Capa densa con activación ReLU
        Dense(64, activation='relu'),
        # Capa de salida: una neurona para predecir la velocidad del personaje
        Dense(1)  # Salida continua para la velocidad
    ])
    return model

# Crear el modelo
model = create_model()

# Compilar el modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(
    x=x_train,  # Usamos los datos de entrada ajustados para el entrenamiento
    y=y_train,  # Etiquetas de salida: velocidades del personaje
    epochs=10,
    batch_size=32,
    validation_data=(x_test, y_test)  # Datos de validación
)

# Evaluar el modelo en el conjunto de prueba
loss = model.evaluate(x_test, y_test)
print("Loss:", loss)