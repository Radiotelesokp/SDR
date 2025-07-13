import numpy as np
from datetime import date
from sdr_samples import get_samples
from plot_csv import plot_max_and_mean
import os

# sdr_scan.py - skanowanie pasma przy uzyciu get_samples()
# zapisuje max_XXX-YYY_DATA.csv i mean_XXX-YYY_DATA.csv

# wzor na max widma:   20*log10(max(|FFT(samples)|))
# wzor na srednia moc: 10*log10(mean(|FFT(samples)|^2))
OUTPUT_DIR = "output"

def scan_band(sdr, sample_rate, gain, n_samples,
              start_freq, stop_freq, step_freq, channel=0):
    results = []

    today_str  = date.today().isoformat()
    range_str  = f"{int(start_freq)}-{int(stop_freq)}"
    max_fname  = os.path.join(OUTPUT_DIR, f"max_{range_str}_{today_str}.csv")
    mean_fname = os.path.join(OUTPUT_DIR,f"mean_{range_str}_{today_str}.csv")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(max_fname, "w") as max_file, open(mean_fname, "w") as mean_file:
        print(f"Zapis do plikow: {max_fname}, {mean_fname}")
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

    return results