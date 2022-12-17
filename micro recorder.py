import struct
import wave
from pvrecorder import  PvRecorder

# ==== SPRAWDZ JAKIE MASZ URZADZENIA I WYBIERZ POTEM Z KTOREGO CHCESZ KORZYSTAC ====

#for index, device in enumerate(PvRecorder.get_audio_devices()):
	#print(f"[{index}] {device}")


# ==== NAGRYWANIE AUDIO ====

audio = []
pvr = PvRecorder(device_index=2, frame_length=1024) #Device_index jest ID urzadzenia ktory bedzie uzywane do nagrywania
smpl_rt=44100
seconds=2.5 #czas ustawiony tutaj jest okolo dwa razy mniejszy niz faktyczny czas nagrywania
filename = "recorded.wav"

#Nagrywanie dzwieku przez okolo 5 sekund
pvr.start()
print("Recording...")
for i in range(0, int(smpl_rt / pvr._frame_length * seconds)):
	frame=pvr.read()
	audio.extend(frame)

print("Done!")
pvr.stop()

# ==== ZAPIS NAGRANIA JAKO PLIK .WAV ====

with wave.open(filename,'w') as f:
	f.setparams((1,2,16000,512,"NONE","NONE"))
	f.writeframes(struct.pack("h"*len(audio),*audio))
pvr.delete()