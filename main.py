import matplotlib.pyplot as plt
import numpy as np
from pedalboard import Pedalboard, PitchShift
from pedalboard.io import AudioFile
from scipy import signal, fftpack


def spec(sig, fs):
    tstep = 1 / fs
    f, t, spec = signal.spectrogram(sig[0], fs, window="hamm", nperseg=int(0.02 / tstep))
    plt.pcolormesh(t, f, spec, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()


with AudioFile('Tomasz_Piwowarski.wav') as f:
    audio = f.read(f.frames)
    samplerate = f.samplerate

board = Pedalboard([PitchShift(semitones=12)])

effected = board(audio, samplerate)

with AudioFile('processed-output.wav', 'w', samplerate, effected.shape[0]) as f:
    f.write(effected)

spec(audio, samplerate)
spec(effected, samplerate)