import logging
import os

# Logger config
LOG_DIR = os.path.join(os.getcwd(), "log")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# Normal logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log/log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(threadName)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
