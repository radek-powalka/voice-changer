import matplotlib.pyplot as plt
import numpy as np
import parselmouth


# klasa zawierająca metody tworzące wykresy pomocne w analizie głosu
class Plotter:
    Snd = None
    Spectrogram = None
    Intensity = None
    Pitch = None

    def __init__(self, filename):
        self.Snd = parselmouth.Sound(filename)
        self.Spectrogram = self.Snd.to_spectrogram()
        self.Intensity = self.Snd.to_intensity()
        self.Pitch = self.Snd.to_pitch()

    # rysowanie spektrogramu
    def draw_spectrogram(self, dynamic_range=70):
        fig = plt.figure()
        spectrogram = self.Spectrogram
        x, y = spectrogram.x_grid(), spectrogram.y_grid()
        sg_db = 10 * np.log10(spectrogram.values)
        plt.pcolormesh(x, y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
        plt.ylim([spectrogram.ymin, spectrogram.ymax])
        plt.xlabel("Czas [s]")
        plt.ylabel("Częstotliwość [Hz]")
        return fig

    # rysowanie przebiegu natężenia
    def draw_intensity(self):
        fig = self.draw_spectrogram()
        plt.twinx()
        plt.plot(self.Intensity.xs(), self.Intensity.values.T, linewidth=3, color='w')
        plt.plot(self.Intensity.xs(), self.Intensity.values.T, linewidth=1)
        plt.grid(False)
        plt.ylim(0)
        plt.ylabel("Natężenie [dB]")
        plt.xlim([self.snd.xmin, self.snd.xmax])
        return fig

    # rysowanie częstotliwości podstawowej głosu
    def draw_pitch(self):
        fig = self.draw_spectrogram()
        pitch_values = self.Pitch.selected_array['frequency']  # pobranie przebiegu f0
        pitch_values[pitch_values == 0] = np.nan  # zastąpienie fragmentów bez głosu wartościami NaN
        plt.twinx()
        plt.plot(self.Pitch.xs(), pitch_values, 'o', markersize=5, color='w')
        plt.plot(self.Pitch.xs(), pitch_values, 'o', markersize=2)
        plt.grid(False)
        plt.ylim(0, self.Pitch.ceiling)
        plt.ylabel("Częstotliwość podstawowa [Hz]")
        return fig
