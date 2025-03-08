import logger
import db_functions
import functions

# config.yaml Laden
config = functions.load_config()
mode = config['mode']

# Logger verwenden
log = logger.setup_logger()  # Hier ändern wir den Namen von 'logger' auf 'log'

# Initialisiere die Datenbank
db_functions.initialize_db()

if __name__ == "__main__":
    # Beispiel-Daten einfügen (kann später durch echte Foto-Daten ersetzt werden)

    # Wenn im Test/Devmodus, fügen wir 5 zufällige Einträge hinzu
    if mode in ['test','dev']:
        db_functions.insert_random_entries(5)