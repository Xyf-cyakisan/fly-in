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
        self._graph = graph

    def _set_distance_between_hubs(self):
        min_v = {}
        min_v["x"] = min([hub.coordinates[0] for hub in self._graph.hubs.values()] + [self._graph.start_hub.coordinates[0], self._graph.end_hub.coordinates[0]])
        min_v["y"] = min([hub.coordinates[1] for hub in self._graph.hubs.values()] + [self._graph.start_hub.coordinates[1], self._graph.end_hub.coordinates[1]])
        max_v = {}
        max_v["x"] = max([hub.coordinates[0] for hub in self._graph.hubs.values()] + [self._graph.start_hub.coordinates[0], self._graph.end_hub.coordinates[0]])
        max_v["y"] = max([hub.coordinates[1] for hub in self._graph.hubs.values()] + [self._graph.start_hub.coordinates[1], self._graph.end_hub.coordinates[1]])
        distance_between = {
            "x": (self.screen_x - 35) // abs(max_v["x"] - min_v["x"]),
            "y": (self.screen_y - 35) // abs(max_v["y"] - min_v["y"])
            }
        self.converted_coordinates = {
            "x": {},
            "y": {}
            }
        counter = 0
        for coord in range(max_v["y"], min_v["y"] -1, -1):
            self.converted_coordinates["y"][coord] = (distance_between["y"] * counter if counter != 0 else 35)
            counter += 1
        counter = 0
        for coord in range(min_v["x"], max_v["x"] + 1):
            self.converted_coordinates["x"][coord] = (distance_between["x"] * counter if counter != 0 else 35)
            counter += 1

    def _initialize_pygame(self):
        pygame.init()
        self.screen_x, self.screen_y = (pygame.display.Info().current_w,
                                        pygame.display.Info().current_h)
        self._set_distance_between_hubs()
        pygame.display.set_icon(pygame.image.load("source/assets/fly-in_icone.png"))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Fly-in")
        self.screen.blit(pygame.image.load(f"source/assets/Fly-In_Background_2_{self.screen_x}{self.screen_y}.png"), (0, 0))
        pygame.display.flip()

    def _get_screen_coords(self, x, y):
        return self.converted_coordinates["x"][x], self.converted_coordinates["y"][y]

    def display_graph(self):
        self._initialize_pygame()
        pygame.draw.circle(self.screen, "white", self._get_screen_coords(0, 0), 35)
        pygame.display.flip()
        pygame.draw.circle(self.screen, "black", self._get_screen_coords(0, 0), 30)
        pygame.display.flip()
        running = True
        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
        pygame.quit()


if __name__ == "__main__":
    view = PygameView("prout")
    view.display_graph()
