import socket
import librosa
import numpy as np

HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 8888         # Puerto en el que el servidor estará escuchando

def receive_audio_data():
    # Crea un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enlaza el socket a la dirección y puerto especificados
    server_socket.bind((HOST, PORT))

    # Pone el socket en modo de escucha
    server_socket.listen(1)

    print(f"Servidor escuchando en {HOST}:{PORT}")

    # Acepta conexiones entrantes
    client_socket, client_address = server_socket.accept()

    print(f"Conexión establecida desde {client_address}")

    # Recibe los datos de audio de Unity
    audio_data = client_socket.recv(1024)

    # Procesa los datos de audio
    processed_data = process_audio_data(audio_data)

    # Cierra los sockets
    client_socket.close()
    server_socket.close()

def process_audio_data(audio_data):
    # Convierte los datos de audio en un array NumPy
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    # Calcula la tasa de muestreo (samplerate) adecuada para librosa
    samplerate = 44100  # Suponiendo una tasa de muestreo de 44100 Hz

    # Analiza el audio utilizando librosa para extraer características
    tempo, beat_frames = librosa.beat.beat_track(y=audio_array, sr=samplerate)
    energy = np.mean(librosa.feature.rms(y=audio_array))

    # Aquí puedes hacer más procesamiento de los datos según tus necesidades

    # Devuelve los resultados del análisis
    return tempo, energy

if __name__ == "__main__":
    receive_audio_data()

