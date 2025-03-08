import logger
import db_functions
import functions

# config.yaml Laden
config = functions.load_config()

# Logger verwenden
logger = logger.setup_logger()

# Initialisiere die Datenbank
db_functions.initialize_db()

# Beispiel-Daten einfügen (kann später durch echte Foto-Daten ersetzt werden)
db_functions.insert_photo('2025-03-08', 48.2082, 16.3738, 'xx', 'xxx')

if __name__ == "__main__":
    logger.info("Das ist eine Info-Nachricht aus dem main.py-Skript.")
