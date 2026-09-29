"""
Widgets: drawing pieces that any screen can reuse.
Right now: converting between template points and pixels, and drawing a letter.
Later: Button (for back / next), progress stars, etc.
"""
import math
import pygame
from config import AREA, OFFSET_X, OFFSET_Y, BLUE, WHITE


# ---------- coordinates ----------
def to_px(p):
    """0-1 template point -> screen pixel"""
    return (OFFSET_X + p[0] * AREA, OFFSET_Y + p[1] * AREA)


def to_norm(p):
    """screen pixel -> 0-1 point"""
    return [round((p[0] - OFFSET_X) / AREA, 4), round((p[1] - OFFSET_Y) / AREA, 4)]


# ---------- letter drawing ----------
def smooth(pts, steps=10):
    """turn a few template points into a smooth curve (Catmull-Rom)"""
    if len(pts) < 3:            # 1 or 2 points can't be curved
        return pts
    p = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(steps):
            t = k / steps; t2 = t * t; t3 = t2 * t
            out.append([0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t
                        + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                        + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)])
    out.append(pts[-1])
    return out


def stamp_points(px, step=2):
    """points every 2 pixels along the line, for drawing an even tube"""
    out = [px[0]]
    for a, b in zip(px, px[1:]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        out += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(1, n + 1)]
    return out


def dashed(screen, px, dash=14, gap=12):
    """draw a dashed line through a list of pixel points: 14 px drawn, 12 px gap, repeating"""
    if len(px) < 2:
        return
    draw_on, left = True, dash
    for a, b in zip(px, px[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        pos = 0
        while pos < seg:
            step = min(left, seg - pos)
            p1 = (a[0] + (b[0] - a[0]) * pos / seg, a[1] + (b[1] - a[1]) * pos / seg)
            p2 = (a[0] + (b[0] - a[0]) * (pos + step) / seg, a[1] + (b[1] - a[1]) * (pos + step) / seg)
            if draw_on:
                pygame.draw.line(screen, BLUE, p1, p2, 4)
            pos += step
            left -= step
            if left <= 0:
                draw_on = not draw_on
                left = dash if draw_on else gap


def draw_template(screen, strokes, font):
    """draw the letter as a hollow blue tube with a dashed guide and numbered start points"""
    curves = [[to_px(p) for p in smooth(s)] for s in strokes]
    for color, r in ((BLUE, 33), (WHITE, 29)):        # outline, then hollow inside
        for c in curves:
            for pt in stamp_points(c):
                pygame.draw.circle(screen, color, pt, r)
    for c in curves:                                  # dashed guide on top
        dashed(screen, c)
    for i, s in enumerate(strokes, 1):                # start numbers
        c = to_px(s[0])
        pygame.draw.circle(screen, BLUE, c, 15)
        t = font.render(str(i), True, WHITE)
        screen.blit(t, t.get_rect(center=c))
