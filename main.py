from microRecorder import MicroRecorder
from voiceChanger import VoiceChanger
from run_tts import get_tts

pedalboard_test = {
    "semitones": 4,
    "cutoff_freq_hz": 300,
    "gain_db": 6
}

pedalboard_tomek = {
    "cutoff_freq_hz": 300,
    "gain_db": 7,
    "q": 1.5,
    "drive_db": 3,
    "semitones": -12
}

print("Audio sources:")
audio_sources = ["1. Existing file", "2. Record", "3. TTS"]
print(audio_sources)
while True:
    source = input("Choose audio source: ")
    if source == "1":
        while True:
            fname = input("Path: ")
            if fname.endswith(".wav"):
                break
            print("Choose .wav file")
        voiceChanger = VoiceChanger(fname)
        break

    elif source == "2":
        recorder = MicroRecorder("RecordedVoice")
        recorder.check_devices()
        fname = recorder.record()
        voiceChanger = VoiceChanger(fname)
        break

    elif source == "3":
        user_text = input("Type your text: ")
        get_tts(user_text)
        voiceChanger = VoiceChanger("TTS_PL.wav")
        break

manipulation_options = ["1. Pedalboard", "2. Praat"]
print(manipulation_options)
while True:
    manipulation = int(input("Choose a package: "))

    if manipulation == 1:
        print("Presets available for Pedalboard:")
        pedalboard_presets = ["1. Test", "2. Tomek"]
        print(pedalboard_presets)
        while True:
            preset = int(input("Choose a preset: "))
            if preset == 1:
                voiceChanger.pedalboard_manipulation("Test", semitones=pedalboard_test["semitones"],
                                                     cutoff_freq_hz=pedalboard_test["cutoff_freq_hz"],
                                                     gain_db=pedalboard_test["gain_db"])
                break
            elif preset == 2:
                voiceChanger.pedalboard_manipulation("Tomek", semitones=pedalboard_tomek["semitones"],
                                                     cutoff_freq_hz=pedalboard_tomek["cutoff_freq_hz"],
                                                     gain_db=pedalboard_tomek["gain_db"],
                                                     q=pedalboard_tomek["q"],
                                                     drive_db=pedalboard_tomek["drive_db"])
                break
        break
    elif manipulation == 2:
        voiceChanger.praat_manipulation()
        break


# def voice_changer(function, preset, txt):
#     elif function == "record":
#         # Radek tu wklei funkcję do nagrywania
#     board=pedalboard(preset)

#
#
# porównanie nagrań zmodyfikowanych za pomocą biblioteki Pedalboard
# pedalboard_analysis = Plotter("processed-output1.wav")
# pedalboard_analysis.draw_intensity()
# pedalboard_analysis.draw_pitch()
# praat_analysis = Plotter("ass.wav")
# praat_analysis.draw_intensity()
# praat_analysis.draw_pitch()
# plt.show()
