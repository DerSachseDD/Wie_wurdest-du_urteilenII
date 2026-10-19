# Wie würdest du urteilen?

Ein modularer Flask-Starter für eine deutschsprachige Fall-Schätzungs-Webseite. Nutzer:innen schätzen Geldstrafe und Freiheitsstrafe, geben eine Stimme ab und vergleichen sie mit dem Durchschnitt.

## Voraussetzungen

- Python 3.12
- PyCharm
- Internetzugang für Tailwind CSS und Chart.js via CDN

## Start in PyCharm

1. Öffne den Ordner dieses Projekts in PyCharm.
2. Lege einen Python-3.12-Virtualenv als Interpreter an.
3. Öffne das Terminal in PyCharm und installiere die Abhängigkeiten:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Starte das Projekt:

   ```bash
   python run.py
   ```

5. Öffne die lokale Adresse, die Flask im Terminal ausgibt (normalerweise `http://127.0.0.1:5000`).

Die SQLite-Datenbank wird beim ersten Start unter `instance/judgement.db` angelegt. Fälle werden beim Start aus `app/cases/data.json` eingefügt bzw. aktualisiert.

## Neue Fälle hinzufügen

Bearbeite ausschließlich `app/cases/data.json` und füge ein Objekt mit einer eindeutigen `id` hinzu:

```json
{
  "id": 4,
  "title": "Kurzer Falltitel",
  "description": "Sachverhalt in wenigen Sätzen.",
  "real_sentence": "Demo-Fall: 250 € Geldstrafe",
  "category": "theft",
  "real_fine": 250,
  "real_jail": 0
}
```

Pflichtfelder entsprechend der gewünschten Grundstruktur sind `id`, `title`, `description`, `real_sentence` und `category`. `real_fine` und `real_jail` steuern die Diagramme und sollten ebenfalls angegeben werden. Geldwerte sind Euro, Freiheitsstrafen sind Jahre. IDs müssen eindeutig sein. Starte die App neu, damit JSON-Änderungen synchronisiert werden.

## Routen

- `GET /` – zufälliger Fall
- `POST /api/vote` – validiert und speichert die Schätzung; leitet Browser zur Ergebnisseite weiter
- `GET /result/<case_id>` – Ergebnis und Chart.js-Diagramme
- `GET /api/stats/<case_id>` – Durchschnittswerte als JSON
- `GET /health` – einfacher Health Check

## Architektur

- `app/__init__.py`: Flask-App-Factory, Datenbankinitialisierung
- `app/models.py`: SQLAlchemy-Modelle `Case` und `Vote`
- `app/routes.py`: Blueprint und HTTP-Routen
- `app/statistics.py`: getrennte Funktion für Durchschnittsberechnung und Satzformatierung
- `app/cases/case_loader.py`: JSON laden und mit der Datenbank synchronisieren
- `app/cases/data.json`: editierbare Falldaten
- `app/templates/`: Jinja-Templates
- `app/static/style.css`: kleine CSS-Ergänzungen

## Wichtige Hinweise vor Veröffentlichung

Die enthaltenen Fälle sind **Demo-Beispiele**. Die angezeigten Beträge sind keine verifizierten echten Gerichtsurteile. Ergänze vor dem öffentlichen Einsatz nachvollziehbare Quellen und prüfe jeden Fall juristisch. Die Demo zeigt einen Geldwert als Geldstrafe/Bußgeld vereinfachend in einem gemeinsamen Slider; rechtlich sind Geldstrafe und Bußgeld unterschiedliche Sanktionen.

Für einen produktiven Einsatz solltest du außerdem einen zufälligen, geheimen `SECRET_KEY` als Umgebungsvariable setzen, CSRF-Schutz ergänzen, Rate-Limiting/Spam-Schutz einrichten, Datenschutz- und Impressumstexte ergänzen und Debug-Modus deaktivieren. Plausible Analytics ist im `base.html` als Kommentar-Platzhalter vorbereitet; es wird nichts getrackt.
