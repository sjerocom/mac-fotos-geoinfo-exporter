import logger
import db_functions
import functions
import photos_functions

# config.yaml Laden
config = functions.load_config()
mode = config['mode']
db_path = config['database_path']
photos_to_get_from_library = config['photos_to_get_from_library']

# Logger verwenden
log = logger.setup_logger()  # Hier ändern wir den Namen von 'logger' auf 'log'

# Initialisiere die Datenbank
db_functions.initialize_db()

if __name__ == "__main__":

    photos_functions.get_photos(photos_to_get_from_library)


