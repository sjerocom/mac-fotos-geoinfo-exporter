import sqlite3
import os
from functions import load_config


def initialize_db():
    config = load_config()  # Konfiguration laden
    db_path = config['database_path']
    mode = config['mode']

    # Debugging-Ausgabe
    print(f"Running in {mode} mode")  # Zeigt den aktuellen Modus an
    print(f"Database path: {db_path}")  # Zeigt den Pfad zur Datenbank an

    # Stelle sicher, dass der "data" Ordner existiert
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created 'data' directory.")  # Ordner 'data' wurde erstellt

    # Testmodus: Lösche die DB und erstelle sie neu
    if mode == 'test':
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Database {db_path} removed for testing purposes.")  # Zeigt, dass die DB gelöscht wurde
        else:
            print(f"Database {db_path} does not exist. No need to remove.")

    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Erstelle die Tabelle, wenn sie noch nicht existiert
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        lat REAL,
        long REAL,
        location TEXT,
        country TEXT
    )
    ''')

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()

    print(f"Database initialized at {db_path}")

# Beispiel für das Hinzufügen von Fotos zu DB
def insert_photo(date, lat, long, location, country):
    config = load_config()
    db_path = config['database_path']

    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO photos (date, lat, long, location, country)
    VALUES (?, ?, ?, ?, ?)
    ''', (date, lat, long, location, country))

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()

    print(f"Photo data inserted: {date}, {lat}, {long}, {location}, {country}")