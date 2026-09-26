"""
TraceMate device app (week 1 version).

Shows a letter template and records the stylus / mouse path while the student traces.
Run:  python main.py alif
Keys: R = reset, Esc = quit
"""
import json
import sys
import time

import pygame

import config

BOX = config.SCREEN_H - 40
BOX_X = (config.SCREEN_W - BOX) // 2
BOX_Y = (config.SCREEN_H - BOX) // 2


def load_template(name):
    with open(config.TEMPLATES_DIR / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


def to_px(x, y):
    return (BOX_X + x * BOX, BOX_Y + y * BOX)


def to_norm(px, py):
    return [round((px - BOX_X) / BOX, 4), round((py - BOX_Y) / BOX, 4)]


TRACK_COLOR = (214, 228, 247)   # light blue path
DOT_COLOR = (120, 150, 200)     # dotted center line
START_COLOR = (46, 160, 90)     # green start badges
badge_font = None


def draw_template(screen, template):
    global badge_font
    if badge_font is None:
        badge_font = pygame.font.Font(None, 30)

    # 1) soft rounded track + dotted center line
    for stroke in template["strokes"]:
        pts = [to_px(x, y) for x, y in stroke]
        for p in pts:
            pygame.draw.circle(screen, TRACK_COLOR, p, 18)
        for i, p in enumerate(pts):
            if i % 3 == 0:
                pygame.draw.circle(screen, DOT_COLOR, p, 3)

    # 2) numbered start badges on top (1 = first stroke, 2 = second...)
    for number, stroke in enumerate(template["strokes"], 1):
        start = to_px(*stroke[0])
        pygame.draw.circle(screen, START_COLOR, start, 16)
        label = badge_font.render(str(number), True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=start))


def save_attempt(name, strokes, attempt_no):
    config.DATA_DIR.mkdir(exist_ok=True)
    path = config.DATA_DIR / f"attempt_{name}_{int(time.time())}.json"
    data = {"template": name,  "attempt_no": attempt_no, "points": [[to_norm(x, y) for x, y in s] for s in strokes],
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return path


def main(name):
    template = load_template(name)
    pygame.init()
    flags = pygame.FULLSCREEN if config.FULLSCREEN else 0
    screen = pygame.display.set_mode((config.SCREEN_W, config.SCREEN_H), flags)
    pygame.display.set_caption("TraceMate")
    font = pygame.font.Font(None, 26)

    strokes, current, status = [], None, "Trace the letter"
    attempt_no = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                strokes, current, status = [], None, "Trace the letter"
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                current = [e.pos]
            elif e.type == pygame.MOUSEMOTION and current is not None:
                current.append(e.pos)
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and current is not None:
                strokes.append(current)
                current = None
                if len(strokes) >= len(template["strokes"]):
                    attempt_no += 1
                    path = save_attempt(name, strokes, attempt_no)
                    # TODO week 4: score = accuracy.score(template, strokes) and show feedback
                    status = f"Saved {sum(map(len, strokes))} points to {path.name}. R = try again"

        screen.fill((255, 255, 255))
        draw_template(screen, template)
        for s in strokes + ([current] if current else []):
            if len(s) > 1:
                pygame.draw.lines(screen, (30, 90, 200), False, s, 10)
        screen.blit(font.render(status, True, (70, 70, 70)), (12, 10))
        pygame.display.flip()
        clock.tick(120)
    pygame.quit()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "alif")
