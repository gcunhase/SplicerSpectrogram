
from splicer_spectrogram import SplicerSpectrogram
from timeit import default_timer as timer

__author__ = "Gwena Cunha"


if __name__ == "__main__":

    # Settings
    time = timer()
    data_dir = "assets"
    results_dir = data_dir + "_splices"
    specs_dir = data_dir + "_specs"
    splicerSpectrogram = SplicerSpectrogram(extension=".mp3")

    # Splice audios
    splicerSpectrogram.splice_audio_files(data_dir, results_dir, chunk_length_ms=3000)

    # Audios spectrogram
    splicerSpectrogram.audio_spectrograms(results_dir, specs_dir, spec_type="log_power")

    # Time program ran for
    print("\nProgram ran for: %.2f seconds\n" % (timer()-time))
