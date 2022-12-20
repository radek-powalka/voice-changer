from playsound import playsound
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import os
import wave
import random
from pedalboard.io import AudioFile
from pedalboard import Pedalboard, Chorus, Delay, Distortion, LowShelfFilter, HighShelfFilter, Phaser, PitchShift

# with AudioFile('Tomasz_Piwowarski.wav') as f:
#   audio = f.read(f.frames)
#   samplerate = f.samplerate
#
# def spec(sig,fs):
#   f, t, spec = signal.spectrogram(sig[0], fs, window='hamm', nperseg=int(0.05*fs))
#   plt.pcolormesh(t, f, 20*np.log10(np.abs(spec)), shading='gouraud')
#   plt.ylabel('Frequency [Hz]')
#   plt.xlabel('Time [s]')
#   plt.show()

#playsound('Tomasz_Piwowarski.wav')

#board = Pedalboard([Chorus(rate_hz=1,depth=0.5,centre_delay_ms=9,feedback=0.4,mix=0.7)])
#board = Pedalboard([Delay(delay_seconds=0.1,feedback=0.2,mix=0.5)])
#board = Pedalboard([Distortion(drive_db=20)])
#board = Pedalboard([LowShelfFilter(cutoff_frequency_hz=800, gain_db=20, q=0.7),
 #                   HighShelfFilter(cutoff_frequency_hz=5000, gain_db=20, q=0.7)])
#board=Pedalboard([Chorus(rate_hz=1,depth=0.8,centre_delay_ms=9,feedback=0.5,mix=0.7), Delay(delay_seconds=0.1,feedback=0.3,mix=0.8), LowShelfFilter(cutoff_frequency_hz=400, gain_db=6, q=0.7),Phaser(rate_hz=2,depth=1.2,centre_frequency_hz=1500,feedback=0.3,mix=1),Distortion(drive_db=-3), PitchShift(semitones=-2)])
#board=Pedalboard([Phaser(rate_hz=1,depth=0.9,centre_frequency_hz=1300,feedback=0.5,mix=1),Distortion(drive_db=5)])

# effected = board(audio, samplerate)
#
# with AudioFile('processed-output.wav', 'w', samplerate, effected.shape[0]) as f:
#   f.write(effected)

def pitchshift_test_generator(file_name):
  # Wczytanie nagrania i przepuszczenie go przez 11 PitchShiftów
  i_list=[]
  infiles=[]
  for i in range (-5,6):
    i_list.append(i)
    with AudioFile(file_name) as f:
      audio = f.read(f.frames)
      samplerate = f.samplerate
    board = Pedalboard([PitchShift(semitones=i)])
    effected = board(audio, samplerate)
    with AudioFile('processed-output'+str(i)+'.wav', 'w', samplerate, effected.shape[0]) as f:
      f.write(effected)

  # Przetasowanie nagrań i złączenie ich w jedno
  random.shuffle(i_list)
  for numb in i_list:
    infiles.append('processed-output'+str(numb)+'.wav')
  outfile = 'processed-'+file_name
  data = []
  for infile in infiles:
    w = wave.open(infile, 'rb')
    data.append([w.getparams(), w.readframes(w.getnframes())])
    w.close()

  output = wave.open(outfile, 'wb')
  output.setparams(data[0][0])
  for i in range(len(data)):
    output.writeframes(data[i][1])
  output.close()

  #Zapis użytych pitchshiftów w kolejności
  file = open('order_of_semitones.txt', 'w')
  for i in i_list:
    file.write(str(i) + "\n")
  file.close()

  #Skasowanie niepotrzebnych nagrań
  for infile in infiles:
    os.remove(infile)




pitchshift_test_generator('Tomasz_Piwowarski.wav')


# playsound('processed-output.wav')

# spec(effected,samplerate)
