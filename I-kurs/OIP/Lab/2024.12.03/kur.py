import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

sampling_rate = 44100


def generate_rectangular_wave(frequency, duration, amplitude):
    """
    Generates a rectangular wave signal.
    """
    num_samples = int(sampling_rate * duration)
    time = np.linspace(0, duration, num_samples, endpoint=False)
    audio_signal = amplitude * \
        np.sign(np.sin(2 * np.pi * frequency * time))  # Eq. 2
    return audio_signal


def generate_asymetric_triangular_wave(frequency, duration, amplitude):
    """
    Generates an asymmetric triangular wave signal.
    """
    num_samples = int(sampling_rate * duration)
    time = np.linspace(0, duration, num_samples, endpoint=False)
    period = 1 / frequency
    audio_signal = amplitude * (2 / period * (time % period) - 1)  # Eq. 3
    return audio_signal


def generate_sine_wave(frequency, duration, amplitude):
    """
    Generates a sine wave signal.
    """
    num_samples = int(sampling_rate * duration)
    time = np.linspace(0, duration, num_samples, endpoint=False)
    audio_signal = amplitude * np.sin(2 * np.pi * frequency * time)  # Eq. 1
    return audio_signal


def generate_symetric_triangular_wave(frequency, duration, amplitude):
    """
    Generates a symmetric triangular wave signal.
    """
    num_samples = int(sampling_rate * duration)
    time = np.linspace(0, duration, num_samples, endpoint=False)
    period = 1 / frequency
    audio_signal = amplitude * \
        (2 * (1 - np.abs((2 / period) * (time % period - period / 2)))) - 1  # Eq. 4
    return audio_signal


def visualize_signal(audio_signal, duration, title="Audio signal"):
    """
    Visualizes an audio signal in the time domain.

    Arguments:
        audio_signal: The audio signal to visualize.
        duration: The duration of the signal in seconds.
        title: The title for the plot.

    Returns:
        None
    """
    time = np.linspace(0, duration, len(audio_signal),
                       endpoint=False)  # Time axis
    plt.figure(figsize=(10, 4))
    plt.plot(time, audio_signal, label="Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_positive_spectrum(signal, title="Signal Spectrum (Positive Frequencies Only)"):
    """
    Plots the amplitude spectrum of a signal, showing only positive frequencies.

    Arguments:
        signal: The input signal.
        title: The title of the plot.

    Returns:
        None
    """
    signal_fft = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), 1 / sampling_rate)

    # Positive half of frequencies
    positive_frequencies = frequencies[:len(frequencies) // 2]
    positive_signal_fft = 2.0 / \
        len(signal) * np.abs(signal_fft[:len(signal) // 2])

    plt.figure(figsize=(10, 4))
    plt.plot(positive_frequencies, positive_signal_fft, label="Amplitude")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()


def save_signal_to_wav(filename, signal):
    """
    Save a signal to a WAV file.

    Arguments:
      filename (str): The name of the output WAV file.
      signal (numpy.ndarray): The signal data as a NumPy array.

    Returns:
      None
    """

    # Calculate the maximum amplitude of the signal
    max_amplitude = np.max(np.abs(signal))

    # Normalize the signal to the range [-1, 1]
    normalized_signal = signal / max_amplitude

    # Write the signal to a WAV file
    wavfile.write(filename, sampling_rate, normalized_signal)


def main():
    """
    The main function.

    This function generates simple audio signals, plays them, visualizes them, plots the spectrum, and saves the signals to wav file formats.
    """

    # Define the parameters for the audio signal.
    frequency = 480  # where x is the last digit of your faculty number !
    duration = 1
    amplitude = 1

    # Generate sine audio signal.
    audio_signal = generate_sine_wave(frequency, duration, amplitude)
    visualize_signal(audio_signal, duration, title="Sin wave")
    plot_positive_spectrum(
        audio_signal, title="Sin wave spectrum (positive frequencies only)")
    save_signal_to_wav("sin_wave.wav", audio_signal)

    # Generate rectangular audio signal.
    rectangular_wave = generate_rectangular_wave(
        frequency, duration, amplitude)
    visualize_signal(rectangular_wave, duration, title="Rectangular Wave")
    plot_positive_spectrum(rectangular_wave, title="Rectangular Wave Spectrum")
    save_signal_to_wav("rectangular_wave.wav", rectangular_wave)

    # Generate asymetric triangular audio signal.
    asymetric_triangle_wave = generate_asymetric_triangular_wave(
        frequency, duration, amplitude)
    visualize_signal(asymetric_triangle_wave, duration,
                     title="Asymmetric Triangular Wave")
    plot_positive_spectrum(asymetric_triangle_wave,
                           title="Asymmetric Triangular Wave Spectrum")
    save_signal_to_wav("asymetric_triangle_wave.wav", asymetric_triangle_wave)

    # Generate symetric triangular audio signal.
    symmetric_triangle_wave = generate_symetric_triangular_wave(
        frequency, duration, amplitude)
    visualize_signal(symmetric_triangle_wave, duration,
                     title="Symmetric Triangular Wave")
    plot_positive_spectrum(symmetric_triangle_wave,
                           title="Symmetric Triangular Wave Spectrum")
    save_signal_to_wav("symmetric_triangle_wave.wav", symmetric_triangle_wave)


if __name__ == "__main__":
    main()
