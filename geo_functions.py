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