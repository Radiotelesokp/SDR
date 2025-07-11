import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_max_and_mean(prefix, save=True, show=True):
    max_file = f"max_{prefix}.csv"
    mean_file = f"mean_{prefix}.csv"

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
        png_file = f"spectrum_{prefix}.png"
        plt.savefig(png_file)
        print(f"Wykres zapisany jako: {png_file}")

    if show:
        plt.show()

    plt.close()