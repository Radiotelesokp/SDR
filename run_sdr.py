#!/usr/bin/env python3
import sys
import SoapySDR

SoapySDR.setLogLevel(SoapySDR.SOAPY_SDR_FATAL)

import bias_tee
import sdr_scan
import sdr_spectrum
import plot_csv


# TO check id: prompt in comand line: 'SoapySDRUtil --find' and find ypur HackRF serial number
SERIAL = "0000000000000000436c63dc2f272b63"  # HackRF serial number, 

HELP = """
Dostępne polecenia:
  bias on        - włącz Bias-Tee
  bias off       - wyłącz Bias-Tee
  bias status    - pokaż stan Bias-Tee
  spectrum       - skanuj spektrum (szczegółowy FFT)
  power          - skanuj moc (jeden punkt na częstotliwość)
  plot           - narysuj wykres z zapisanych danych
  help           - pokaż menu
  exit           - wyjście z programu
"""

def input_float(msg):
    while True:
        try:
            val = input(msg).strip()

            if not val:
                print("Anulowano.\n")
                raise KeyboardInterrupt

            return float(val)

        except ValueError:
            print("Wpisz poprawną liczbę")


def main():
    # Polaczenie z SDR
    try:
        #sdr = SoapySDR.Device()
        sdr = SoapySDR.Device(dict(driver="hackrf", serial=SERIAL))
    except Exception as e:
        sys.exit(f"Blad polaczenia z SDR: {e}")

    driver = sdr.getDriverKey().lower()
    print(f"Uzywany sterownik SDR: {driver}")

    # Wymagany: HackRF
    if driver != "hackrf":
        sys.exit(f"Brak obslugiwanego SDR - wymagany 'hackrf', wykryto '{driver}'.")

    print(">>> Wpisz 'help' aby zobaczyc komendy.")

    while True:
        try:
            cmd = input(">>> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExit.")
            break

        # Sterowanie Bias-Tee
        if cmd.startswith("bias "):
            try:
                action = cmd.split(maxsplit=1)[1]
            except IndexError:
                print("Uzycie: bias on|off|status")
                continue
            try:
                bias_tee.control_bias_tee(sdr, action)
            except Exception as err:
                print("Blad Bias-Tee:", err)
            continue

        # Skanowanie spektrum(poprawne FFT) 
        if cmd == "spectrum":
            try:
                start_freq  = input_float("Start freq  (Hz): ")
                stop_freq   = input_float("Stop freq   (Hz): ")
                step_freq   = input_float("Step        (Hz): ")
                sample_rate = input_float("Sample rate (Hz): ")
                gain        = input_float("Gain        (dB): ")
                n_samples   = int(input_float("Sample count: "))

                print("» Rozpoczynam skanowanie spektrum...  (Ctrl+C aby przerwać)")
                frequencies, power_spectrum = sdr_spectrum.scan_spectrum_sweep(
                    sdr, sample_rate, gain, n_samples,
                    start_freq, stop_freq, step_freq
                )
                
                print("» Skanowanie spektrum zakończone.\n")

            except KeyboardInterrupt:
                print("» Skanowanie przerwane.\n")
            except Exception as err:
                print("Błąd podczas skanowania spektrum:", err)
            continue

        # Skanowanie mocy (prosty)
        if cmd == "power":
            try:
                start_freq  = input_float("Start freq  (Hz): ")
                stop_freq   = input_float("Stop freq   (Hz): ")
                step_freq   = input_float("Step        (Hz): ")
                sample_rate = input_float("Sample rate (Hz): ")
                gain        = input_float("Gain        (dB): ")
                n_samples   = int(input_float("Sample count: "))

                print("» Rozpoczynam skanowanie mocy...  (Ctrl+C aby przerwać)")
                frequencies, power_levels = sdr_spectrum.scan_power_vs_frequency(
                    sdr, sample_rate, gain, n_samples,
                    start_freq, stop_freq, step_freq
                )
                
                print("» Skanowanie mocy zakończone.\n")

            except KeyboardInterrupt:
                print("» Skanowanie przerwane.\n")
            except Exception as err:
                print("Błąd podczas skanowania mocy:", err)
            continue

        # Rysowanie wykresów
        if cmd == "plot":
            try:
                prefix = input("Podaj prefix pliku (np. 1000-2000_2025-07-14): ").strip()
                plot_type = input("Typ wykresu [spectrum/power/max_mean]: ").strip().lower()
                
                if plot_type in ["spectrum", "s"]:
                    plot_csv.plot_spectrum_from_csv(prefix, save=True, show=True)
                elif plot_type in ["power", "p"]:
                    plot_csv.plot_power_from_csv(prefix, save=True, show=True)
                elif plot_type in ["max_mean", "mm", ""]:
                    plot_csv.plot_max_and_mean(prefix, save=True, show=True)
                else:
                    print("Nieznany typ wykresu")
                    
            except KeyboardInterrupt:
                print("Anulowano.\n")
            except Exception as err:
                print("Błąd podczas rysowania:", err)
            continue

        # Pomoc / Wyjscie
        if cmd in {"help"}:
            print(HELP)
            continue

        if cmd in {"exit"}:
            break

        print("Nieznane polecenie. Wpisz 'help'.")


if __name__ == "__main__":
    main()