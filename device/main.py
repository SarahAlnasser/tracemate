"""
TraceMate device app: the entry point (like @main in Swift).
It opens the window, picks the screen to show, and runs the loop.

Run (from the tracemate folder):
       python3 device/main.py templates/alif.json
       python3 device/main.py templates/b.json
Keys:  hold left mouse = trace (each press = new stroke)
       ENTER = score    R = retry    ESC = quit
"""
import os, sys
import pygame
from config import WIDTH, HEIGHT, FPS, DEFAULT_TEMPLATE
from core.letter_template import LetterTemplate
from screens.tracing import TracingScreen


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TEMPLATE
    template = LetterTemplate.load(path)

    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TraceMate simulator - " + os.path.basename(path))
    clock = pygame.time.Clock()

    current = TracingScreen(template)   # the screen being shown; later this switches between idle/start/tracing/end

    while True:                          # main loop: runs until the user quits
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit(); return
            current.handle_event(e)      # everything else goes to the current screen

        current.draw(window)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
