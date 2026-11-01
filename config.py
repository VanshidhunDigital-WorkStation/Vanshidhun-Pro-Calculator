import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)

MAX_HISTORY = 100