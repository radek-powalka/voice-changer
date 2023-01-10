from microRecorder import MicroRecorder
from voiceChanger import VoiceChanger
from plotter import Plotter
from os import path
import matplotlib.pyplot as plt
# from run_tts import get_tts

# wybór pliku audio
print("Audio sources:")
audio_sources = ["Existing file", "Record", "Text to speech (only Polish language is supported)"]

for index, source in enumerate(audio_sources):
    print(f"[{index}] {source}")

while True:
    source = input("Choose audio source: ")
    if source == "0":
        while True:
            fname = input("Path: ")
            if path.exists(fname) & fname.endswith(".wav") or fname.endswith(".mp3") is True:
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

    # elif source == "2":
    #     user_text = input("Type your text: ")
    #     get_tts(user_text)
    #     voiceChanger = VoiceChanger("TTS_PL.wav")
    #     break

# wybór biblioteki, która zmodyfikuje nagranie
manipulation_options = ["Pedalboard (offers a handful of effects, but has only a naive pitch shift functionality)",
                        "Praat (offers more advanced pitch shifter, but has no other effects)"]

for index, option in enumerate(manipulation_options):
    print(f"[{index}] {option}")

while True:
    manipulation = input("Choose a package: ")

    # wybór ustawień przygotowanych dla biblioteki Pedalboard wg których nagranie zostanie zmodyfikowane
    if manipulation == "0":
        print("Presets available for Pedalboard:")
        pedalboard_presets = ["Test", "Anonymous TV speaker", "Child (with reverb)"]

        for index, preset in enumerate(pedalboard_presets):
            print(f"[{index}] {preset}")

        while True:
            preset = input("Choose a preset: ")
            if preset == "0":
                voiceChanger.pedalboard_manipulation("Test", semitones_test=4, cutoff_freq_hz=300,
                                                     gain_db=6)
                break
            elif preset == "1":
                voiceChanger.pedalboard_manipulation("Anonymous TV speaker", semitones=-1, cutoff_freq_hz=300, gain_db=7,
                                                     q=1.5, drive_db=3)
                break
            elif preset == "2":
                voiceChanger.pedalboard_manipulation("Child", semitones_child=4, room_size=0.6)
                break

        processed_fname = "pedalboard-processed-output.wav"
        break

    # wybór ustawień przygotowanych dla biblioteki praat-parselmouth wg których nagranie zostanie zmodyfikowane
    elif manipulation == "1":
        print("Presets available for Praat:")
        praat_presets = ["Male", "Female", "User's preset"]

        for index, preset in enumerate(praat_presets):
            print(f"[{index}] {preset}")

        while True:
            preset = input("Choose a preset: ")

            if preset == "0":
                voiceChanger.praat_manipulation("Male")
                break
            elif preset == "1":
                voiceChanger.praat_manipulation("Female")
                break
            elif preset == "2":  # modyfikacja nagrania wg ustawień użytkownika
                while True:
                    try:
                        user_factor = float(input("Factor: "))
                        voiceChanger.praat_manipulation("User", factor=user_factor)
                        break
                    except ValueError:
                        print("Your input must be a number")
                break

        processed_fname = "praat-processed-output.wav"
        break

# stworzenie spektrogramów oryginalnego i zmodyfikowanego nagrania
original_audio_spec = Plotter(fname)
original_audio_spec.draw_pitch("Original audio spectrogram")
processed_audio_spec = Plotter(processed_fname)
processed_audio_spec.draw_pitch("Processed audio spectrogram")
plt.show()

print("Done!")
