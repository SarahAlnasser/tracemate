"""
LetterTemplate: one letter loaded from a JSON file in templates/.
Points are stored as 0-1 numbers so the template works on any screen size.
"""
import json
from config import DEFAULT_TOLERANCE


class LetterTemplate:
    def __init__(self, letter, strokes, tolerance, audio=None):
        self.letter = letter          # the Arabic letter itself, e.g. "ب"
        self.strokes = strokes        # list of strokes; each stroke is a list of [x, y] points (0-1)
        self.tolerance = tolerance    # how far (0-1) a point can be from the letter and still count
        self.audio = audio            # name of the instruction sound file (not played yet)

    @classmethod
    def load(cls, path):
        """read a template JSON file and return a LetterTemplate"""
        with open(path, encoding="utf-8") as f:   # utf-8 so the Arabic letter reads correctly
            data = json.load(f)
        return cls(
            letter=data["letter"],
            strokes=data["strokes"],
            tolerance=data.get("tolerance", DEFAULT_TOLERANCE),
            audio=data.get("audio"),
        )
