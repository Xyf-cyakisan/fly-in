import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
try:
    import pygame
except ImportError:
    import sys
    print("Error: Pygame module not found, please use "
          "the 'make install' before running the program")
    sys.exit(1)


class PygameView:

    COLORS: dict[str, str | tuple[int, int, int]] = {
        'default': "white",
        "black": (40, 40, 45),
        "blue": (0, 128, 255),
        "brown": (120, 70, 30),
        "crimson": (220, 20, 60),
        "cyan": (43, 220, 255),
        "darkred": (139, 0, 0),
        "gold": (255, 215, 0),
        "green": (50, 200, 80),
        "lime": (150, 255, 50),
        "magenta": (200, 0, 200),
        "maroon": (128, 0, 0),
        "orange": (255, 128, 0),
        "purple": (160, 60, 200),
        "rainbow": (255, 100, 150),
        "red": (220, 50, 50),
        "violet": (130, 80, 220),
        "yellow": (220, 200, 30),
        "grey": (192, 192, 192)
    }

    def __init__(self, graph):
        self._graph = graph

    def _draw_circle(self, color, coords):
        around = self.COLORS["black"]
        if color == around:
            around = self.COLORS["default"]
        pygame.draw.circle(self.screen, around, self._get_screen_coords(*coords), 35)
        pygame.draw.circle(self.screen, color, self._get_screen_coords(*coords), 30)
        pygame.display.flip()

    def _draw_connections(self):
        for connection in self._graph.connections:
            pygame.draw.line(self.screen, self.COLORS["grey"], self._get_screen_coords(*connection.hubs[0].coordinates), self._get_screen_coords(*connection.hubs[1].coordinates), 20)

    def _draw_hubs(self):
        for hub in self._graph.hubs.values():
            self._draw_circle(self.COLORS[hub.color], hub.coordinates)
        self._draw_circle(self.COLORS[self._graph.start_hub.color],
                          self._graph.start_hub.coordinates)
        self._draw_circle(self.COLORS[self._graph.end_hub.color],
                          self._graph.end_hub.coordinates)
        pygame.display.flip()

    def _print_names(self):
        for hub in self._graph.hubs.values():
            text = self.font.render(hub.name, True, "white", "black")
            coords = self._get_screen_coords(*hub.coordinates)
            coords = (coords[0] - 35, coords[1] + 45)
            self.screen.blit(text, coords)
        text = self.font.render(self._graph.start_hub.name, True, "white", "black")
        coords = self._get_screen_coords(*self._graph.start_hub.coordinates)
        coords = (coords[0] - 35, coords[1] + 45)
        self.screen.blit(text, coords)
        text = self.font.render(self._graph.end_hub.name, True, "white", "black")
        coords = self._get_screen_coords(*self._graph.end_hub.coordinates)
        coords = (coords[0] - 35, coords[1] + 45)
        self.screen.blit(text, coords)
        pygame.display.flip()

    def _set_distance_between_hubs(self):
        min_v = {}
        min_v["x"] = min([hub.coordinates[0] for hub in self._graph.hubs.values()] + [self._graph.start_hub.coordinates[0], self._graph.end_hub.coordinates[0]])
        min_v["y"] = min([hub.coordinates[1] for hub in self._graph.hubs.values()] + [self._graph.start_hub.coordinates[1], self._graph.end_hub.coordinates[1]])
        max_v = {}
        max_v["x"] = max([hub.coordinates[0] for hub in self._graph.hubs.values()] + [self._graph.start_hub.coordinates[0], self._graph.end_hub.coordinates[0]])
        max_v["y"] = max([hub.coordinates[1] for hub in self._graph.hubs.values()] + [self._graph.start_hub.coordinates[1], self._graph.end_hub.coordinates[1]])
        covered_by_map_x = self.screen_x * 0.85
        covered_by_map_y = self.screen_y * 0.90
        distance_between = {
            "x": (covered_by_map_x - 35) // abs(max_v["x"] - min_v["x"]),
            "y": (covered_by_map_y - 35) // abs(max_v["y"] - min_v["y"])
            }
        self.converted_coordinates = {
            "x": {},
            "y": {}
            }
        counter = 0
        for coord in range(min_v["y"], max_v["y"] + 1):
            self.converted_coordinates["y"][coord] = (distance_between["y"] * counter + self.screen_y * 0.05 if counter != 0 else self.screen_y * 0.05)
            counter += 1
        counter = 0
        for coord in range(min_v["x"], max_v["x"] + 1):
            self.converted_coordinates["x"][coord] = (distance_between["x"] * counter + self.screen_x * 0.075 if counter != 0 else self.screen_x * 0.075)
            counter += 1

    def _initialize_pygame(self):
        pygame.init()
        pygame.font.init()
        self.screen_x, self.screen_y = (pygame.display.Info().current_w,
                                        pygame.display.Info().current_h)
        self._set_distance_between_hubs()
        pygame.display.set_icon(pygame.image.load("source/assets/fly-in_icone.png"))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Fly-in")
        self.screen.blit(pygame.image.load(f"source/assets/Fly-In_Background_2_{self.screen_x}{self.screen_y}.png"), (0, 0))
        pygame.display.flip()
        self.font = pygame.font.Font(None, 25)

    def _get_screen_coords(self, x, y):
        return self.converted_coordinates["x"][x], self.converted_coordinates["y"][y]

    def display_graph(self):
        self._initialize_pygame()
        self._draw_connections()
        self._draw_hubs()
        self._print_names()
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
