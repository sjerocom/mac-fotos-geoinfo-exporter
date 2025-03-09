# functions.py
import logger  # Importiere den Logger
import sqlite3
import yaml
import geo_functions
import random
from faker import Faker
fake = Faker()  # Initialisiere den Faker-Generator

# Logger instanziieren
log = logger.setup_logger()

def load_config(config_path="config.yaml"):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config()
db_path = config['database_path']

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


def create_test_entries():
        insert_random_entries(5)

        # Beispiel 1: Adresse zu Latitude und Longitude
        address = "Brandenburger Tor"
        city = "Berlin"
        postcode = "10117"
        country = "Germany"

        # Aufruf der Funktion get_lat_long
        lat, long = geo_functions.get_lat_long(address, city, postcode, country, db_path)
        log.info(f"Adresse: {address}, {city}, {postcode}, {country} -> Latitude: {lat}, Longitude: {long}")

        # Beispiel 2: Latitude und Longitude zu Ort und Land
        lat_test = 52.5163
        long_test = 13.3777

        # Aufruf der Funktion get_address_from_coords
        city, country = geo_functions.get_address_from_coords(lat_test, long_test, db_path)
        log.info(f"Koordinaten: ({lat_test}, {long_test}) -> Stadt: {city}, Land: {country}")