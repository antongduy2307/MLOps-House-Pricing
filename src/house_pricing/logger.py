import logging 
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%d-%m-%Y')}.log") 

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def write_separator():
    separator = "-" * 40
    with open(LOG_FILE_PATH, "a") as f:
        f.write(f"\n{separator}\n")
        f.write(f"NEW EXECUTION SESSION STARTED AT: {datetime.now().strftime('%H:%M:%S')}\n")
        f.write(f"{separator}\n")

write_separator()

def get_logger(name):
    print("--------------------------------")
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger