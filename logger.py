# logger.py
import logging
import sys
import colorlog

# Logger konfigurieren
def setup_logger():
    logger = logging.getLogger(__name__)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
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
        # Hier wird sys.stdout verwendet:
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger