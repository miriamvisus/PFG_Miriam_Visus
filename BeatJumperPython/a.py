import librosa
import requests
import os
import tempfile


# Calcular duración máxima
def calculate_duration(git_repo_url, audio_folder, num_audios):
    base_url = git_repo_url.rstrip('/')  + '/raw/main'

    audio_path = f"{audio_folder}/Audio88.mp3"
    audio_url = f"{base_url}/{audio_path}"

    response_audio = requests.get(audio_url)

    if response_audio.status_code == 200:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio_file:
            temp_audio_file.write(response_audio.content)
            temp_audio_file.close()
            audio_file_path = temp_audio_file.name

            try:

                # Calcular la duración
                duration = librosa.get_duration(filename=audio_file_path)

                #  Actualizar la duración máxima
                print("Duración:", duration)


            finally:
                # Eliminar el archivo temporal después de usarlo
                os.unlink(audio_file_path)
    else:
        print(f"Failed to fetch audio from {audio_url}. Status code: {response_audio.status_code}")


    return duration

# Especifica los nombres de las carpetas y la cantidad de imágenes por carpeta en el repositorio Git
git_repo_url = 'https://github.com/miriamvisus/PFG_Miriam_Visus_Martin'
audio_folder = 'AUDIOS'
num_audios = 115

duration = calculate_duration(git_repo_url, audio_folder, num_audios)


import socket
import librosa
import numpy as np
import struct
import soundfile as sf
from pydub import AudioSegment
import time


# Dirección IP y puerto del servidor
HOST = '127.0.0.1'
RECEIVE_PORT = 8000
SEND_PORT = 8001

def receive_audio_data():
    try:

        # Crear un socket TCP/IP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Enlazar el socket a la dirección y puerto especificados
        server_socket.bind((HOST, RECEIVE_PORT))

        # Poner el socket en modo de escucha
        server_socket.listen(1)

        print(f"Servidor escuchando en {HOST}:{RECEIVE_PORT}")

        # Aceptar conexiones entrantes
        client_socket, client_address = server_socket.accept()

        print(f"Conexión establecida desde {client_address}")

        # Recibe el tamaño del archivo de audio
        size_bytes = b""
        while len(size_bytes) < 4:
            packet = client_socket.recv(4 - len(size_bytes))
            if not packet:
                raise Exception("No se recibieron datos")
            size_bytes += packet
        file_size = struct.unpack('I', size_bytes)[0]
        print("file size: ", file_size)

        # Recibe los datos de audio y reconstruye el archivo de audio
        audio_data = b""
        remaining_bytes = file_size
        while remaining_bytes > 0:
            packet = client_socket.recv(min(1024, remaining_bytes))
            if not packet:
                raise Exception("No se recibieron datos")
            audio_data += packet
            remaining_bytes -= len(packet)

        audio_array = np.frombuffer(audio_data, dtype=np.float32)

        samplerate = 44100

        # Guardar los datos de audio en formato WAV
        sf.write("output_audio.wav", audio_array, samplerate)

        # Convertir el archivo WAV a MP3
        audio = AudioSegment.from_wav("output_audio.wav")
        audio.export("output_audio.mp3", format="mp3")

        # Procesar los datos de audio
        tempo, energy = process_audio_data("output_audio.mp3")
        energy_length = energy.shape[1]
        print("Longitud de la energía:", energy_length)

        # Cierra la conexión
        client_socket.close()
        server_socket.close()

        return tempo, energy, energy_length

    except Exception as e:
        print(f"Error al recibir datos de audio: {e}")


def process_audio_data(audio_file):
    try:
        # Cargar los datos de audio utilizando librosa.load()
        y, sr = librosa.load(audio_file, sr=None)

        # Calcular el tempo
        tempo = librosa.beat.tempo(y=y, sr=sr)

        # Calcular la energía
        energy = librosa.feature.rms(y=y)

        print("Tempo:", tempo)
        print("Energía:", energy)

        return tempo, energy

    except Exception as e:
        print(f"Error al procesar datos de audio: {e}")


def send_data_to_unity(tempo, energy, energy_length):
    try:
        # Convertir la matriz de energía a una lista plana de valores flotantes
        energy_flat = energy.flatten().tolist()

        # Comprobar si energy contiene solo valores de punto flotante
        if all(isinstance(x, float) for x in energy_flat):
            # Crear un socket TCP/IP
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Conectar al servidor
            client_socket.connect((HOST, SEND_PORT))

            # Empaquetar los datos de tempo, longitud de energía y energía
            tempo_bytes = struct.pack('f', tempo)
            energy_length_bytes = struct.pack('I', energy_length)
            energy_format = f'{len(energy_flat)}f'
            energy_bytes = struct.pack(energy_format, *energy_flat)

            # Impresiones adicionales para verificar el flujo de datos
            print("Datos de tempo enviados:", tempo_bytes)
            print("Datos de longitud de energía enviados:", energy_length_bytes)
            print("Datos de energía enviados:", energy_bytes)

            # Enviar los datos de tempo, longitud de energía y energía
            client_socket.send(tempo_bytes)
            client_socket.send(energy_length_bytes)
            client_socket.send(energy_bytes)

            # Cerrar la conexión
            client_socket.close()
        else:
            raise ValueError("La lista 'energy' no contiene solo valores de punto flotante")

    except Exception as e:
        print(f"Error al enviar datos a Unity: {e}")


tempo, energy, energy_length = receive_audio_data()



import socket
import librosa
import numpy as np
import struct
import soundfile as sf
from pydub import AudioSegment

# Dirección IP y puerto del servidor
HOST = '127.0.0.1'
RECEIVE_PORT = 8000
SEND_PORT = 8001

def receive_audio_data():
    try:

        # Crear un socket TCP/IP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Enlazar el socket a la dirección y puerto especificados
        server_socket.bind((HOST, RECEIVE_PORT))

        # Poner el socket en modo de escucha
        server_socket.listen(1)

        print(f"Servidor escuchando en {HOST}:{RECEIVE_PORT}")

        # Aceptar conexiones entrantes
        client_socket, client_address = server_socket.accept()

        print(f"Conexión establecida desde {client_address}")

        # Recibe el tamaño del archivo de audio
        size_bytes = b""
        while len(size_bytes) < 4:
            packet = client_socket.recv(4 - len(size_bytes))
            if not packet:
                raise Exception("No se recibieron datos")
            size_bytes += packet
        file_size = struct.unpack('I', size_bytes)[0]
        print("file size: ", file_size)

        # Recibe los datos de audio y reconstruye el archivo de audio
        audio_data = b""
        remaining_bytes = file_size
        while remaining_bytes > 0:
            packet = client_socket.recv(min(1024, remaining_bytes))
            if not packet:
                raise Exception("No se recibieron datos")
            audio_data += packet
            remaining_bytes -= len(packet)

        audio_array = np.frombuffer(audio_data, dtype=np.float32)

        samplerate = 44100

        # Guardar los datos de audio en formato WAV
        sf.write("output_audio.wav", audio_array, samplerate)

        # Convertir el archivo WAV a MP3
        audio = AudioSegment.from_wav("output_audio.wav")
        audio.export("output_audio.mp3", format="mp3")

        # Procesar los datos de audio
        tempo, energy = process_audio_data("output_audio.mp3")
        energy_length = energy.shape[1]
        print("Longitud de la energía:", energy_length)

        # Cierra la conexión
        client_socket.close()
        server_socket.close()

        return tempo, energy, energy_length

    except Exception as e:
        print(f"Error al recibir datos de audio: {e}")


def process_audio_data(audio_file):
    try:
        # Cargar los datos de audio utilizando librosa.load()
        y, sr = librosa.load(audio_file, sr=None)

        # Calcular el tempo
        tempo = librosa.beat.tempo(y=y, sr=sr)

        # Calcular la energía
        energy = librosa.feature.rms(y=y)

        print("Tempo:", tempo)
        print("Energía:", energy)

        return tempo, energy

    except Exception as e:
        print(f"Error al procesar datos de audio: {e}")


def send_data_to_unity(tempo, energy, energy_length):
    try:
        # Convertir la matriz de energía a una lista plana de valores flotantes
        energy_flat = energy.flatten().tolist()

        # Comprobar si energy contiene solo valores de punto flotante
        if all(isinstance(x, float) for x in energy_flat):
            # Crear un socket TCP/IP
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Conectar al servidor
            client_socket.connect((HOST, SEND_PORT))

            # Empaquetar los datos de tempo, longitud de energía y energía
            tempo_bytes = struct.pack('f', tempo)
            energy_length_bytes = struct.pack('I', energy_length)
            energy_format = f'{len(energy_flat)}f'
            energy_bytes = struct.pack(energy_format, *energy_flat)

            # Impresiones adicionales para verificar el flujo de datos
            print("Datos de tempo enviados:", tempo_bytes)
            print("Datos de longitud de energía enviados:", energy_length_bytes)
            print("Datos de energía enviados:", energy_bytes)

            # Enviar los datos de tempo, longitud de energía y energía
            client_socket.send(tempo_bytes)
            client_socket.send(energy_length_bytes)
            client_socket.send(energy_bytes)

            # Cerrar la conexión
            client_socket.close()
        else:
            raise ValueError("La lista 'energy' no contiene solo valores de punto flotante")

    except Exception as e:
        print(f"Error al enviar datos a Unity: {e}")


tempo, energy, energy_length = receive_audio_data()
send_data_to_unity(tempo, energy, energy_length)

import socket
import librosa
import numpy as np
import struct
import soundfile as sf
from pydub import AudioSegment
import threading


def main():
    # Dirección IP y puerto del servidor
    HOST = '127.0.0.1'
    PORT = 8000

    # Crear un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Enlazar el socket a la dirección y puerto especificados
        server_socket.bind((HOST, PORT))

        # Poner el socket en modo de escucha
        server_socket.listen(1)

        print(f"Servidor escuchando en {HOST}:{PORT}")

        while True:
            # Aceptar conexiones entrantes
            client_socket, client_address = server_socket.accept()
            print(f"Conexión establecida desde {client_address}")

            # Iniciar un hilo para manejar la conexión con el cliente
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

    finally:
        # Cerrar la conexión del servidor
        server_socket.close()


def receive_audio_data(client_socket):
    try:

        # Recibe el tamaño del archivo de audio
        size_bytes = b""
        while len(size_bytes) < 4:
            packet = client_socket.recv(4 - len(size_bytes))
            if not packet:
                raise Exception("No se recibieron datos")
            size_bytes += packet
        file_size = struct.unpack('I', size_bytes)[0]
        print("file size: ", file_size)

        # Recibe los datos de audio y reconstruye el archivo de audio
        audio_data = b""
        remaining_bytes = file_size
        while remaining_bytes > 0:
            packet = client_socket.recv(min(1024, remaining_bytes))
            if not packet:
                raise Exception("No se recibieron datos")
            audio_data += packet
            remaining_bytes -= len(packet)

        audio_array = np.frombuffer(audio_data, dtype=np.float32)

        samplerate = 44100

        # Guardar los datos de audio en formato WAV
        sf.write("output_audio.wav", audio_array, samplerate)

        # Convertir el archivo WAV a MP3
        audio = AudioSegment.from_wav("output_audio.wav")
        audio.export("output_audio.mp3", format="mp3")

        # Procesar los datos de audio
        tempo, energy = process_audio_data("output_audio.mp3")
        energy_length = energy.shape[1]
        print("Longitud de la energía:", energy_length)

        return tempo, energy, energy_length

    except Exception as e:
        print(f"Error al recibir datos de audio: {e}")


def process_audio_data(audio_file):
    try:
        # Cargar los datos de audio utilizando librosa.load()
        y, sr = librosa.load(audio_file, sr=None)

        # Calcular el tempo
        tempo = librosa.beat.tempo(y=y, sr=sr)

        # Calcular la energía
        energy = librosa.feature.rms(y=y)

        print("Tempo:", tempo)
        print("Energía:", energy)

        return tempo, energy

    except Exception as e:
        print(f"Error al procesar datos de audio: {e}")


def send_data_to_unity(client_socket, tempo, energy, energy_length):
    try:
        # Convertir la matriz de energía a una lista plana de valores flotantes
        energy_flat = energy.flatten().tolist()

        # Comprobar si energy contiene solo valores de punto flotante
        if all(isinstance(x, float) for x in energy_flat):

            # Empaquetar los datos de tempo, longitud de energía y energía
            tempo_bytes = struct.pack('f', tempo)
            energy_length_bytes = struct.pack('I', energy_length)
            energy_format = f'{len(energy_flat)}f'
            energy_bytes = struct.pack(energy_format, *energy_flat)

            # Impresiones adicionales para verificar el flujo de datos
            print("Datos de tempo:", tempo_bytes)
            print("Datos de longitud de energía:", energy_length_bytes)
            print("Datos de energía:", energy_bytes)

            # Enviar los datos de tempo, longitud de energía y energía
            client_socket.send(tempo_bytes)
            client_socket.send(energy_length_bytes)
            client_socket.send(energy_bytes)

            print("Datos enviados a Unity")

            # Cerrar la conexión del cliente
            client_socket.close()

        else:
            raise ValueError("La lista 'energy' no contiene solo valores de punto flotante")

    except Exception as e:
        print(f"Error al enviar datos a Unity: {e}")

def handle_client(client_socket):
    try:
        # Lógica para manejar la conexión con el cliente
        tempo, energy, energy_length = receive_audio_data(client_socket)
        send_data_to_unity(client_socket, tempo, energy, energy_length)
    finally:
        # Cerrar la conexión del cliente
        client_socket.close()

if __name__ == "__main__":
    main()

