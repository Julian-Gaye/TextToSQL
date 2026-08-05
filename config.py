import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "La variable GOOGLE_API_KEY n'a pas été trouvée dans le fichier .env !"
    )

DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "demo_database.db"