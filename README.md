# To-Do Web-App

Eine kleine Flask-Webanwendung zur Verwaltung von Aufgaben. Entstanden als Übungsprojekt zum Lernen von Git und GitHub.

## Installation & Start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Danach im Browser öffnen: http://127.0.0.1:5000

## Projektstruktur

- `app.py` – Flask-Server mit den Routen (Aufgaben anzeigen, hinzufügen, erledigen)
- `templates/index.html` – die Weboberfläche
- `requirements.txt` – benötigte Python-Pakete
- `tasks.json` – Speicherdatei für Aufgaben (wird automatisch erstellt, nicht versioniert)
