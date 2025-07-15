import numpy as np
import SoapySDR
import logging
from datetime import date
from plot_csv import plot_max_and_mean


class SpectrumScanner:
    logger = logging.getLogger(__name__)

    def __init__(self, sdr, start_freq, stop_freq, step_freq, sample_rate, gain, n_samples, channel):
        self.sdr = sdr
        self.start_freq = self.convertStrToFloat(start_freq)
        self.stop_freq = self.convertStrToFloat(stop_freq)
        self.step_freq = self.convertStrToFloat(step_freq)
        self.sample_rate = self.convertStrToFloat(sample_rate)
        self.gain = self.convertStrToFloat(gain)
        self.n_samples = self.convertStrToInt(n_samples)
        self.channel = self.convertStrToInt(channel)

    def convertStrToFloat(self, variable: str) -> float:
        try:
            return float(variable)
        except (TypeError, ValueError) as e:
            self.logger.warning(f"Conversion to float failed for value: {variable} ({e})")
            return 0.0

    def convertStrToInt(self, variable: str) -> int:
        try:
            return int(variable)
        except (TypeError, ValueError) as e:
            self.logger.warning(f"Conversion to int failed for value: {variable} ({e})")
            return 0

    def getSimpleFrequency(self, freq):
        direction = SoapySDR.SOAPY_SDR_RX

        self.sdr.setSampleRate(direction, self.channel, self.sample_rate)
        self.sdr.setFrequency(direction, self.channel, freq)
        self.sdr.setGain(direction, self.channel, self.gain)

        buffer = np.empty(self.n_samples, dtype=np.complex64)
        sample_format = SoapySDR.SOAPY_SDR_CF32

        stream = self.sdr.setupStream(direction, sample_format)
        self.sdr.activateStream(stream)

        result = self.sdr.readStream(stream, [buffer], self.n_samples)

        self.sdr.deactivateStream(stream)
        self.sdr.closeStream(stream)

        if result.ret <= 0:
            raise RuntimeError("SDR sampling error.")

        return buffer[:result.ret]

    def scan(self):
        results = []
        today_str = date.today().isoformat()
        max_filename = f"max_{int(self.start_freq)}-{int(self.stop_freq)}_{today_str}.csv"
        mean_filename = f"mean_{int(self.start_freq)}-{int(self.stop_freq)}_{today_str}.csv"

        with open(max_filename, "w") as max_file, open(mean_filename, "w") as mean_file:
            self.logger.info(f"Write to files: {max_filename}, {mean_filename}")
            max_file.write("frequency_hz,max_db\n")
            mean_file.write("frequency_hz,mean_db\n")

            for freq in np.arange(self.start_freq, self.stop_freq + self.step_freq, self.step_freq):
                samples = self.getSimpleFrequency(freq)
                spectrum = np.fft.fftshift(np.fft.fft(samples))

                max_val = np.abs(spectrum).max()            # wzor na max widma:   20*log10(max(|FFT(samples)|))
                mean_val = np.mean(np.abs(spectrum) ** 2)   # wzor na srednia moc: 10*log10(mean(|FFT(samples)|^2))

                if max_val == 0 or mean_val == 0:
                    self.logger.warning(f"Ignore {int(freq)} Hz - no signal")
                    continue

                max_db = 20 * np.log10(max_val)
                mean_db = 10 * np.log10(mean_val)

                results.append((freq, max_db, mean_db))
                max_file.write(f"{int(freq)},{max_db:.2f}\n")
                mean_file.write(f"{int(freq)},{mean_db:.2f}\n")

        plot_max_and_mean(f"{int(self.start_freq)}-{int(self.stop_freq)}_{today_str}")

        return results


# sdr_scan.py - skanowanie pasma przy uzyciu get_samples()
# zapisuje max_XXX-YYY_DATA.csv i mean_XXX-YYY_DATA.csv

'''
def scan_band(sdr, sample_rate, gain, n_samples,
              start_freq, stop_freq, step_freq, channel=0):
    results = []


    today_str  = date.today().isoformat()
    max_filename  = f"max_{int(start_freq)}-{int(stop_freq)}_{today_str}.csv"
    mean_filename = f"mean_{int(start_freq)}-{int(stop_freq)}_{today_str}.csv"

    with open(max_filename, "w") as max_file, open(mean_filename, "w") as mean_file:
        print(f"Zapis do plikow: {max_filename}, {mean_filename}")
        max_file.write("frequency_hz,max_db\n")
        mean_file.write("frequency_hz,mean_db\n")

        for freq in np.arange(start_freq, stop_freq + step_freq, step_freq):
            samples  = get_samples(sdr, sample_rate, freq, gain, n_samples, channel)
            spectrum = np.fft.fftshift(np.fft.fft(samples))

            max_val  = np.abs(spectrum).max()
            mean_val = np.mean(np.abs(spectrum) ** 2)

            if max_val == 0 or mean_val == 0:
                print(f"Pominieto {int(freq)} Hz - brak sygnalu")
                continue

            max_db  = 20 * np.log10(max_val)
            mean_db = 10 * np.log10(mean_val)

            results.append((freq, max_db, mean_db))
            max_file.write(f"{int(freq)},{max_db:.2f}\n")
            mean_file.write(f"{int(freq)},{mean_db:.2f}\n")

    plot_max_and_mean(f"{int(start_freq)}-{int(stop_freq)}_{today_str}")

    return results '''