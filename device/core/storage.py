"""
Storage: saves attempts on the device as JSON files.
Later this is where offline saving + syncing to the backend will live.
"""
import json, os, time
from config import ATTEMPTS_DIR


def save_attempt(letter, attempt_no, score_val, passed, student):
    """save one attempt as a JSON file inside the attempts folder"""
    os.makedirs(ATTEMPTS_DIR, exist_ok=True)
    data = {
        "letter": letter,
        "attempt_no": attempt_no,
        "score": score_val,
        "passed": passed,
        "points": student,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    name = f"{ATTEMPTS_DIR}/{time.strftime('%Y%m%d_%H%M%S')}_{attempt_no}.json"
    with open(name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("saved", name, "score", score_val)
