from pedalboard import Pedalboard, PitchShift, HighShelfFilter, LowShelfFilter, Distortion
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

        # utworzenie pedalboarda podnoszącego wysokość głosu
        if preset == "Test":
            board = Pedalboard([PitchShift(semitones=kwargs.get("semitones")),
                                HighShelfFilter(cutoff_frequency_hz=kwargs.get("cutoff_freq_hz"),
                                                gain_db=kwargs.get("gain_db"))])
        elif preset == "Tomek":
            board = Pedalboard([LowShelfFilter(cutoff_frequency_hz=kwargs.get("cutoff_freq_hz"),
                                               gain_db=kwargs.get("gain_db"),
                                               q=kwargs.get("gain_db")),
                                Distortion(drive_db=kwargs.get("drive_db")),
                                PitchShift(semitones=kwargs.get("semitones"))])

        # zastosowanie wczytanych efektów na wybranym pliku
        effected = board(audio, samplerate)

        # zapisanie zmodulowanego pliku
        with AudioFile("pedalboard-processed-output.wav", "w", samplerate, effected.shape[0]) as f:
            f.write(effected)

    # wykorzystanie pitch shiftera z biblioteki praat-parselmouth
    def praat_manipulation(self, **kwargs):
        sound = parselmouth.Sound(self.Filename)
        factor = 1.5
        manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
        pitch_tier = call(manipulation, "Extract pitch tier")
        call(pitch_tier, "Multiply frequencies", sound.xmin, sound.xmax, factor)
        call([pitch_tier, manipulation], "Replace pitch tier")
        sound_up = call(manipulation, "Get resynthesis (overlap-add)")
        sound_up.save("praat-processed-output.wav", "WAV")