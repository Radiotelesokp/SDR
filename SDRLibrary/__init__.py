"""
SDR
* DONE: Przeczytać dokumenty o bias-tee, wzmacniaczu i SDR, żeby zrozumieć, jak działa cały tor sygnału
* DONE: Skonfigurować Pythona: utworzyć virtualenv, zainstalować UHD/SoapySDR i potrzebne biblioteki
* Napisać skrypt, który odbiera sygnał i pokazuje widmo na wykresie
* Zaprogramować moduł, który skanuje kolejne częstotliwości i zapisuje wyniki do pliku
* DONE: Dodać sterowanie bias-tee przez Pythona, żeby włączać i wyłączać przedwzmacniacz
* DONE: Połączyć wszystkie skrypty w jeden pakiet Pythonowy
* DONE: Przygotować krótką instrukcję obsługi i przykładowe skrypty

"""

from SDRLibrary.bias_tee import *
from SDRLibrary.plot_csv import *
from SDRLibrary.sdr_samples import *
from SDRLibrary.sdr_scan import *

__all__ = ["BiasTee", "SpectrumScanner", "plot_max_and_mean", "get_samples"]