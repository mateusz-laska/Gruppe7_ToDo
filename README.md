# Todo Manager

Ein einfacher, konsolenbasierter Todo Manager in Python zur Verwaltung von Aufgaben mit Prioritäten, Kategorien und Status.
Die Anwendung speichert Todos persistent in einer JSON Datei und bietet verschiedene Filter, Such und Verwaltungsfunktionen.

---

## Projektübersicht

Dieses Projekt implementiert eine interaktive Todo Manager Anwendung für die Kommandozeile.
Benutzer können Todos anlegen, anzeigen, filtern, bearbeiten und löschen.
Alle Daten werden lokal gespeichert, sodass der Zustand zwischen Programmausführungen erhalten bleibt.

Repository
[https://github.com/mateusz-laska/Gruppe7_ToDo](https://github.com/mateusz-laska/Gruppe7_ToDo)

---

## Features

- Erstellen neuer Todos mit Titel, Beschreibung, Kategorie und Priorität
- Prioritäten low, medium, high, critical
- Anzeigen aller Todos
- Filtern nach Status offen oder erledigt
- Filtern nach Priorität
- Suche nach Stichwörtern
- Umschalten des Status offen, erledigt
- Anzeigen detaillierter Todo Informationen
- Löschen von Todos mit Sicherheitsabfrage
- Persistente Speicherung in einer JSON Datei

---

## Wichtige Funktionen

load_todos(): 
Liest die Todo Daten aus der Datei todos.json ein und gibt eine Liste von Task Objekten zurück.

save_todos(todos): 
Speichert alle aktuellen Todos persistent in der JSON Datei todos.json.

add_todo(todos): 
Interagiert mit dem Benutzer über die Konsole und erstellt ein neues Todo anhand der Benutzereingaben.

list_todos(todos, status, query): 
Verarbeitet und filtert Todos nach Status oder Suchbegriff und gibt sie formatiert in der Konsole aus.

change_todo_status(todos): 
Ändert den Status eines Todos von offen zu erledigt oder umgekehrt basierend auf der Benutzerinteraktion.

---

## Projektstruktur

```
todo-manager-app
│
├── ToDo_Manager.py
├── task.py
├── todos.json
└── README.md

```

## Installation

Voraussetzungen
- Python 3.9 oder neuer
- Keine externen Bibliotheken notwendig

Repository klonen
```
git clone https://github.com/mateusz-laska/Gruppe7_ToDo
cd Gruppe7_ToDo
```
---

## Verwendung

Anwendung starten
```
python ToDo_Manager.py
```
Nach dem Start erscheint ein interaktives Menue zur Verwaltung aller Todos.

---

## Bedienung

Hauptmenu
- Todos anzeigen, filtern und bearbeiten
- Neues Todo hinzufügen
- Programm beenden

Filter und Verwaltungsoptionen
- Alle Todos anzeigen
- Nur offene oder erledigte Todos anzeigen
- Suche nach Stichwort
- Filtern nach Priorität
- Status eines Todos ändern
- Details eines Todos anzeigen
- Todo löschen

---

## Datenspeicherung

Alle Todos werden in der Datei todos.json gespeichert.
Die Datei wird automatisch erstellt und aktualisiert.

---

## Lizenz

Dieses Projekt dient Ausbildungs und Lernzwecken und ist frei verwendbar.





