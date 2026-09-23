"""Device settings. Change API_URL to the laptop running XAMPP."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT.parent / "templates"
AUDIO_DIR = ROOT / "audio"
DATA_DIR = ROOT / "data"              # saved attempts + offline queue

SCREEN_W, SCREEN_H = 800, 480         # Raspberry Pi 7" touchscreen
FULLSCREEN = False                    # set True on the Pi

API_URL = "http://192.168.1.10/tracemate/backend/api"
DEVICE_KEY = "dev-key-1"              # matches devices.api_key in the database

MAX_ATTEMPTS = 3                      # retries before moving to the next letter
PASS_SCORE = 70                       # score (0-100) needed to pass
