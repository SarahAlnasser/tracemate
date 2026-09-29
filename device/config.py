"""
Settings shared by the whole device app.
Change a value here and every file that imports it picks it up.
"""

# ---------- screen ----------
WIDTH = 1024                    # matches the Pi touchscreen, 1024x600
HEIGHT = 600
MARGIN = 60                     # empty border around the letter area
AREA = HEIGHT - 2 * MARGIN      # size of the square the letter is drawn in
OFFSET_X = (WIDTH - AREA) / 2   # left edge of that square, so the letter sits in the middle of the wide screen
OFFSET_Y = MARGIN               # top edge of that square
FPS = 120                       # how many times per second the screen is redrawn

# ---------- colours (R, G, B) ----------
BLUE = (107, 189, 211)
WHITE = (255, 255, 255)
INK = (40, 40, 40)

# ---------- tracing rules ----------
PASS_SCORE = 70                 # % needed to pass
DEFAULT_TOLERANCE = 0.05        # used when a template file doesn't give its own tolerance

# ---------- files ----------
DEFAULT_TEMPLATE = "templates/alif.json"  # opened when no template is typed after the command
ATTEMPTS_DIR = "attempts"                 # where scored attempts are saved (relative to where you run the command)
