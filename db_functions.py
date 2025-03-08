# db_functions.py
import sqlite3
import os
from functions import load_config
import logger  # Importiere den Logger
import random
from faker import Faker

# Logger instanziieren
log = logger.setup_logger()

fake = Faker()  # Initialisiere den Faker-Generator

# Funktion zum Erstellen einer neuen DB
def create_db(db_path):
    """Erstellt eine neue Datenbank mit der angegebenen Pfad."""
    log.info(f"Creating new database at {db_path}")
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

    log.info(f"Database created at {db_path}")


# Funktion zum Löschen und Erstellen der DB
def delete_and_create_db(db_path):
    """Löscht die bestehende DB und erstellt sie neu."""
    if os.path.exists(db_path):
        os.remove(db_path)
        log.info(f"Database {db_path} removed for testing purposes.")  # Zeigt, dass die DB gelöscht wurde
    else:
        log.info(f"Database {db_path} does not exist. Creating a new one.")

    # Erstelle die DB nach dem Löschen oder wenn sie nicht existiert
    create_db(db_path)


# Funktion zum Überprüfen, ob die DB existiert
def check_db_exists(db_path):
    """Überprüft, ob die Datenbank existiert."""
    return os.path.exists(db_path)


# Funktion zum Initialisieren der DB
def initialize_db():
    config = load_config()  # Konfiguration laden
    db_path = config['database_path']
    mode = config['mode']

    # Logger-Ausgabe
    log.info(f"Running in {mode} mode")  # Zeigt den aktuellen Modus an
    log.info(f"Database path: {db_path}")  # Zeigt den Pfad zur Datenbank an

    # Stelle sicher, dass der "data" Ordner existiert
    if not os.path.exists('data'):
        os.makedirs('data')
        log.info("Created 'data' directory.")  # Ordner 'data' wurde erstellt

    # Modus "test"
    if mode == 'test':
        if check_db_exists(db_path):
            delete_and_create_db(db_path)
        else:
            create_db(db_path)

    # Modus "prod"
    elif mode == 'prod':
        if not check_db_exists(db_path):
            create_db(db_path)
        else:
            log.info(f"Database {db_path} already exists. No action taken.")

    log.info(f"Database initialization complete at {db_path}")


# Funktion zum Hinzufügen von zufälligen Einträgen, die die bestehende insert_photo verwenden
def insert_random_entries(num_entries):
    log.info(f"Inserting {num_entries} random entries into the database.")

    for _ in range(num_entries):
        random_date = fake.date_this_decade()  # Zufälliges Datum
        random_lat = round(random.uniform(-90.0, 90.0), 6)  # Zufällige Latitude
        random_long = round(random.uniform(-180.0, 180.0), 6)  # Zufällige Longitude
        random_location = fake.city()  # Zufälliger Ort
        random_country = fake.country()  # Zufälliges Land

        # Verwende die bestehende insert_photo Funktion, um die Einträge hinzuzufügen
        insert_photo(random_date, random_lat, random_long, random_location, random_country)

    log.info(f"{num_entries} random entries inserted into the database.")

# Funktion zum Hinzufügen von echten Fotos zu DB (bereits vorhanden)
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

    log.info(f"Photo data inserted: {date}, {lat}, {long}, {location}, {country}")