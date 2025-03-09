# db_functions.py
import sqlite3
import os
from functions import load_config
import logger  # Importiere den Logger

# Logger instanziieren
log = logger.setup_logger()


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
        filename TEXT,
        date TEXT,
        lat REAL,
        long REAL,
        city TEXT,
        country TEXT,
        address TEXT
    )
    ''')

    # Erstelle Tabellen für Adresse -> Lat/Long und Lat/Long -> Adresse
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS address_to_coords (
        address TEXT PRIMARY KEY,
        lat REAL,
        long REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS coords_to_address (
        lat REAL,
        long REAL,
        city TEXT,
        country TEXT,
        address TEXT,
        PRIMARY KEY (lat, long)
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

