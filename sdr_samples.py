import numpy as np
import SoapySDR

# sdr_samples.py - pojedyncze pobranie probek z urzadzenia SDR
# zwraca: ndarray[complex64] z odebranymi probkami

def get_samples(sdr, sample_rate, center_freq, gain, n_samples, channel=0):
    direction = SoapySDR.SOAPY_SDR_RX

    sdr.setSampleRate(direction, channel, float(sample_rate))
    sdr.setFrequency(direction, channel, float(center_freq))
    sdr.setGain(direction, channel, float(gain))

    buffer = np.empty(n_samples, dtype=np.complex64)
    sample_format = SoapySDR.SOAPY_SDR_CF32

    stream = sdr.setupStream(direction, sample_format)
    
    try:
        sdr.activateStream(stream)
        result = sdr.readStream(stream, [buffer], n_samples)
    finally:
        try:
            sdr.deactivateStream(stream)
            sdr.closeStream(stream)
        except:
            pass

    if result.ret <= 0:
        raise RuntimeError("Blad pobierania probek z SDR.")

    return buffer[:result.ret]