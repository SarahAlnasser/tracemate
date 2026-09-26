"""
TraceMate template maker
------------------------
Trace a letter with the mouse (or stylus) and save it as a JSON template.

Usage:
    python template_maker.py --letter ا --name alif --font NotoNaskhArabic-Regular.ttf
    python template_maker.py --view templates/alif.json      # check a saved template

Controls:
    Draw        hold mouse button and drag (one drag = one stroke)
    U           undo last stroke
    C           clear all strokes
    S           save to templates/<name>.json
    Esc         quit

Draw strokes in the correct writing order and direction
(e.g. ا top to bottom; ب body right to left, then the dot).
"""

import argparse
import json
import math
import os

import pygame

WIDTH, HEIGHT = 1024, 600          # Raspberry Pi 7" screen size
BOX = HEIGHT - 40                 # square drawing area, same scale for x and y
BOX_X = (WIDTH - BOX) // 2
BOX_Y = (HEIGHT - BOX) // 2
MIN_STEP_PX = 3                   # ignore tiny mouse jitter
SPACING = 0.01                    # distance between saved points (normalized)


def resample(stroke, spacing=SPACING):
    """Return points spaced evenly along the stroke, so fast and slow drawing give the same template."""
    if len(stroke) < 2:
        return [list(p) for p in stroke]
    out = [list(stroke[0])]
    carry = 0.0
    for (x1, y1), (x2, y2) in zip(stroke, stroke[1:]):
        seg = math.dist((x1, y1), (x2, y2))
        if seg == 0:
            continue
        d = spacing - carry
        while d <= seg:
            t = d / seg
            out.append([x1 + t * (x2 - x1), y1 + t * (y2 - y1)])
            d += spacing
        carry = seg - (d - spacing)
    if math.dist(out[-1], stroke[-1]) > spacing / 2:
        out.append(list(stroke[-1]))
    return out


def to_norm(px, py):
    """Screen pixels -> 0..1 inside the drawing box."""
    return ((px - BOX_X) / BOX, (py - BOX_Y) / BOX)


def to_px(nx, ny):
    """0..1 inside the drawing box -> screen pixels."""
    return (BOX_X + nx * BOX, BOX_Y + ny * BOX)


def build_template(letter, strokes_px, tolerance, audio):
    strokes = []
    for s in strokes_px:
        norm = [to_norm(x, y) for x, y in s]
        strokes.append([[round(x, 4), round(y, 4)] for x, y in resample(norm)])
    return {"letter": letter, "strokes": strokes, "tolerance": tolerance, "audio": audio}


def draw_guide(screen, font, letter):
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (220, 220, 220), (BOX_X, BOX_Y, BOX, BOX), 1)
    if font and letter:
        glyph = font.render(letter, True, (225, 225, 225))
        screen.blit(glyph, glyph.get_rect(center=(WIDTH // 2, HEIGHT // 2)))


def draw_strokes(screen, strokes, color=(30, 90, 200), width=6):
    for s in strokes:
        if len(s) > 1:
            pygame.draw.lines(screen, color, False, s, width)
        elif s:
            pygame.draw.circle(screen, color, s[0], width)
        if s:
            pygame.draw.circle(screen, (0, 170, 80), s[0], 8)   # green = stroke start


def run_maker(args):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"TraceMate template maker: {args.name}")
    font = pygame.font.Font(args.font, int(BOX * 0.8)) if args.font else None
    small = pygame.font.Font(None, 24)

    strokes, current, message = [], None, "Trace the letter. S = save, U = undo, C = clear"
    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                current = [e.pos]
            elif e.type == pygame.MOUSEMOTION and current is not None:
                if math.dist(current[-1], e.pos) >= MIN_STEP_PX:
                    current.append(e.pos)
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and current is not None:
                strokes.append(current)
                current = None
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key == pygame.K_u and strokes:
                    strokes.pop()
                elif e.key == pygame.K_c:
                    strokes.clear()
                elif e.key == pygame.K_s and strokes:
                    tpl = build_template(args.letter, strokes, args.tolerance, f"{args.name}_instruction.wav")
                    os.makedirs(args.out, exist_ok=True)
                    path = os.path.join(args.out, f"{args.name}.json")
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(tpl, f, ensure_ascii=False, indent=2)
                    message = f"Saved {path}  ({len(tpl['strokes'])} strokes)"

        draw_guide(screen, font, args.letter)
        draw_strokes(screen, strokes + ([current] if current else []))
        screen.blit(small.render(message, True, (60, 60, 60)), (10, 8))
        pygame.display.flip()
        clock.tick(120)
    pygame.quit()


def run_viewer(path):
    with open(path, encoding="utf-8") as f:
        tpl = json.load(f)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Viewing {path}")
    small = pygame.font.Font(None, 24)
    strokes = [[to_px(x, y) for x, y in s] for s in tpl["strokes"]]
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False
        draw_guide(screen, None, None)
        # show the tolerance band as a light halo around the path
        band = max(2, int(tpl["tolerance"] * BOX * 2))
        draw_strokes(screen, strokes, color=(215, 230, 250), width=band)
        draw_strokes(screen, strokes)
        info = f"{tpl['letter']}  strokes: {len(strokes)}  points: {sum(map(len, strokes))}  tolerance: {tpl['tolerance']}"
        screen.blit(small.render(info, True, (60, 60, 60)), (10, 8))
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Make TraceMate letter templates")
    p.add_argument("--letter", help="the letter to trace, e.g. ا")
    p.add_argument("--name", help="file name, e.g. alif")
    p.add_argument("--font", help="path to an Arabic .ttf font for the grey guide letter")
    p.add_argument("--tolerance", type=float, default=0.05, help="allowed distance from the path (0..1)")
    p.add_argument("--out", default="templates", help="output folder")
    p.add_argument("--view", help="open a saved template instead of making one")
    a = p.parse_args()
    if a.view:
        run_viewer(a.view)
    elif a.letter and a.name:
        run_maker(a)
    else:
        p.error("use --letter and --name to make a template, or --view to check one")
