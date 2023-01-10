from pedalboard import Pedalboard, PitchShift, HighShelfFilter, LowShelfFilter, Distortion, Reverb
from pedalboard.io import AudioFile
import parselmouth
from parselmouth.praat import call


class VoiceChanger:

    Filename = None

    def __init__(self, filename):
        self.Filename = filename

    def pedalboard_manipulation(self, preset, **kwargs):
        # wczytanie pliku audio
        with AudioFile(self.Filename) as f:
            audio = f.read(f.frames)
            samplerate = f.samplerate

        # utworzenie pedalboarda dla wybranego presetu
        if preset == "Test":
            board = Pedalboard([PitchShift(semitones=kwargs.get("semitones_test")),
                                HighShelfFilter(cutoff_frequency_hz=kwargs.get("cutoff_freq_hz"),
                                                gain_db=kwargs.get("gain_db"))])
        elif preset == "Anonymous TV speaker":
            board = Pedalboard([LowShelfFilter(cutoff_frequency_hz=kwargs.get("cutoff_freq_hz"),
                                               gain_db=kwargs.get("gain_db"),
                                               q=kwargs.get("gain_db")),
                                Distortion(drive_db=kwargs.get("drive_db")),
                                PitchShift(semitones=kwargs.get("semitones"))])
        elif preset == "Child":
            board = Pedalboard([PitchShift(semitones=kwargs.get("semitones_child")),
                                Reverb(room_size=kwargs.get("room_size"))])

        # zastosowanie wczytanych efektów na wybranym pliku
        effected = board(audio, samplerate)

        # zapisanie zmodulowanego pliku
        with AudioFile("pedalboard-processed-output.wav", "w", samplerate, effected.shape[0]) as f:
            f.write(effected)

    # wykorzystanie pitch shiftera z biblioteki praat-parselmouth
    def praat_manipulation(self, preset, **kwargs):
        sound = parselmouth.Sound(self.Filename)

        if preset == "Male":
            factor = 0.6
        elif preset == "Female":
            factor = 1.75
        elif preset == "User":
            factor = kwargs.get("factor")

        manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
        pitch_tier = call(manipulation, "Extract pitch tier")
        call(pitch_tier, "Multiply frequencies", sound.xmin, sound.xmax, factor)
        call([pitch_tier, manipulation], "Replace pitch tier")
        sound_up = call(manipulation, "Get resynthesis (overlap-add)")
        sound_up.save("praat-processed-output.wav", "WAV")