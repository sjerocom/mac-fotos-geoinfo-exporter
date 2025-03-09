import logger
import db_functions
import functions
import geo_functions

# config.yaml Laden
config = functions.load_config()
mode = config['mode']
db_path = config['database_path']

# Logger verwenden
log = logger.setup_logger()  # Hier ändern wir den Namen von 'logger' auf 'log'

# Initialisiere die Datenbank
db_functions.initialize_db()

if __name__ == "__main__":
    # Beispiel-Daten einfügen (kann später durch echte Foto-Daten ersetzt werden)

    # Wenn im Test/Devmodus, fügen wir 5 zufällige Einträge hinzu
    if mode in ['test','dev']:
        functions.insert_random_entries(5)

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
