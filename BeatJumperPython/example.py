import socket
import librosa
import numpy as np
import scipy.signal as signal
import requests
import os
import tempfile
from io import BytesIO
import struct
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment

# Cargar las imágenes desde el repositorio Git
def load_audios_from_git(git_repo_url, audio_folder, num_audios):
    base_url = git_repo_url.rstrip('/')  + '/raw/main'

    for i in range(num_audios):
        audio_path = f"{audio_folder}/Audio{i+1}.mp3"  # Cambiar la extensión según el formato de tus audios
        audio_url = f"{base_url}/{audio_path}"

        response_audio = requests.get(audio_url)

        if response_audio.status_code == 200:
            audio_content = response_audio.content
            audio_array = np.frombuffer(audio_content, dtype=np.float32)

            samplerate = 44100

            # Guardar los datos de audio en formato WAV
            sf.write("output_audio.wav", audio_array, samplerate)

            # Convertir el archivo WAV a MP3
            audio = AudioSegment.from_wav("output_audio.wav")
            audio.export("output_audio.mp3", format="mp3")

            # Procesar los datos de audio
            tempo, energy = process_audio_data("output_audio.mp3")

            # Eliminar los archivos WAV y MP3 después de usarlos
            os.remove("output_audio.wav")
            os.remove("output_audio.mp3")
        else:
            print(f"Failed to fetch audio from {audio_url}. Status code: {response_audio.status_code}")

        return tempo, energy


# Especifica los nombres de las carpetas y la cantidad de imágenes por carpeta en el repositorio Git
git_repo_url = 'https://github.com/miriamvisus/PFG_Miriam_Visus_Martin'
audio_folder = 'AUDIOS'
num_audios = 33


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


# Carga las imágenes desde el repositorio Git
audios_data = load_audios_from_git(git_repo_url, audio_folder, num_audios)




import socket
import librosa
import numpy as np
import scipy.signal as signal
import requests
import os
import tempfile
from io import BytesIO
import struct
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment

# Cargar las imágenes desde el repositorio Git
def load_audios_from_git(git_repo_url, audio_folder, num_audios):
    base_url = git_repo_url.rstrip('/')  + '/raw/main'

    for i in range(num_audios):
        audio_path = f"{audio_folder}/Audio{i+1}.mp3"  # Cambiar la extensión según el formato de tus audios
        audio_url = f"{base_url}/{audio_path}"

        response_audio = requests.get(audio_url)

        if response_audio.status_code == 200:
            audio_content = BytesIO(response_audio.content)

            samplerate = 44100

            # Guardar los datos de audio en formato WAV
            sf.write("output_audio.wav", audio_content, samplerate)

            # Convertir el archivo WAV a MP3
            audio = AudioSegment.from_wav("output_audio.wav")
            audio.export("output_audio.mp3", format="mp3")

            # Procesar los datos de audio
            tempo, energy = process_audio_data("output_audio.mp3")

            # Eliminar los archivos WAV y MP3 después de usarlos
            os.remove("output_audio.wav")
            os.remove("output_audio.mp3")
        else:
            print(f"Failed to fetch audio from {audio_url}. Status code: {response_audio.status_code}")

        return tempo, energy


# Especifica los nombres de las carpetas y la cantidad de imágenes por carpeta en el repositorio Git
git_repo_url = 'https://github.com/miriamvisus/PFG_Miriam_Visus_Martin'
audio_folder = 'AUDIOS'
num_audios = 33


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


# Carga los audios desde el repositorio Git
audios_data = load_audios_from_git(git_repo_url, audio_folder, num_audios)

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout

datos_etiquetados = [
    {"audio": "Boogie Party.mp3", "tempo": 16333.333333333334, "energia": [[6.2261846e-05, 1.3578097e-02, 1.7227709e-02, 1.2510431e-01,
  1.2431628e-01, 1.0510165e-01]]},
    {"audio": "Brain Dance.mp3", "tempo": 5208.6614173228345, "energia": [[1.2333974e-09, 1.0701557e-06, 1.8551402e-06, 6.3947648e-02,
  6.5589264e-02, 5.8502056e-02]]},
    {"audio": "Hillbilly Swing.mp3", "tempo": 77823.5294117647, "energia": [[1.20071832e-07, 6.23181859e-06, 5.75990889e-05, 1.02966905e-01,
  9.19943750e-02, 7.57390261e-02]]},
]

# Convertir datos etiquetados a un DataFrame de pandas
df = pd.DataFrame(datos_etiquetados)

# Imprimir la longitud de la lista de energía en cada fila
for index, row in df.iterrows():
    print(f"Longitud de la lista de energía en la fila {index}: {len(row['energia'])}")

# Imprimir los tipos de datos antes de la normalización
print("Tipos de datos antes de la normalización:")
print("Tipo de df:", type(df))

# Desempaquetar la lista de energía en columnas separadas
energia_columns = ['energia_' + str(i) for i in range(len(df['energia'][0]))]
df[energia_columns] = pd.DataFrame(df['energia'].tolist(), index=df.index)

print(df)


# Eliminar la columna 'energia' original
df.drop(columns=['energia'], inplace=True)

# División de datos en conjuntos de entrenamiento, validación y prueba
train_data, test_data = train_test_split(df, test_size=0.15, random_state=42)
train_data, val_data = train_test_split(train_data, test_size=0.15, random_state=42)

# Normalización de características
scaler = MinMaxScaler()

# Normalizar 'energia'
for column in energia_columns:
    train_data[column] = train_data[column].apply(lambda x: scaler.fit_transform(np.array(x).reshape(-1, 1)))
    val_data[column] = val_data[column].apply(lambda x: scaler.transform(np.array(x).reshape(-1, 1)))
    test_data[column] = test_data[column].apply(lambda x: scaler.transform(np.array(x).reshape(-1, 1)))

# Normalizar 'tempo'
train_data['tempo'] = scaler.fit_transform(train_data[['tempo']])
val_data['tempo'] = scaler.transform(val_data[['tempo']])
test_data['tempo'] = scaler.transform(test_data[['tempo']])

# Imprimir las columnas de cada conjunto de datos
print("Columnas de datos de entrenamiento:")
print(train_data.columns)

print("\nColumnas de datos de validación:")
print(val_data.columns)

print("\nColumnas de datos de prueba:")
print(test_data.columns)

# Imprimir los tipos de datos después de la normalización
print("\nTipos de datos después de la normalización:")
print("Tipo de train_data:", type(train_data))
print("Tipo de val_data:", type(val_data))
print("Tipo de test_data:", type(test_data))

# Guardar los datos preprocesados
train_data.to_csv('train_data.csv', index=False)
val_data.to_csv('val_data.csv', index=False)
test_data.to_csv('test_data.csv', index=False)

# Leer los archivos CSV
train_data = pd.read_csv('train_data.csv')
val_data = pd.read_csv('val_data.csv')
test_data = pd.read_csv('test_data.csv')

# Desempaquetar la columna 'energia_0' en columnas separadas
# Desempaquetar la columna 'energia_0' en columnas separadas
def unpack_energy_columns(df):
    energia_data = df['energia_0'].apply(pd.Series)
    max_length = len(energia_data.columns)
    energia_columns = ['energia_' + str(i) for i in range(max_length)]
    df[energia_columns] = energia_data
    df.drop(columns=['energia_0'], inplace=True)
    return df

train_data = unpack_energy_columns(train_data)
val_data = unpack_energy_columns(val_data)
test_data = unpack_energy_columns(test_data)

# División de características y etiquetas
X_train = train_data.drop(columns=['tempo', 'audio']).to_numpy()
y_train = train_data['tempo'].to_numpy()
X_val = val_data.drop(columns=['tempo', 'audio']).to_numpy()
y_val = val_data['tempo'].to_numpy()
X_test = test_data.drop(columns=['tempo', 'audio']).to_numpy()
y_test = test_data['tempo'].to_numpy()

# Crear modelo de red neuronal
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(1)
])

# Compilar el modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50, batch_size=32)

# Evaluar el modelo con datos de prueba
loss = model.evaluate(X_test, y_test)

print(f'Loss on test set: {loss}')

# Guardar el modelo entrenado
model.save('platform_generation_model.h5')