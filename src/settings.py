import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = os.path.join(BASE_DIR, 'db', 'photo-booth.sqlite')


