"""
Accuracy engine (slice 1, week 4).

Plan for v1 (tolerance-based):
  1. Resample the student's strokes to evenly spaced points (same as the template).
  2. Precision: % of student points within `tolerance` of the template path.
  3. Coverage:  % of template points that have a student point within `tolerance`.
  4. score = 100 * (0.5 * precision + 0.5 * coverage); passed = score >= config.PASS_SCORE
"""


def score(template, student_strokes):
    """Return (score 0-100, passed bool)."""
    raise NotImplementedError("Week 4: accuracy engine v1")
