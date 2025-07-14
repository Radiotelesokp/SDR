import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = "output"

def plot_max_and_mean(prefix, save=True, show=True):
    max_file = os.path.join(OUTPUT_DIR, f"max_{prefix}.csv")
    mean_file = os.path.join(OUTPUT_DIR, f"mean_{prefix}.csv")

    if not os.path.exists(max_file) or not os.path.exists(mean_file):
        print("Nie znaleziono plikow:", max_file, mean_file)
        return

    df_max = pd.read_csv(max_file)
    df_mean = pd.read_csv(mean_file)

    plt.figure(figsize=(10, 5))
    plt.plot(df_max["frequency_hz"], df_max["max_db"], label="Max dB", marker='o')
    plt.plot(df_mean["frequency_hz"], df_mean["mean_db"], label="Mean dB", marker='x')

    plt.title(f"Widmo sygnalu - {prefix}")
    plt.xlabel("Czestotliwosc [Hz]")
    plt.ylabel("Poziom [dB]")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save:
        png_file = os.path.join(OUTPUT_DIR, f"spectrum_{prefix}.png")
        plt.savefig(png_file)
        print(f"Wykres zapisany jako: {png_file}")

    if show:
        plt.show()

    plt.close()


def plot_spectrum_from_csv(prefix, save=True, show=True):
    """
    Rysuje spektrogram z pliku CSV zawierającego szczegółowe dane FFT.
    """
    spectrum_file = os.path.join(OUTPUT_DIR, f"spectrum_{prefix}.csv")
    
    if not os.path.exists(spectrum_file):
        print(f"Nie znaleziono pliku spektrum: {spectrum_file}")
        return
    
    df = pd.read_csv(spectrum_file)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df["frequency_hz"] / 1e6, df["power_dbfs"], 'b-', linewidth=0.5, alpha=0.8)
    
    plt.title(f"Spektrum sygnału - {prefix}")
    plt.xlabel("Częstotliwość [MHz]")
    plt.ylabel("Moc [dBFS]")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save:
        png_file = os.path.join(OUTPUT_DIR, f"spectrum_{prefix}.png")
        plt.savefig(png_file, dpi=300, bbox_inches='tight')
        print(f"📊 Wykres spektrum zapisany jako: {png_file}")
    
    if show:
        plt.show()
    
    plt.close()


def plot_power_from_csv(prefix, save=True, show=True):
    """
    Rysuje wykres mocy z pliku CSV (jeden punkt na częstotliwość).
    """
    power_file = os.path.join(OUTPUT_DIR, f"power_{prefix}.csv")
    
    if not os.path.exists(power_file):
        print(f"Nie znaleziono pliku mocy: {power_file}")
        return
    
    df = pd.read_csv(power_file)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df["frequency_hz"] / 1e6, df["power_db"], 'r-o', linewidth=1, markersize=3)
    
    plt.title(f"Moc sygnału - {prefix}")
    plt.xlabel("Częstotliwość [MHz]")
    plt.ylabel("Moc [dB]")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save:
        png_file = os.path.join(OUTPUT_DIR, f"power_{prefix}.png")
        plt.savefig(png_file, dpi=300, bbox_inches='tight')
        print(f"📊 Wykres mocy zapisany jako: {png_file}")
    
    if show:
        plt.show()
    
    plt.close()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print(f"Użycie: python3 {os.path.basename(__file__)} <prefix> [spectrum|power|max_mean]")
        sys.exit(1)
    
    prefix = sys.argv[1]
    plot_type = sys.argv[2] if len(sys.argv) > 2 else "max_mean"
    
    if plot_type in ["spectrum", "s"]:
        plot_spectrum_from_csv(prefix)
    elif plot_type in ["power", "p"]:
        plot_power_from_csv(prefix)
    elif plot_type in ["max_mean", "mm"]:
        plot_max_and_mean(prefix)
    else:
        print("Nieznany typ wykresu. Dostępne: spectrum, power, max_mean")
        sys.exit(1)