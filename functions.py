# functions.py
import logger  # Importiere den Logger
import sqlite3
import yaml
import random
from faker import Faker
fake = Faker()  # Initialisiere den Faker-Generator

# Logger instanziieren
log = logger.setup_logger()

def load_config(config_path="config.yaml"):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


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