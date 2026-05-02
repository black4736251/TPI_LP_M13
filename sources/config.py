import os
import sys

def base_dir():
    if getattr(sys, "frozen", False): # Avoids using the /tmp folder on Linux distributions
        # Binary path that user executed (./builds/main.bin)
        return os.path.dirname(os.path.abspath(sys.argv[0]))

    # Normal in Python → climb one level from sources/
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = base_dir()

DB_PATH = os.path.join(BASE_DIR, "databases", "database.db")
IMAGES_PATH = os.path.join(BASE_DIR, "images", "program")
REPORTS_PATH = os.path.join(BASE_DIR, "reports", "sales.csv")
SOUNDS_PATH = os.path.join(BASE_DIR, "sounds")