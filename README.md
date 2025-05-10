# SDR
## Konfiguracja środowiska
Projekt zawiera dwa rodzaje konfiguracji: docker-compose oraz venv. Wybór pozostawiam do oceny czytelnika.
### Venv
1. Tworzenie venv
```shell
python3 -m venv .venv
```
2. Uruchomienie venv
```shell
source .venv/bin/activate
```
3. Pobranie bibliotek:
```shell
pip install -r requirements.txt
```
4. Zatrzymanie venv
```shell
deactivate
```

### Docker compose
Komenda uruchamiająca docker-compose
```shell
docker-compose up
```

Aby zatrzymać dockera wystarczy wpisać 
```shell
docker-compose down
```
