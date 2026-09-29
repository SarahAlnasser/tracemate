"""
Tracing screen: shows one letter, lets the student trace it, then scores it.
It owns its own state (the student's strokes, the score, the attempt number)
and has two jobs that main.py calls every frame:
  handle_event(e)  -> react to mouse / keys
  draw(screen)     -> draw everything from the current state
"""
import pygame
from config import WHITE, INK, HEIGHT, PASS_SCORE
from core.accuracy_engine import score
from core.storage import save_attempt
from screens.widgets import to_px, to_norm, draw_template


class TracingScreen:
    def __init__(self, template):
        self.template = template                              # the LetterTemplate being traced
        self.font = pygame.font.SysFont("arial", 18, bold=True)
        self.big = pygame.font.SysFont("arial", 26, bold=True)
        self.student = []         # the student's strokes (each a list of 0-1 points)
        self.drawing = False      # is the mouse / stylus held down right now
        self.result = None        # (final, accuracy, coverage) after ENTER, None before
        self.attempt_no = 1

    # ---------- input ----------
    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.result is None:
            self.drawing = True
            self.student.append([to_norm(e.pos)])             # start a new stroke
        if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            self.drawing = False
        if e.type == pygame.MOUSEMOTION and self.drawing:
            self.student[-1].append(to_norm(e.pos))           # keep adding to the current stroke
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN and self.result is None:
            self.submit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
            self.retry()

    # ---------- actions ----------
    def submit(self):
        """score the current trace and save it"""
        t = self.template
        self.result = score(t.strokes, self.student, t.tolerance)
        final = self.result[0]
        save_attempt(t.letter, self.attempt_no, final, final >= PASS_SCORE, self.student)

    def retry(self):
        """clear the trace and start a new attempt"""
        self.student, self.result = [], None
        self.attempt_no += 1

    # ---------- drawing ----------
    def draw(self, screen):
        screen.fill(WHITE)
        draw_template(screen, self.template.strokes, self.font)
        for s in self.student:                                # student's ink
            if len(s) > 1:
                pygame.draw.lines(screen, INK, False, [to_px(p) for p in s], 5)

        if self.result:
            final, acc, cov = self.result
            msg = f"Score {final}%  ({'PASS' if final >= PASS_SCORE else 'TRY AGAIN'})"
            screen.blit(self.big.render(msg, True, INK), (20, 15))
            screen.blit(self.font.render(f"accuracy {acc}%   coverage {cov}%   R = retry", True, INK), (20, HEIGHT - 35))
        else:
            screen.blit(self.font.render(f"Attempt {self.attempt_no}: trace, then press ENTER", True, INK), (20, 15))
