"""
Kleine Flask-Webanwendung zur Verwaltung von Aufgaben (To-Do-Liste).
Übungsprojekt zum Lernen von Git und GitHub.
"""

import json
import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

import watcher

load_dotenv()  # liest die .env Datei mit den API-Keys ein

app = Flask(__name__)
DATEI = "tasks.json"


def lade_aufgaben():
    if not os.path.exists(DATEI):
        return []
    with open(DATEI, "r", encoding="utf-8") as f:
        return json.load(f)


def speichere_aufgaben(aufgaben):
    with open(DATEI, "w", encoding="utf-8") as f:
        json.dump(aufgaben, f, indent=2, ensure_ascii=False)


@app.route("/")
def index():
    aufgaben = lade_aufgaben()
    return render_template("index.html", aufgaben=aufgaben)


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "").strip()
    if text:
        aufgaben = lade_aufgaben()
        aufgaben.append({"text": text, "erledigt": False})
        speichere_aufgaben(aufgaben)
    return redirect(url_for("index"))


@app.route("/done/<int:index>", methods=["POST"])
def done(index):
    aufgaben = lade_aufgaben()
    if 0 <= index < len(aufgaben):
        aufgaben[index]["erledigt"] = True
        speichere_aufgaben(aufgaben)
    return redirect(url_for("index"))


@app.route("/rate/<int:index>", methods=["POST"])
def rate(index):
    bewertung = request.form.get("bewertung", type=int)
    aufgaben = lade_aufgaben()
    if 0 <= index < len(aufgaben) and bewertung in (1, 2, 3, 4, 5):
        aufgaben[index]["bewertung"] = bewertung
        speichere_aufgaben(aufgaben)
    return redirect(url_for("index"))


@app.route("/ebay")
def ebay_liste():
    artikel = watcher.lade_artikel()
    return render_template("ebay.html", artikel=artikel)


@app.route("/ebay/add", methods=["POST"])
def ebay_hinzufuegen():
    item_id = request.form.get("item_id", "").strip()
    if item_id:
        ergebnis = watcher.artikel_hinzufuegen(item_id)
        if ergebnis is None:
            return "Artikel konnte nicht gefunden werden. Item-ID prüfen.", 400
    return redirect(url_for("ebay_liste"))


if __name__ == "__main__":
    # Hintergrund-Watcher starten, der die eBay-Artikel überwacht
    # und bei 15/10/5 Minuten Restzeit eine Telegram-Nachricht sendet
    watcher.starten()
    # use_reloader=False, damit der Watcher-Thread nicht doppelt startet
    app.run(debug=True, use_reloader=False)
