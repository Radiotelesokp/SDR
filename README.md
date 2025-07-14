# SDR Spectrum Analyzer

Program do automatycznego skanowania i wizualizacji widma radiowego z użyciem HackRF One i SoapySDR.

## Funkcje
- Automatyczne skanowanie wybranego zakresu częstotliwości (np. 1–2 GHz)
- Szczegółowy spektrogram (FFT dla każdego kroku)
- Prosty wykres mocy (średnia moc na każdej częstotliwości)
- Obsługa Bias-Tee (zasilanie anteny)
- Zapis wyników do plików CSV i PNG
- Interaktywny tryb konsolowy oraz tryb automatyczny

## Wymagania
- Python 3.8+
- SoapySDR (instalowany systemowo)
- HackRF One
- Pakiety Python: numpy, pandas, matplotlib

## Instalacja
1. Zainstaluj SoapySDR i sterowniki HackRF:
   ```bash
   sudo apt update
   sudo apt install python3-soapysdr soapysdr-module-hackrf hackrf
   ```
2. Utwórz środowisko wirtualne i zainstaluj zależności:
   ```bash
   python3 -m venv venv --system-site-packages
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Podłącz HackRF One i sprawdź numer seryjny:
   ```bash
   SoapySDRUtil --find
   ```
   Skopiuj numer seryjny do plików konfiguracyjnych (np. `run_sdr.py`, `auto_scan.py`).

## Użycie
### Tryb interaktywny:
```bash
python3 run_sdr.py
```
Dostępne komendy:
- `spectrum` – szczegółowy spektrogram (FFT)
- `power` – prosty wykres mocy
- `plot` – rysowanie wykresów z plików CSV
- `bias on|off|status` – sterowanie Bias-Tee
- `help` – menu pomocy
- `exit` – wyjście

### Tryb automatyczny:
```bash
python3 auto_scan.py
```
Parametry zakresu i ustawień odbiornika edytuj w pliku `auto_scan.py`.

### Rysowanie wykresów z plików:
```bash
python3 plot_csv.py <prefix> [spectrum|power|max_mean]
# Przykład:
python3 plot_csv.py 1000000000-2000000000_2025-07-14 spectrum
```

## Struktura plików
- `run_sdr.py` – tryb interaktywny
- `auto_scan.py` – tryb automatyczny
- `sdr_spectrum.py` – logika FFT i zapisu CSV
- `plot_csv.py` – rysowanie wykresów
- `bias_tee.py` – obsługa Bias-Tee
- `sdr_samples.py` – pobieranie próbek z SDR
- `output/` – wyniki CSV i PNG

## Uwagi
- SoapySDR i sterowniki HackRF instaluj systemowo (nie przez pip)
- Jeśli pojawią się błędy importu, sprawdź czy środowisko wirtualne ma dostęp do systemowych pakietów
- W razie problemów z matplotlib: sprawdź czy nie masz kilku wersji tej biblioteki
