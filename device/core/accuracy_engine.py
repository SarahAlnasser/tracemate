"""
Accuracy engine: scores a student's trace against a letter template.
No pygame here, only maths, so it can be tested on its own.

final score = average of
  accuracy: how many of the student's points stay near the letter
  coverage: how much of the letter the student actually traced
"""
import math


def dist_to_segment(p, a, b):
    """shortest distance from point p to the straight line segment between a and b"""
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def dist_to_strokes(p, strokes):
    """shortest distance from point p to any line in a list of strokes"""
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
    """compare the student's strokes to the template; returns (final %, accuracy %, coverage %)"""
    pts = [p for s in student for p in s]
    if len(pts) < 5:
        return 0, 0, 0
    accuracy = sum(dist_to_strokes(p, template) <= tol for p in pts) / len(pts)
    tpts = densify(template)
    coverage = sum(dist_to_strokes(t, student) <= tol for t in tpts) / len(tpts)
    final = round(100 * (accuracy + coverage) / 2)
    return final, round(100 * accuracy), round(100 * coverage)
