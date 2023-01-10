import struct
import wave
import keyboard
from pvrecorder import PvRecorder


class MicroRecorder:

	Audio = []
	DeviceIndex = 0 # indeks urządzenia, które zostanie użyte do nagrywania
	Filename = None

	def __init__(self, filename):
		self.Filename = filename

	def check_devices(self):
		print("List of your recording devices:")
		for index, device in enumerate(PvRecorder.get_audio_devices()):
			print(f"[{index}] {device}")
		idx = input("Choose a recording device: ")
		self.DeviceIndex = int(idx)

	def record(self):
		filename = self.Filename + ".wav"
		pvr = PvRecorder(device_index=self.DeviceIndex,  frame_length=1024)
		pvr.start()
		print("Recording... (press space to stop)")
		while True:
			frame = pvr.read()
			self.Audio.extend(frame)
			if keyboard.is_pressed("space"):
				pvr.stop()
				break
		print("Done!")
		pvr.stop()

		with wave.open(filename, 'w') as f:
			f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
			f.writeframes(struct.pack("h" * len(self.Audio), *self.Audio))
		pvr.delete()

		return filename
