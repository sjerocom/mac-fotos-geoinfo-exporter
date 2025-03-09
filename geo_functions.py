from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import logging

# Logger initialisieren
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Nominatim-Geocoder initialisieren
geolocator = Nominatim(user_agent="geo_function_app")


# Funktion: Adresse -> Latitude, Longitude
def get_lat_long(address, city, postcode, country):
    """Konvertiert eine Adresse (mit Hausnummer, PLZ, Ort, Land) in Latitude und Longitude"""
    full_address = f"{address}, {postcode} {city}, {country}"

    try:
        # Geocoding: Adresse in Koordinaten umwandeln
        location = geolocator.geocode(full_address)

        if location:
            log.info(f"Adresse gefunden: {full_address} -> Lat: {location.latitude}, Long: {location.longitude}")
            return location.latitude, location.longitude
        else:
            log.warning(f"Adresse nicht gefunden: {full_address}")
            return None, None

    except GeocoderTimedOut:
        log.error("Geocoder-TimedOut-Fehler: Der Geocoding-Dienst hat die Anfrage nicht rechtzeitig bearbeitet.")
        return None, None
    except Exception as e:
        log.error(f"Fehler beim Geocoding: {e}")
        return None, None


# Funktion: Latitude, Longitude -> Ort, Land
def get_address_from_coords(lat, long):
    """Konvertiert Latitude und Longitude in den zugehörigen Ort und Land"""
    try:
        # Umkehr-Geocoding: Koordinaten in Adresse umwandeln
        location = geolocator.reverse((lat, long), language="de")

        if location:
            address = location.address
            city = location.raw.get("address", {}).get("city", "Unbekannte Stadt")
            country = location.raw.get("address", {}).get("country", "Unbekanntes Land")
            log.info(f"Koordinaten gefunden: {lat}, {long} -> {address}")
            return city, country
        else:
            log.warning(f"Keine Adresse gefunden für Koordinaten: {lat}, {long}")
            return "Unbekannte Stadt", "Unbekanntes Land"

    except GeocoderTimedOut:
        log.error("Geocoder-TimedOut-Fehler: Der Umkehr-Geocoding-Dienst hat die Anfrage nicht rechtzeitig bearbeitet.")
        return "Unbekannte Stadt", "Unbekanntes Land"
    except Exception as e:
        log.error(f"Fehler beim Umkehr-Geocoding: {e}")
        return "Unbekannte Stadt", "Unbekanntes Land"