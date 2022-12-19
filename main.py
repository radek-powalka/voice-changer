import matplotlib.pyplot as plt
import numpy as np
from pedalboard import Pedalboard, PitchShift, HighShelfFilter
from pedalboard.io import AudioFile
import parselmouth
from parselmouth.praat import call
from plotter import Plotter


# wczytanie pliku audio
with AudioFile("Tomasz_Piwowarski.wav") as f:
    audio = f.read(f.frames)
    samplerate = f.samplerate

# utworzenie pedalboarda podnoszącego wysokość głosu
board = Pedalboard([PitchShift(semitones=4), HighShelfFilter(cutoff_frequency_hz=300, gain_db=6)])

# zastosowanie wczytanych efektów na wybranym pliku
effected = board(audio, samplerate)

# zapisanie zmodulowanego pliku
with AudioFile("processed-output1.wav", "w", samplerate, effected.shape[0]) as f:
    f.write(effected)


# wykorzystanie pitch shiftera z biblioteki praat-parselmouth
sound = parselmouth.Sound("Tomasz_Piwowarski.wav")
factor = 1.25
manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
pitch_tier = call(manipulation, "Extract pitch tier")
call(pitch_tier, "Multiply frequencies", sound.xmin, sound.xmax, factor)
call([pitch_tier, manipulation], "Replace pitch tier")
sound_up = call(manipulation, "Get resynthesis (overlap-add)")
sound_up.save("processed-output2.wav", "WAV")


# porównanie nagrań zmodyfikowanych za pomocą biblioteki Pedalboard
pedalboard_analysis = Plotter("processed-output1.wav")
pedalboard_analysis.draw_intensity()
pedalboard_analysis.draw_pitch()
praat_analysis = Plotter("processed-output2.wav")
praat_analysis.draw_intensity()
praat_analysis.draw_pitch()
plt.show()
