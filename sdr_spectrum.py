import numpy as np
from datetime import date
from sdr_samples import get_samples
import os

# sdr_spectrum.py - prawdziwy spektrogram z FFT
# Dla każdej częstotliwości centralnej pobiera próbki i tworzy bins FFT
# Zwraca szczegółowe dane widma w dziedzinie częstotliwości

OUTPUT_DIR = "output"

def scan_spectrum_sweep(sdr, sample_rate, gain, n_samples, 
                       start_freq, stop_freq, step_freq, channel=0, callback=None):
    """
    Skanuje pasmo częstotliwości i tworzy prawdziwy spektrogram.
    Dla każdej częstotliwości pobiera próbki, wykonuje FFT i zapisuje bins FFT.
    
    Args:
        sdr: urządzenie SDR
        sample_rate: częstotliwość próbkowania [Hz]
        gain: wzmocnienie [dB]
        n_samples: liczba próbek do pobrania
        start_freq: początek pasma [Hz]
        stop_freq: koniec pasma [Hz] 
        step_freq: krok częstotliwości [Hz]
        channel: kanał SDR (domyślnie 0)
        callback: opcjonalna funkcja callback(freq, power_db)
        
    Returns:
        tuple: (frequencies_array, power_spectrum_array) lub results list jeśli callback
    """
    
    if callback is not None:
        # Tryb callback - wywołuj funkcję dla każdego punktu widma
        results = []
        for center_freq in np.arange(start_freq, stop_freq + step_freq, step_freq):
            freqs, powers = _process_single_frequency(
                sdr, sample_rate, gain, n_samples, center_freq, channel
            )
            
            # Wywołaj callback dla każdego binu FFT
            for freq, power in zip(freqs, powers):
                if start_freq <= freq <= stop_freq:  # Filtruj do żądanego zakresu
                    callback(freq, power)
                    results.append((freq, power))
        
        return results
    
    else:
        # Tryb normalny - zbierz wszystkie dane i zapisz do pliku
        all_frequencies = []
        all_powers = []
        
        print(f"🔍 Skanowanie spektrum {start_freq/1e6:.0f}-{stop_freq/1e6:.0f} MHz...")
        
        for center_freq in np.arange(start_freq, stop_freq + step_freq, step_freq):
            print(f"   Przetwarzam {center_freq/1e6:.1f} MHz...", end='\r')
            
            freqs, powers = _process_single_frequency(
                sdr, sample_rate, gain, n_samples, center_freq, channel
            )
            
            # Filtruj bins FFT do żądanego zakresu częstotliwości
            mask = (freqs >= start_freq) & (freqs <= stop_freq)
            filtered_freqs = freqs[mask]
            filtered_powers = powers[mask]
            
            all_frequencies.extend(filtered_freqs)
            all_powers.extend(filtered_powers)
        
        print("\n✅ Skanowanie zakończone")
        
        # Konwertuj do numpy arrays i posortuj według częstotliwości
        frequencies = np.array(all_frequencies)
        power_spectrum = np.array(all_powers)
        
        # Sortuj według częstotliwości
        sort_indices = np.argsort(frequencies)
        frequencies = frequencies[sort_indices]
        power_spectrum = power_spectrum[sort_indices]
        
        # Zapisz do pliku CSV
        _save_spectrum_to_csv(frequencies, power_spectrum, start_freq, stop_freq)
        
        # Automatycznie narysuj wykres (tylko jeśli plot_csv jest dostępny)
        try:
            import plot_csv
            today_str = date.today().isoformat()
            range_str = f"{int(start_freq)}-{int(stop_freq)}_{today_str}"
            plot_csv.plot_spectrum_from_csv(range_str, save=True, show=False)
        except ImportError as e:
            print(f"Nie można zaimportować plot_csv: {e}")
        except Exception as e:
            print(f"Błąd podczas rysowania wykresu: {e}")
        
        return frequencies, power_spectrum


def _process_single_frequency(sdr, sample_rate, gain, n_samples, center_freq, channel):
    """
    Przetwarza jedną częstotliwość centralną - pobiera próbki i wykonuje FFT.
    
    Returns:
        tuple: (frequencies, power_spectrum_db)
    """
    # Pobierz próbki dla danej częstotliwości centralnej
    samples = get_samples(sdr, sample_rate, center_freq, gain, n_samples, channel)
    
    # FFT daje bins wokół częstotliwości centralnej
    fft_bins = np.fft.fftshift(np.fft.fft(samples))
    fft_freqs = np.fft.fftshift(np.fft.fftfreq(len(samples), 1/sample_rate))
    
    # Rzeczywiste częstotliwości = freq_centralna + offset_FFT
    actual_freqs = center_freq + fft_freqs
    
    # Moc w dBFS dla każdego binu (dodaj epsilon aby uniknąć log(0))
    magnitude = np.abs(fft_bins)
    power_dbfs = 20 * np.log10(magnitude + 1e-12)
    
    return actual_freqs, power_dbfs


def _save_spectrum_to_csv(frequencies, power_spectrum, start_freq, stop_freq):
    """Zapisuje pełne dane spektrum do pliku CSV."""
    today_str = date.today().isoformat()
    range_str = f"{int(start_freq)}-{int(stop_freq)}"
    spectrum_fname = os.path.join(OUTPUT_DIR, f"spectrum_{range_str}_{today_str}.csv")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"💾 Zapisuję spektrum do: {spectrum_fname}")
    
    with open(spectrum_fname, "w") as f:
        f.write("frequency_hz,power_dbfs\n")
        for freq, power in zip(frequencies, power_spectrum):
            f.write(f"{freq:.0f},{power:.2f}\n")


def scan_power_vs_frequency(sdr, sample_rate, gain, n_samples,
                           start_freq, stop_freq, step_freq, channel=0, callback=None):
    """
    Uproszczona wersja - dla każdej częstotliwości mierzy całkowitą moc.
    Daje jeden punkt mocy na częstotliwość (bez szczegółów FFT).
    """
    frequencies = []
    power_levels = []
    
    print(f"🔍 Skanowanie mocy {start_freq/1e6:.0f}-{stop_freq/1e6:.0f} MHz...")
    
    for center_freq in np.arange(start_freq, stop_freq + step_freq, step_freq):
        print(f"   Mierzę {center_freq/1e6:.1f} MHz...", end='\r')
        
        samples = get_samples(sdr, sample_rate, center_freq, gain, n_samples, channel)
        
        # Całkowita moc sygnału (RMS)
        total_power = np.mean(np.abs(samples)**2)
        power_db = 10 * np.log10(total_power + 1e-12)
        
        frequencies.append(center_freq)
        power_levels.append(power_db)
        
        # Callback jeśli podany
        if callback is not None:
            callback(center_freq, power_db)
    
    print("\n✅ Skanowanie zakończone")
    
    if callback is None:
        # Zapisz do pliku
        today_str = date.today().isoformat()
        range_str = f"{int(start_freq)}-{int(stop_freq)}"
        power_fname = os.path.join(OUTPUT_DIR, f"power_{range_str}_{today_str}.csv")
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        print(f"💾 Zapisuję dane mocy do: {power_fname}")
        
        with open(power_fname, "w") as f:
            f.write("frequency_hz,power_db\n")
            for freq, power in zip(frequencies, power_levels):
                f.write(f"{int(freq)},{power:.2f}\n")
        
        # Automatycznie narysuj wykres (tylko jeśli plot_csv jest dostępny)
        try:
            import plot_csv
            plot_csv.plot_power_from_csv(range_str, save=True, show=False)
        except ImportError as e:
            print(f"Nie można zaimportować plot_csv: {e}")
        except Exception as e:
            print(f"Błąd podczas rysowania wykresu: {e}")
    
    return np.array(frequencies), np.array(power_levels)
