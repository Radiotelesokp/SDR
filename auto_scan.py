#!/usr/bin/env python3
"""
auto_scan.py  –  automatyczny skaner pasma 1–2 GHz dla HackRF One

• łączy się z HackRF (po numerze seryjnym)
• opcjonalnie włącza Bias-Tee (jeśli potrzebujesz)
• skanuje zadany zakres i zapisuje wyniki w pliku CSV
"""

import sys
import datetime
import SoapySDR

SoapySDR.setLogLevel(SoapySDR.SOAPY_SDR_FATAL)

import bias_tee
import sdr_spectrum
import plot_csv


# ────────── KONFIGURACJA ──────────────────────────────────────────────────────
SERIAL = "0000000000000000436c63dc2f272b63"     # numer HackRF One

# Zakres skanowania
START_FREQ  = 1_000_000_000      # 1 GHz
STOP_FREQ   = 2_000_000_000      # 2 GHz
STEP_FREQ   = 1_000_000          # 1 MHz

# Ustawienia odbiornika
SAMPLE_RATE = 2_000_000          # 2 MS/s
GAIN        = 32                 # dB
N_SAMPLES   = 1_048_576          # 1 M próbek (1024*1024)

# Bias-Tee (True = włącz, False = wyłącz)
USE_BIAS_TEE = False
# ──────────────────────────────────────────────────────────────────────────────


def main() -> None:
    # 1. Połączenie z urządzeniem
    try:
        sdr = SoapySDR.Device(dict(driver="hackrf", serial=SERIAL))
    except Exception as err:
        sys.exit(f"Nie mogę otworzyć HackRF: {err}")

    print("▶️  Połączono z HackRF One")
    print(f"   Driver : {sdr.getDriverKey()}")
    print(f"   Serial : {SERIAL}")

    # 2. Bias-Tee (jeśli potrzebny)
    if USE_BIAS_TEE:
        try:
            bias_tee.control_bias_tee(sdr, "on")
            print("⚡ Bias-Tee włączony")
        except Exception as err:
            print("❗ Błąd Bias-Tee:", err)

    # 3. Skanowanie
    try:
        print(f"🔍 Skanowanie {START_FREQ/1e6:.0f}–{STOP_FREQ/1e6:.0f} MHz …")
        frequencies, power_spectrum = sdr_spectrum.scan_spectrum_sweep(
            sdr,
            SAMPLE_RATE,
            GAIN,
            N_SAMPLES,
            START_FREQ,
            STOP_FREQ,
            STEP_FREQ
        )
        
        # Narysuj spektrogram
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        range_str = f"{int(START_FREQ)}-{int(STOP_FREQ)}_{today_str}"
        plot_csv.plot_spectrum_from_csv(range_str, save=True, show=False)
        
        print("✅ Skanowanie zakończone")

    except KeyboardInterrupt:
        print("\n⏹️  Przerwano skanowanie klawiszem")
    finally:
        if USE_BIAS_TEE:
            try:
                bias_tee.control_bias_tee(sdr, "off")
            except Exception:
                pass


if __name__ == "__main__":
    main()
