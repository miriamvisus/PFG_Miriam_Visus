import socket
import librosa
import numpy as np
import scipy.signal as signal
import struct
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment

# Dirección I-P y puerto del servidor
HOST = '127.0.0.1'
PORT = 8888


def receive_audio_data():
    try:

        # Crear un socket TCP/IP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Enlazar el socket a la dirección y puerto especificados
        server_socket.bind((HOST, PORT))

        # Poner el socket en modo de escucha
        server_socket.listen(1)

        print(f"Servidor escuchando en {HOST}:{PORT}")

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

        # Reproduce el audio
        sd.play(audio_array, samplerate=44100, blocking=True)

        # Guardar los datos de audio en formato WAV
        sf.write("output_audio.wav", audio_array, samplerate)

        # Convertir el archivo WAV a MP3
        audio = AudioSegment.from_wav("output_audio.wav")
        audio.export("output_audio.mp3", format="mp3")

        # Procesar los datos de audio
        tempo, energy = process_audio_data("output_audio.mp3")

        # Cierra la conexión
        client_socket.close()
        server_socket.close()

        return tempo, energy

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

def send_data_to_unity(tempo, energy):
    try:
        # Crear un socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conectar al servidor
        client_socket.connect((HOST, PORT))

        # Empaquetar los datos de tempo y energía
        tempo_bytes = struct.pack('f', tempo)
        energy_bytes = struct.pack(f'{len(energy)}f', *energy)

        # Enviar los datos de tempo y energía
        client_socket.send(tempo_bytes)
        client_socket.send(energy_bytes)

        # Cerrar la conexión
        client_socket.close()

    except Exception as e:
        print(f"Error al enviar datos a Unity: {e}")

tempo, energy = receive_audio_data()
send_data_to_unity(tempo, energy)
