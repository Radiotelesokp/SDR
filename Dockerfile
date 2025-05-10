# Użyj oficjalnego obrazu Pythona
FROM python:3.11-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki projektu
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Domyślny punkt wejścia – możesz to zmienić na np. gunicorn, uvicorn, itp.
CMD ["python", "main.py"]