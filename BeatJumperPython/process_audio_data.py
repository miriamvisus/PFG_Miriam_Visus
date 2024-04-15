import librosa
import numpy as np
import scipy.signal as signal

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


if __name__ == "__main__":
    # Procesar los datos de audio
    audio = "C:\\Users\\miria.PORMIR\\PFG_Miriam_Visus_Martin\\BeatJumperUnity\\Assets\\Audios\\Boogie Party.mp3"
    tempo, energy = process_audio_data(audio)