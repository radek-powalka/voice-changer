import matplotlib.pyplot as plt
import numpy as np
from pedalboard import Pedalboard, PitchShift, HighpassFilter
from pedalboard.io import AudioFile
from scipy import signal, fftpack


# funkcja tworząca spektrogram
def spec(sig, fs):
    f, t, spec = signal.spectrogram(sig[0], fs, window="hamm", nperseg=int(0.05 * fs))
    plt.pcolormesh(t, f, 20*np.log10(abs(spec)), shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()


# wczytanie pliku audio
with AudioFile('Tomasz_Piwowarski.wav') as f:
    audio = f.read(f.frames)
    samplerate = f.samplerate

# utworzenie pedalboarda podnoszącego wysokość głosu
board = Pedalboard([PitchShift(semitones=4), HighpassFilter(cutoff_frequency_hz=450)])

# zastosowanie wczytanych efektów na wybranym pliku
effected = board(audio, samplerate)

# zapisanie zmodulowanego pliku
with AudioFile('processed-output.wav', 'w', samplerate, effected.shape[0]) as f:
    f.write(effected)

# wyświetlenie spektrogramów
spec(audio, samplerate)
spec(effected, samplerate)
