# Description: This script generates and visualizes different types of audio signals (sine, rectangular, asymmetric triangular, and symmetric triangular waves). It then saves these signals as WAV files.  The script uses matplotlib for visualization and scipy for WAV file I/O.
# Tags: Audio Signal Generation, Waveform Visualization, WAV File, Signal Processing, Spectrum Analysis

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

sampling_rate = 44100


def generate_sine_wave(frequency, duration, amplitude):
    """
    Generates a simple audio signal with a sine wave form.

    Arguments:
        frequency: The frequency of the signal in Hz.
        duration: The duration of the signal in seconds.
        amplitude: The amplitude of the signal.

    Returns:
        A simple audio signal with a sine wave form.
    """
    num_samples = int(sampling_rate * duration)
    time = np.linspace(0, duration, num_samples, endpoint=False)
    audio_signal = amplitude * np.sin(2 * np.pi * frequency * time)
    return audio_signal


def generate_rectangular_wave(frequency, duration, amplitude):
    """
    Generates a simple audio signal with a rectangular wave form.

    Arguments:
        frequency: The frequency of the signal in Hz.
        duration: The duration of the signal in seconds.
        amplitude: The amplitude of the signal.

    Returns:
        A simple audio signal with a rectangular wave form.
    """
    num_samples = int(sampling_rate * duration)
    time = np.linspace(0, duration, num_samples, endpoint=False)
    audio_signal = amplitude * np.sign(np.sin(2 * np.pi * frequency * time))
    return audio_signal


def generate_asymetric_triangular_wave(frequency, duration, amplitude):
    """
    Generates a simple audio signal with an asymmetric triangular wave form.

    Arguments:
        frequency: The frequency of the signal in Hz.
        duration: The duration of the signal in seconds.
        amplitude: The amplitude of the signal.

    Returns:
        A simple audio signal with an asymmetric triangular wave form.
    """
    num_samples = int(sampling_rate * duration)
    time = np.linspace(0, duration, num_samples, endpoint=False)
    period = 1 / frequency
    audio_signal = amplitude * (2 * np.abs((time % period) / period - 0.5) - 1)
    return audio_signal


def generate_symmetric_triangular_wave(frequency, duration, amplitude):
    """
    Generates a simple audio signal with a symmetric triangular wave form.

    Arguments:
        frequency: The frequency of the signal in Hz.
        duration: The duration of the signal in seconds.
        amplitude: The amplitude of the signal.

    Returns:
        A simple audio signal with a symmetric triangular wave form.
    """
    num_samples = int(sampling_rate * duration)
    time = np.linspace(0, duration, num_samples, endpoint=False)
    period = 1 / frequency
    audio_signal = amplitude * (2 * np.abs((time % period) / period - 0.5) - 1)
    return audio_signal


def visualize_signal(audio_signal, duration, title="Audio signal"):
    """
    Visualizes an audio signal.

    Arguments:
        audio_signal: The audio signal to visualize.
        duration: The duration of the signal in seconds.
    """
    time = np.linspace(0, duration, len(audio_signal))
    plt.figure(figsize=(10, 6))
    plt.plot(time, audio_signal)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.show()


def plot_positive_spectrum(signal, title="Signal Spectrum (Positive Frequencies Only)"):
    """
    Plot the amplitude spectrum of a signal, showing only positive frequencies.

    Arguments:
        signal (array-like): The input signal for which to calculate the spectrum.
        title (str, optional): The title for the plot (default is "Signal Spectrum (Positive Frequencies Only)").
    """
    signal_fft = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), 1 / sampling_rate)
    positive_frequencies = frequencies[:len(frequencies) // 2]
    positive_signal_fft = 2.0 / \
        len(signal) * np.abs(signal_fft[:len(signal) // 2])

    plt.figure(figsize=(10, 6))
    plt.plot(positive_frequencies, positive_signal_fft)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.show()


def save_signal_to_wav(filename, signal):
    """
    Save a signal to a WAV file.

    Arguments:
        filename (str): The name of the output WAV file.
        signal (numpy.ndarray): The signal data as a NumPy array.
    """
    max_amplitude = np.max(np.abs(signal))
    normalized_signal = (signal / max_amplitude * 32767).astype(np.int16)
    wavfile.write(filename, sampling_rate, normalized_signal)


def main():
    """
    The main function.

    This function generates simple audio signals, visualizes them, plots the spectrum,
    and saves the signals to WAV file formats.
    """
    frequency = 40  # Replace with appropriate frequency
    duration = 0.1
    amplitude = 1

    # Generate sine audio signal.
    sine_wave = generate_sine_wave(frequency, duration, amplitude)
    visualize_signal(sine_wave, duration, title="Sine Wave")
    plot_positive_spectrum(
        sine_wave, title="Sine Wave Spectrum (Positive Frequencies Only)")
    save_signal_to_wav("sine_wave.wav", sine_wave)

    # Generate rectangular audio signal.
    rectangular_wave = generate_rectangular_wave(
        frequency, duration, amplitude)
    visualize_signal(rectangular_wave, duration, title="Rectangular Wave")
    plot_positive_spectrum(
        rectangular_wave, title="Rectangular Wave Spectrum (Positive Frequencies Only)")
    save_signal_to_wav("rectangular_wave.wav", rectangular_wave)

    # Generate asymmetric triangular audio signal.
    asym_tri_wave = generate_asymetric_triangular_wave(
        frequency, duration, amplitude)
    visualize_signal(asym_tri_wave, duration,
                     title="Asymmetric Triangular Wave")
    plot_positive_spectrum(
        asym_tri_wave, title="Asymmetric Triangular Wave Spectrum (Positive Frequencies Only)")
    save_signal_to_wav("asymmetric_triangular_wave.wav", asym_tri_wave)

    # Generate symmetric triangular audio signal.
    sym_tri_wave = generate_symmetric_triangular_wave(
        frequency, duration, amplitude)
    visualize_signal(sym_tri_wave, duration, title="Symmetric Triangular Wave")
    plot_positive_spectrum(
        sym_tri_wave, title="Symmetric Triangular Wave Spectrum (Positive Frequencies Only)")
    save_signal_to_wav("symmetric_triangular_wave.wav", sym_tri_wave)


if __name__ == "__main__":
    main()