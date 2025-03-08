import logger
import db_functions
import functions

# config.yaml Laden
config = functions.load_config()

# Logger verwenden
log = logger.setup_logger()  # Hier ändern wir den Namen von 'logger' auf 'log'

# Initialisiere die Datenbank
db_functions.initialize_db()

if __name__ == "__main__":
    # Beispiel-Daten einfügen (kann später durch echte Foto-Daten ersetzt werden)
    db_functions.insert_photo('2025-03-08', 48.2082, 16.3738, 'xx', 'xxx')