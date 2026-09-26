"""
Rough trace-to-template comparison (week 1 prototype).
This is NOT the real accuracy engine. It only proves the pipeline works:
saved trace -> compare with template -> score.

Run from the device folder:  python tools/compare.py
It scores the newest saved attempt in data/.
"""
import json
import math
import sys
from pathlib import Path

DEVICE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = DEVICE_DIR / "data"
TEMPLATES_DIR = DEVICE_DIR.parent / "templates"


def newest_attempt():
    files = sorted(DATA_DIR.glob("attempt_*.json"), key=lambda f: f.stat().st_mtime)
    if not files:
        sys.exit("No saved attempts in data/. Run main.py and trace a letter first.")
    return files[-1]


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def flatten(strokes):
    """Turn a list of strokes into one list of points."""
    return [point for stroke in strokes for point in stroke]


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def percent_close(points, targets, tolerance):
    """What % of `points` have at least one target point within `tolerance`."""
    close = 0
    for p in points:
        nearest = min(distance(p, t) for t in targets)
        if nearest <= tolerance:
            close += 1
    return 100 * close / len(points)


def main():
    attempt_file = newest_attempt()
    attempt = load_json(attempt_file)
    template = load_json(TEMPLATES_DIR / f"{attempt['template']}.json")

    student = flatten(attempt["points"])
    letter = flatten(template["strokes"])
    tolerance = template["tolerance"]

    # Precision: did the student stay on the line?
    precision = percent_close(student, letter, tolerance)
    # Coverage: did the student trace the WHOLE letter?
    coverage = percent_close(letter, student, tolerance)
    score = (precision + coverage) / 2

    print(f"File:      {attempt_file.name}")
    print(f"Letter:    {attempt['template']} (attempt {attempt.get('attempt_no', '?')})")
    print(f"Precision: {precision:.1f}%  (student points on the line)")
    print(f"Coverage:  {coverage:.1f}%  (letter points the student covered)")
    print(f"Score:     {score:.1f} / 100")


if __name__ == "__main__":
    main()