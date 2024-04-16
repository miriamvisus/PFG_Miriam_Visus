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

