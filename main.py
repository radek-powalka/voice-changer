from microRecorder import MicroRecorder
from voiceChanger import VoiceChanger
from plotter import Plotter
from os import path
import matplotlib.pyplot as plt
from run_tts import get_tts


print("Audio sources:")
audio_sources = ["Existing file", "Record", "Text to speech (only polish language is supported)"]

for index, source in enumerate(audio_sources):
    print(f"[{index}] {source}")

while True:
    source = input("Choose audio source: ")
    if source == "0":
        while True:
            fname = input("Path: ")
            if fname.endswith(".wav") & path.exists(fname) is True:
                break
            else:
                print("Wrong path")

        voiceChanger = VoiceChanger(fname)
        break

    elif source == "1":
        recorder = MicroRecorder("recorded-voice")
        recorder.check_devices()
        fname = recorder.record()
        voiceChanger = VoiceChanger(fname)
        break

    elif source == "2":
        user_text = input("Type your text: ")
        get_tts(user_text)
        voiceChanger = VoiceChanger("TTS_PL.wav")
        break

manipulation_options = ["Pedalboard (offers a handful of effects, but has only a naive pitch shift functionality",
                        "Praat (offers more advanced pitch shifter, but no other effects"]

for index, option in enumerate(manipulation_options):
    print(f"[{index}] {option}")

while True:
    manipulation = input("Choose a package: ")

    if manipulation == "0":
        print("Presets available for Pedalboard:")
        pedalboard_presets = ["1. Test", "2. Tomek"]

        for index, preset in enumerate(pedalboard_presets):
            print(f"[{index}] {preset}")

        while True:
            preset = input("Choose a preset: ")
            if preset == "0":
                voiceChanger.pedalboard_manipulation("Test", semitones=4, cutoff_freq_hz=300,
                                                     gain_db=6)
                break
            elif preset == "1":
                voiceChanger.pedalboard_manipulation("Tomek", semitones=-1, cutoff_freq_hz=300, gain_db=7,
                                                     q=1.5, drive_db=3)
                break

        processed_fname = "pedalboard-processed-output.wav"
        break

    elif manipulation == "1":
        voiceChanger.praat_manipulation()
        processed_fname = "praat-processed-output.wav"
        break

original_audio_spec = Plotter(fname)
original_audio_spec.draw_pitch("Original audio spectrogram")
processed_audio_spec = Plotter(processed_fname)
processed_audio_spec.draw_pitch("Processed audio spectrogram")
plt.show()
print("Done!")
