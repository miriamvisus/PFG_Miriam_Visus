import librosa
import numpy as np
import requests
import os
import tempfile

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Dense, Dropout, LeakyReLU, Concatenate, LSTM
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
num_audios = 115

#Calcular duración máxima
max_duration = calculate_max_duration(git_repo_url, audio_folder, num_audios)

# Carga los audios desde el repositorio Git
tempos, energies = load_audios_from_git(git_repo_url, audio_folder, num_audios, max_duration)


# Ajustar la velocidad del personaje en base al tempo del audio
def adjust_character_speed(tempo):

    # Lógica para ajustar la velocidad del personaje en función del tempo
    if tempo < 100:
        return 5.0
    elif 100 <= tempo < 110:
        return 6.0
    elif 110 <= tempo < 120:
        return 7.0
    else:
        return 8.0


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

    # Espacio mínimo y máximo entre las alturas de las plataformas
    min_platform_space = 0
    max_platform_space = 4

    last_platform_height = base_platform_height  # Inicializar la altura de la última plataforma

    # Iterar sobre las energías de cada audio y ajustar la altura de las plataformas
    for energy in energies:
        for energy_value in energy:

            # Ajustar la altura de las plataformas en función de la energía
            platform_height = base_platform_height + energy_value * energy_scale_factor

            # Limitar la altura al rango especificado
            platform_height = np.clip(platform_height, min_height, max_height)

            # Asegurar que el espacio entre plataformas esté dentro del rango permitido
            platform_height = np.clip(platform_height, last_platform_height + min_platform_space,
                                      last_platform_height + max_platform_space)

            platform_heights.append(platform_height)

            # Actualizar la altura de la última plataforma
            last_platform_height = platform_height

    return np.array(platform_heights)


character_speeds = []
platform_frequencies = []
platform_heights = []

# Iterar sobre los datos de audio y ajustar la velocidad del personaje y generar plataformas
for i in range(num_audios):

    # Ajustar la velocidad del personaje
    character_speed = adjust_character_speed(tempos[i])
    character_speeds.append(character_speed)

    # Generar frecuencia de generación de plataformas
    platform_frequency = adjust_platform_frequency(tempos[i])
    platform_frequencies.append(platform_frequency)

    # Generar frecuencia de generación de plataformas
    platform_heights_audio = adjust_platform_height(energies[i])
    platform_heights.extend(platform_heights_audio)

character_speeds = np.array(character_speeds)
platform_frequencies = np.array(platform_frequencies)
platform_heights = np.array(platform_heights)

print("Forma de platform_heights:", platform_heights.shape)
# Redimensionar platform_heights para que todos los arrays tengan el mismo número de muestras
platform_heights = np.reshape(platform_heights, (num_audios, 1, energies.shape[2]))


# Dividir los datos de tempo y energía en conjuntos de entrenamiento y prueba
tempos_train, tempos_test, energies_train, energies_test = train_test_split(tempos, energies, test_size=0.2, random_state=42)

# Dividir las etiquetas de velocidad en conjuntos de entrenamiento y prueba de manera consistente
character_speeds_train, character_speeds_test = train_test_split(character_speeds, test_size=0.2, random_state=42)

# Dividir las etiquetas de frecuencia de plataformas en conjuntos de entrenamiento y prueba de manera consistente
platform_frequencies_train, platform_frequencies_test = train_test_split(platform_frequencies, test_size=0.2, random_state=42)

# Dividir las etiquetas de altura de plataformas en conjuntos de entrenamiento y prueba de manera consistente
platform_heights_train, platform_heights_test = train_test_split(platform_heights, test_size=0.2, random_state=42)


def create_model():
    # Capa de entrada para el tempo
    tempo_input = Input(shape=(1, ), name='tempo_input')  # Una característica: tempo

    # Capa de entrada para la energía
    energy_input = Input(shape=(energies_train.shape[1], energies_train.shape[2]), name='energy_input')  # Varias características: energía

    dense_tempo = Dense(128, activation='relu')(tempo_input)
    dense_tempo = Dense(64, activation='relu')(dense_tempo)
    dense_tempo = Dense(32, activation='relu')(dense_tempo)
    dense_tempo = Dense(16, activation='relu')(dense_tempo)
    dense_tempo = Dense(8, activation='relu')(dense_tempo)
    dense_tempo = Dropout(0.5)(dense_tempo)

    dense_energy = Dense(128, activation='relu')(energy_input)
    dense_energy = Dense(64, activation='relu')(dense_energy)
    dense_energy = Dense(32, activation='relu')(dense_energy)
    dense_energy = Dense(16, activation='relu')(dense_energy)
    dense_energy = Dense(8, activation='relu')(dense_energy)
    dense_energy = Dropout(0.5)(dense_energy)

    # Capa de salida para la velocidad del personaje
    output_speed = Dense(1, name='output_speed')(dense_tempo)  # Salida continua para la velocidad del personaje

    # Capa de salida para la frecuencia de generación de plataformas
    output_frequency = Dense(1, name='output_frequency')(dense_tempo)  # Salida continua para la frecuencia de generación de plataformas

    # Capa de salida para la altura de las plataformas
    output_height = Dense(1, name='output_height')(dense_energy)  # Salida continua para la altura de las plataformas

    # Modelo que toma dos entradas: tempo y energía, y tiene tres salidas: velocidad, frecuencia y altura
    model = Model(inputs=[tempo_input, energy_input], outputs=[output_speed, output_frequency, output_height])

    return model

# Crear el modelo
model = create_model()

# Compilar el modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
model.fit(
    x=[tempos_train, energies_train],  # Usamos los datos de entrada ajustados para el entrenamiento
    y=[character_speeds_train, platform_frequencies_train, platform_heights_train],  # Etiquetas de salida
    epochs=1000,
    batch_size=32,
    validation_data=([tempos_test, energies_test], [character_speeds_test, platform_frequencies_test, platform_heights_test])  # Datos de validación
)

# Evaluar el modelo en el conjunto de prueba
loss = model.evaluate([tempos_test, energies_test], [character_speeds_test, platform_frequencies_test, platform_heights_test])
print("Pérdida en el conjunto de prueba:", loss)

# Guardar el modelo entreando
model.save('trained_model.h5')
# Guardar el modelo entreando
model.save('trained_model.keras')
