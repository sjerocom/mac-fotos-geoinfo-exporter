# logger.py
import logging
import colorlog

# Logger konfigurieren
def setup_logger():
    # Erstelle einen Logger
    logger = logging.getLogger(__name__)

    # Setze das Log-Level (kann angepasst werden: DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(logging.DEBUG)

    # Erstelle ein Format für die Ausgabe (mit Farbe)
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    # Erstelle einen StreamHandler, um die Logs in der Konsole anzuzeigen
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    # Füge den Handler zum Logger hinzu
    logger.addHandler(ch)

    return logger
