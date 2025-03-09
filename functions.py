# functions.py
import logger  # Importiere den Logger
import yaml
from datetime import datetime, timedelta

# Logger instanziieren
log = logger.setup_logger()

def load_config(config_path="config.yaml"):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config()
db_path = config['database_path']

def convert_apple_timestamp(apple_timestamp):
    """Konvertiert den Apple-Zeitstempel in ein lesbares Datum"""
    apple_epoch = datetime(2001, 1, 1)
    return apple_epoch + timedelta(seconds=apple_timestamp)
