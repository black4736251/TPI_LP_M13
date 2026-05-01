import os

BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))

DB_PATH: str = os.path.join(BASE_DIR, "databases", "database.db")
IMAGES_PATH: str = os.path.join(BASE_DIR, "images", "program")
REPORTS_PATH: str = os.path.join(BASE_DIR, "reports", "sales.csv")
SOUNDS_PATH: str = os.path.join(BASE_DIR, "sounds")