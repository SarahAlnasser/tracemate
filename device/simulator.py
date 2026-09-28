"""

Run:   python device/simulator.py templates/b.json
Keys:  hold left mouse = trace (each press = new stroke)
       ENTER = score    R = retry    ESC = quit
"""
import json, math, os, sys, time
import pygame

SIZE = 700                 
MARGIN = 60                # empty border around the letter area
BLUE = (107, 189, 211)
WHITE = (255, 255, 255)
INK = (40, 40, 40)
PASS_SCORE = 70            # % needed to pass


# ---------- coordinates ----------
def to_px(p):
    """0-1 template point -> screen pixel"""
    area = SIZE - 2 * MARGIN
    return (MARGIN + p[0] * area, MARGIN + p[1] * area)

def to_norm(p):
    """screen pixel -> 0-1 point"""
    area = SIZE - 2 * MARGIN
    return [round((p[0] - MARGIN) / area, 4), round((p[1] - MARGIN) / area, 4)]


# ---------- scoring ----------
def dist_to_segment(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def dist_to_strokes(p, strokes):
    best = float("inf")
    for s in strokes:
        if len(s) == 1:
            best = min(best, math.hypot(p[0] - s[0][0], p[1] - s[0][1]))
        for a, b in zip(s, s[1:]):
            best = min(best, dist_to_segment(p, a, b))
    return best

def densify(strokes, step=0.01):
    """add points along the template so coverage is checked everywhere"""
    out = []
    for s in strokes:
        for a, b in zip(s, s[1:]):
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
            out += [[a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n] for i in range(n)]
        out.append(s[-1])
    return out

def score(template, student, tol):
    pts = [p for s in student for p in s]
    if len(pts) < 5:
        return 0, 0, 0
    # accuracy: how many of the student's points stay near the letter
    accuracy = sum(dist_to_strokes(p, template) <= tol for p in pts) / len(pts)
    # coverage: how much of the letter the student actually traced
    tpts = densify(template)
    coverage = sum(dist_to_strokes(t, student) <= tol for t in tpts) / len(tpts)
    final = round(100 * (accuracy + coverage) / 2)
    return final, round(100 * accuracy), round(100 * coverage)


# ---------- drawing ----------
def smooth(pts, steps=10):
    """turn a few template points into a smooth curve (Catmull-Rom)"""
    if len(pts) < 3:
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

def draw_template(screen, strokes, font):
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

def dashed(screen, px, dash=14, gap=12):
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


# ---------- main ----------
def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "templates/b.json"
    with open(path, encoding="utf-8") as f:
        tpl = json.load(f)
    strokes, tol = tpl["strokes"], tpl.get("tolerance", 0.05)

    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("TraceMate simulator - " + os.path.basename(path))
    font = pygame.font.SysFont("arial", 18, bold=True)
    big = pygame.font.SysFont("arial", 26, bold=True)

    student, drawing, result, attempt_no = [], False, None, 1
    clock = pygame.time.Clock()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit(); return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and result is None:
                drawing = True
                student.append([to_norm(e.pos)])
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                drawing = False
            if e.type == pygame.MOUSEMOTION and drawing:
                student[-1].append(to_norm(e.pos))
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN and result is None:
                final, acc, cov = score(strokes, student, tol)
                result = (final, acc, cov)
                save_attempt(tpl["letter"], attempt_no, final, final >= PASS_SCORE, student)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                student, result = [], None
                attempt_no += 1

        screen.fill(WHITE)
        draw_template(screen, strokes, font)
        for s in student:                                    # student's ink
            if len(s) > 1:
                pygame.draw.lines(screen, INK, False, [to_px(p) for p in s], 5)

        if result:
            final, acc, cov = result
            msg = f"Score {final}%  ({'PASS' if final >= PASS_SCORE else 'TRY AGAIN'})"
            screen.blit(big.render(msg, True, INK), (20, 15))
            screen.blit(font.render(f"accuracy {acc}%   coverage {cov}%   R = retry", True, INK), (20, SIZE - 35))
        else:
            screen.blit(font.render(f"Attempt {attempt_no}: trace, then press ENTER", True, INK), (20, 15))

        pygame.display.flip()
        clock.tick(120)


def save_attempt(letter, attempt_no, score_val, passed, student):
    os.makedirs("attempts", exist_ok=True)
    data = {
        "letter": letter,
        "attempt_no": attempt_no,
        "score": score_val,
        "passed": passed,
        "points": student,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    name = f"attempts/{time.strftime('%Y%m%d_%H%M%S')}_{attempt_no}.json"
    with open(name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("saved", name, "score", score_val)


if __name__ == "__main__":
    main()