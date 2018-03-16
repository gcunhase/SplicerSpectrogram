
from splicer_spectrogram import SplicerSpectrogram
from timeit import default_timer as timer
import argparse

__author__ = "Gwena Cunha"


def main():
    print("Main")

if __name__ == "__main__":
    # argparse
    parser = argparse.ArgumentParser(description='SplicerSpectrogram')
    parser.add_argument('--data_dir', type=str, default='assets', help='Directory with audio data.')
    parser.add_argument('--splices_dir', type=str, default='assets_splices',
                        help='Directory where audio splices will be saved.')
    parser.add_argument('--specs_dir', type=str, default='assets_specs',
                        help='Directory where audio spectrograms will be saved.')
    parser.add_argument('--chunk_length_ms', type=int, default=3000, help='Length of audio chunks in ms.')
    parser.add_argument('--extension', type=str, default='mp3', help='Audio file extension.')
    parser.add_argument('--spec_type', type=str, default='log_power',
                        help='Spectrogram type [linear, linear_grayscale, log_power].')
    args = parser.parse_args()
    args.extension = "." + args.extension

    # Settings
    time = timer()
    splicerSpectrogram = SplicerSpectrogram(extension=args.extension)

    # Splice audios
    splicerSpectrogram.splice_audio_files(args.data_dir, args.splices_dir, chunk_length_ms=args.chunk_length_ms)

    # Audios spectrogram
    splicerSpectrogram.audio_spectrograms(args.splices_dir, args.specs_dir, spec_type=args.spec_type)

    # Time program ran for
    print("\nProgram ran for: %.2f seconds\n" % (timer()-time))
