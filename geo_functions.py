from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import logger  # Importiere den Logger
import yaml
import sqlite3
import time

# Logger instanziieren
log = logger.setup_logger()

def load_config(config_path="config.yaml"):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


# Nominatim-Geocoder initialisieren
geolocator = Nominatim(user_agent="geo_function_app")


# Funktion: Adresse -> Latitude, Longitude
def get_lat_long(address, city, postcode, country, cache_db_path):
    """Konvertiert eine Adresse in Latitude und Longitude und verwendet den Cache."""
    # Prüfen, ob die Adresse bereits im Cache vorhanden ist
    conn = sqlite3.connect(cache_db_path)
    cursor = conn.cursor()

    # Formatiere die Adresse
    full_address = f"{address}, {postcode} {city}, {country}"

    cursor.execute('''
    SELECT lat, long FROM address_to_coords WHERE address = ?
    ''', (full_address,))

    result = cursor.fetchone()

    if result:
        # Wenn vorhanden, gebe die gecachte Latitude/Longitude zurück
        lat, long = result
        log.info(f"Geocodierte Adresse {full_address} gefunden im Cache: Lat: {lat}, Long: {long}")
        conn.close()
        return lat, long

    # Wenn nicht im Cache, Geocoding durchführen
    location = geolocator.geocode(full_address)

    if location:
        lat, long = location.latitude, location.longitude
        log.info(f"Adresse gefunden: {full_address} -> Lat: {lat}, Long: {long}")

        # Füge die neuen Ergebnisse zum Cache hinzu
        cursor.execute('''
        INSERT OR REPLACE INTO address_to_coords (address, lat, long)
        VALUES (?, ?, ?)
        ''', (full_address, lat, long))

        conn.commit()
    else:
        log.warning(f"Adresse nicht gefunden: {full_address}")
        lat, long = None, None

    conn.close()
    return lat, long


# Funktion: Latitude, Longitude -> Ort, Land
def get_address_from_coords(lat, long, cache_db_path):
    """Konvertiert Latitude und Longitude in eine Adresse und verwendet den Cache."""
    # Prüfen, ob die Koordinaten bereits im Cache vorhanden sind
    conn = sqlite3.connect(cache_db_path)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT city, country, address FROM coords_to_address WHERE lat = ? AND long = ?
    ''', (lat, long))

    result = cursor.fetchone()

    if result:
        # Wenn vorhanden, gebe die gecachte Stadt und das Land zurück
        city, country, address = result
        log.info(f"Geocodierte Koordinaten ({lat}, {long}) gefunden im Cache: Stadt: {city}, Land: {country}")
        conn.close()
        return city, country, address

    # Wenn nicht im Cache, Umkehr-Geocoding durchführen
    location = get_location_with_retry(lat, long)

    if location:
        address = location.address
        # Versuche, mehrere Felder zu durchsuchen, falls "city" leer ist
        city = location.raw.get("address", {}).get("city",
                                                   location.raw.get("address", {}).get("town",
                                                                                       location.raw.get("address",
                                                                                                        {}).get(
                                                                                           "village",
                                                                                           "Unbekannte Stadt")))
        country = location.raw.get("address", {}).get("country", "Unbekanntes Land")

        log.info(f"Koordinaten gefunden: ({lat}, {long}) -> {address}")

        # Füge die neuen Ergebnisse zum Cache hinzu
        cursor.execute('''
        INSERT OR REPLACE INTO coords_to_address (lat, long, city, country, address)
        VALUES (?, ?, ?, ?, ?)
        ''', (lat, long, city, country, address))

        conn.commit()
    else:
        log.warning(f"Keine Adresse gefunden für Koordinaten: ({lat}, {long})")
        city, country, address = "Unbekannte Stadt", "Unbekanntes Land", "Unbekannte Adresse"

    conn.close()
    return city, country, address


def get_location_with_retry(lat, lon, retries=3, delay=5):
    """Versucht, die Anfrage bei einem Timeout erneut zu senden."""
    for attempt in range(retries):
        try:
            location = geolocator.reverse((lat, lon), language="de", timeout=10)
            return location
        except GeocoderTimedOut:
            if attempt < retries - 1:
                log.warning(f"Timeout bei Versuch {attempt+1} von {retries}. Neuer Versuch in {delay} Sekunden.")
                time.sleep(delay)
            else:
                log.error("Maximale Anzahl von Versuchen erreicht. Die Anfrage konnte nicht abgeschlossen werden.")
                return None
        except Exception as e:
            log.error(f"Fehler bei Geocoder-Abfrage: {e}")
            return None
    return None