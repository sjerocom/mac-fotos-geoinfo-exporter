import sqlite3
import os
import logger  # Der Logger wird importiert
import yaml
import functions
import geo_functions
import photos_functions

# Logger initialisieren
log = logger.setup_logger()


# Konfiguration laden
def load_config(config_path="config.yaml"):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


# Konfiguration laden
config = load_config()
db_path = config['database_path']

# Apple Photos DB Pfad
apple_photos_db_path = os.path.expanduser(config['apple_photos_db'])  # Verwendet den Pfad aus der config


# Verbindung zur Photos-Datenbank herstellen
def connect_to_photos_db():
    try:
        conn = sqlite3.connect(apple_photos_db_path)
        return conn
    except sqlite3.Error as e:
        log.error(f"Fehler beim Verbinden zur Photos DB: {e}")
        return None

def get_photos(anzahl: int = 1000):
    conn = sqlite3.connect(apple_photos_db_path)
    cursor = conn.cursor()
    anzahl = int(anzahl)

    query = """
        SELECT 
            ZASSET.ZFILENAME, 
            ZASSET.ZDATECREATED, 
            ZASSET.ZLATITUDE, 
            ZASSET.ZLONGITUDE
        FROM ZASSET
        WHERE ZASSET.ZLATITUDE IS NOT NULL 
            AND ZASSET.ZLONGITUDE IS NOT NULL
            AND ZASSET.ZLATITUDE != -180.0 
            AND ZASSET.ZLONGITUDE != -180.0
    ORDER BY ZASSET.ZDATECREATED ASC  -- Sortierung nach Erstellungsdatum (ältestes Foto zuerst)
    """

    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    total = len(data)
    fotos = []
    processed_count = 0  # Zähler für bearbeitete Fotos

    # Überprüfen, ob Daten vorhanden sind
    if total > 0:
        for row in data:
            if processed_count >= anzahl:
                break  # Wenn wir die gewünschte Anzahl erreicht haben, stoppen wir die Schleife

            filename, date_created, lat, lon = row

            # Überprüfen, ob das Foto bereits in der Datenbank existiert
            conn = sqlite3.connect(db_path)  # Stelle eine neue Verbindung zur Foto-DB her
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM photos WHERE filename = ?", (filename,))
            existing = cursor.fetchone()
            conn.close()

            if existing:
                continue  # Überspringe dieses Foto, wenn es bereits verarbeitet wurde

            date_created = functions.convert_apple_timestamp(date_created).strftime("%Y-%m-%d")
            city, country, address = geo_functions.get_address_from_coords(lat, lon, db_path)

            # Extrahierte Informationen anzeigen
            log.info(f"Bearbeite Datensatz: {filename}")

            # Hier kannst du das Format anpassen oder zusätzliche Verarbeitung vornehmen
            fotos.append({
                'filename': filename,
                'date_created': date_created,
                'latitude': lat,
                'longitude': lon,
                'city': city,
                'country': country,
                'address': address
            })

            insert_photo(filename, date_created, lat, lon, city, country, address)
            processed_count += 1  # Erhöhe den Zähler für verarbeitete Fotos

        log.info(f"Verarbeitung abgeschlossen. {processed_count} neue Bilder wurden extrahiert.")
    else:
        log.warning("Keine Bilder gefunden, die den Kriterien entsprechen.")

    return fotos


def insert_photo(filename, date, lat, long, city, country, address):
    config = load_config()
    db_path = config['database_path']

    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO photos (filename, date, lat, long, city, country, address)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (filename, date, lat, long, city, country, address))

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()