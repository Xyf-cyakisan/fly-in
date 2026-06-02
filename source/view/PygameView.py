import os
import time
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import random
try:
    import pygame
except ImportError:
    import sys
    print("Error: Pygame module not found, please use "
          "the 'make install' before running the program")
    sys.exit(1)


class PygameView:
    def __init__(self, graph):
        self.graph = graph

    def display(self):
        pygame.init()
        icone = pygame.image.load("source/assets/fly-in_icone.png")
        pygame.display.set_icon(icone)
        screen = pygame.display.set_mode((2560, 1440))
        clock = pygame.time.Clock()
        pygame.display.set_caption("Fly-in")
        screen.fill("black")
        pygame.display.flip()
        pygame.draw.circle(screen, "blue", (100, 100), 80)
        pygame.display.flip()
        running = True
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()


if __name__ == "__main__":
    view = PygameView("prout")
    view.display()
