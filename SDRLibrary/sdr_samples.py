import numpy as np
import SoapySDR

# sdr_samples.py - pojedyncze pobranie probek z urzadzenia SDR
# zwraca: ndarray[complex64] z odebranymi probkami

def get_samples(sdr, sample_rate, center_freq, gain, n_samples, channel=0):
    direction = SoapySDR.SOAPY_SDR_RX

    sdr.setSampleRate(direction, channel, sample_rate)
    sdr.setFrequency(direction, channel, center_freq)
    sdr.setGain(direction, channel, gain)

    buffer = np.empty(n_samples, dtype=np.complex64)
    sample_format = SoapySDR.SOAPY_SDR_CF32

    stream = sdr.setupStream(direction, sample_format)
    sdr.activateStream(stream)

    result = sdr.readStream(stream, [buffer], n_samples)

    sdr.deactivateStream(stream)
    sdr.closeStream(stream)

    if result.ret <= 0:
        raise RuntimeError("Blad pobierania probek z SDR.")

    return buffer[:result.ret]