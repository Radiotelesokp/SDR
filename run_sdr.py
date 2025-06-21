#!/usr/bin/env python3
import sys
import SoapySDR

SoapySDR.setLogLevel(SoapySDR.SOAPY_SDR_FATAL)

import bias_tee
import sdr_scan

HELP = """
Dostepne polecenia:
  bias on        - wlacz Bias-Tee
  bias off       - wylacz Bias-Tee
  bias status    - pokaz stan Bias-Tee
  scan           - skanuj pasmo
  help           - pokaz menu
  exit           - wyjscie z programu
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
            print("Wpisz poprawna liczbe")


def main():
    # Polaczenie z SDR
    try:
        sdr = SoapySDR.Device()
    except Exception as e:
        sys.exit(f"Blad polaczenia z SDR: {e}")

    driver = sdr.getDriverKey().lower()
    print(f"Uzywany sterownik SDR: {driver}")

    # Wymagany: HackRF
    #if driver != "hackrf":
    #    sys.exit(f"Brak obslugiwanego SDR - wymagany 'hackrf', wykryto '{driver}'.")

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


        # Skanowanie + wykres 
        if cmd == "scan":
            try:
                start_freq  = input_float("Start freq  (Hz): ")
                stop_freq   = input_float("Stop freq   (Hz): ")
                step_freq   = input_float("Step        (Hz): ")
                sample_rate = input_float("Sample rate (Hz): ")
                gain        = input_float("Gain        (dB): ")
                n_samples   = int(input_float("Sample count: "))

                print("» Rozpoczynam skanowanie...  (Ctrl+C aby przerwac)")
                sdr_scan.scan_band(sdr, sample_rate, gain, n_samples,
                                start_freq, stop_freq, step_freq)
                print("» Skanowanie zakonczone.\n")

            except KeyboardInterrupt:
                print("» Skanowanie przerwane.\n")
            except Exception as err:
                print("Blad podczas skanowania:", err)
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