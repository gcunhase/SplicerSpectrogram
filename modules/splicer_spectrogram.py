
import os
import utils
from pydub import AudioSegment
from pydub.utils import make_chunks
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

__author__ = "Gwena Cunha"


class SplicerSpectrogram:

    def __init__(self, extension=".wav"):
        """ Initialize class

        :param extension: audio file extension: .wav, .mp3, .flac
        """

        print("Initialize SplicerSpectrogram")
        self.project_dir = utils.project_dir_name()
        self.extension = extension

    def splice_audio_files(self, data_dir, results_dir, chunk_length_ms=3000):
        """ Checks data directory and collects all audios with specified extension to splice

        :param data_dir: data directory
        :param results_dir: results directory
        :param chunk_length_ms: length of audio chunk in milliseconds
        :return:
        """
        # Find all files in data directory with specific extension
        files = [f for f in os.listdir(self.project_dir + data_dir) if f.endswith(self.extension)]

        # Splice audio, length of splice in ms
        print("\nSplicing audios...")
        for f in files:
            print(f)
            self.splice_single_audio(data_dir, results_dir, f, chunk_length_ms)

    def splice_single_audio(self, data_dir, results_dir, filename, chunk_length_ms=3000):
        """ Splices single audio into segments of specific length or less

        :param data_dir: data directory
        :param results_dir: results directory
        :param filename: name of file to be spliced
        :param chunk_length_ms: length of audio chunk in milliseconds
        :return:
        """

        file_path = data_dir+"/"+filename

        # Create new file if not existent
        file_path_new = results_dir+"/"
        if not os.path.exists(file_path_new):
            os.makedirs(file_path_new)

        # Make chunks of length chunk_length_ms
        audio = AudioSegment.from_file(file_path)
        chunks = make_chunks(audio, chunk_length_ms)

        # Export all of the individual chunks as wav files
        for i, chunk in enumerate(chunks):
            chunk_name = file_path_new+filename.split(self.extension)[0]+"_chunk{0}".format(i)+self.extension
            print "exporting", chunk_name
            chunk.export(chunk_name, format=self.extension.split(".")[1])

    def audio_spectrograms(self, splices_dir, specs_dir, spec_type="log_power"):
        """ Get audio's spectrogram

        :param splices_dir: directory of spliced audio files
        :param specs_dir: directory of audios' spectrogram
        :param spec_type: type of spectrogram
        :return: directory for final spectrograms
        """

        # Gets relative path of list of files
        print("\nRetrieving audio files...")
        files_audio = [f for f in os.listdir(self.project_dir + splices_dir) if f.endswith(self.extension)]

        # Gets new path for results and creates it if not existent
        spectrograms_dir = self.project_dir + specs_dir + "/"
        print("Spectrograms will be saved in: " + spectrograms_dir)
        if not os.path.exists(spectrograms_dir):
            os.makedirs(spectrograms_dir)

        # Obtaining spectrograms
        print("Obtaining spectrograms...")
        for file_audio in files_audio:
            print file_audio
            audio_path = splices_dir + "/" + file_audio
            self.get_spectrogram(audio_path, spec_type, spectrograms_dir)

        return spectrograms_dir

    def get_spectrogram(self, audio_filename, spec_type, output_dir):
        """ Gets audio chromagram and saves it without borders or tile, just content

        Source: https://librosa.github.io/librosa/generated/librosa.display.specshow.html
        Note:
            librosa.core.stft(y, n_fft=2048, hop_length=None, win_length=None, window='hann', center=True,
             dtype=<class 'numpy.complex64'>, pad_mode='reflect')[source]

        :param audio_filename: audio filename
        :param spec_type: type of spectrogram. Types = ["linear", "linear_grayscale", "log_power"]
        :param output_dir: directory to output spectrograms
        :return: spectrogram
        """

        # Load audio file
        y, sr = librosa.load(audio_filename, sr=None)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # Calculate spectrogram
        D = librosa.stft(y)
        D_stft = librosa.amplitude_to_db(D, ref=np.max)
        D_stft = np.array(D_stft, np.float32)

        # Finish calculating spectrogram depending on desired typ
        spectrogram = None
        if "linear" in spec_type:
            spectrogram = D_stft
            librosa.display.specshow(spectrogram, sr=sr)
            plt.colorbar(format='%+2.0f dB')
            plt.title('Linear-frequency power spectrogram')
        elif "linear_grayscale" in spec_type:
            spectrogram = D_stft
            librosa.display.specshow(spectrogram, cmap='gray_r', y_axis='linear', sr=sr)
            plt.colorbar(format='%+2.0f dB')
            plt.title('Linear power spectrogram (grayscale)')
        elif "log_power" in spec_type:
            spectrogram = D_stft
            librosa.display.specshow(spectrogram, x_axis='time', y_axis='log', sr=sr)
            plt.colorbar(format='%+2.0f dB')
            plt.title('Log power spectrogram')
        else:
            print("Spectrogram type not defined")

        # Save image without frames, only content
        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        plt.axis("off")
        spec_filename = audio_filename.split(self.extension)[0]
        spec_filename = spec_filename.split("/")[-1]
        plt.savefig(output_dir + spec_filename + "_" + spec_type + '.png', bbox_inches=extent)
        # plt.show()
        plt.close()
        return spectrogram
