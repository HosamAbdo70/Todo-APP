"""
Kleine Flask-Webanwendung zur Verwaltung von Aufgaben (To-Do-Liste).
Übungsprojekt zum Lernen von Git und GitHub.
"""

import json
import os
from flask import Flask, render_template, request, redirect, url_for

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


if __name__ == "__main__":
    app.run(debug=True)
