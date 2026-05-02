import os
import sys

def base_dir():
    if getattr(sys, "frozen", False):
        # Caminho do binário que o utilizador executou (./builds/main.bin)
        return os.path.dirname(os.path.abspath(sys.argv[0]))

    # Python normal → subir um nível a partir de sources/
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = base_dir()

DB_PATH = os.path.join(BASE_DIR, "databases", "database.db")
IMAGES_PATH = os.path.join(BASE_DIR, "images", "program")
REPORTS_PATH = os.path.join(BASE_DIR, "reports", "sales.csv")
SOUNDS_PATH = os.path.join(BASE_DIR, "sounds")