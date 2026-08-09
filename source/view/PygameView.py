import os
from .models import DroneSprite
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
        self.current_turn = -1
        self.actual_turn = 0

    def _draw_circle(self, color, coords):
        around = self.COLORS["black"]
        if color == around:
            around = self.COLORS["default"]
        pygame.draw.circle(self.screen, around, coords, 35)
        pygame.draw.circle(self.screen, color, coords, 30)

    def _draw_connections(self):
        for connection in self._graph.connections:
            pygame.draw.line(self.screen, self.COLORS["grey"], self.coords[connection.hubs[0].name], self.coords[connection.hubs[1].name], 20)
        pygame.display.flip()

    def _draw_hubs(self):
        for hub in self._graph.hubs.values():
            self._draw_circle(self.COLORS[hub.color], self.coords[hub.name])
        self._draw_circle(self.COLORS[self._graph.start_hub.color],
                          self.coords[self._graph.start_hub.name])
        self._draw_circle(self.COLORS[self._graph.end_hub.color],
                          self.coords[self._graph.end_hub.name])
        pygame.display.flip()

    def _print_names(self):
        for hub in self._graph.hubs.values():
            text = self.font.render(hub.name, True, "white", "black")
            coords = self.coords[hub.name]
            coords = (coords[0] - 35, coords[1] + 45)
            self.screen.blit(text, coords)
        text = self.font.render(self._graph.start_hub.name, True, "white", "black")
        coords = self.coords[self._graph.start_hub.name]
        coords = (coords[0] - 35, coords[1] + 45)
        self.screen.blit(text, coords)
        text = self.font.render(self._graph.end_hub.name, True, "white", "black")
        coords = self.coords[self._graph.end_hub.name]
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
            "x": (covered_by_map_x - 35) // abs(max_v["x"] - min_v["x"]) if abs(max_v["x"] - min_v["x"]) != 0 else 0,
            "y": (covered_by_map_y - 35) // abs(max_v["y"] - min_v["y"]) if abs(max_v["y"] - min_v["y"]) != 0 else 0
            }
        self.converted_coordinates = {
            "x": {},
            "y": {}
            }
        counter = 0
        if distance_between["y"] == 0:
            self.converted_coordinates["y"][min_v["y"]] = self.screen_y // 2
        else:
            for coord in range(min_v["y"], max_v["y"] + 1):
                self.converted_coordinates["y"][coord] = (distance_between["y"] * counter + self.screen_y * 0.05 if counter != 0 else self.screen_y * 0.05)
                counter += 1
            counter = 0
        if distance_between["x"] == 0:
            self.converted_coordinates["x"][min_v["y"]] = self.screen_x // 2
        else:
            for coord in range(min_v["x"], max_v["x"] + 1):
                self.converted_coordinates["x"][coord] = (distance_between["x"] * counter + self.screen_x * 0.075 if counter != 0 else self.screen_x * 0.075)
                counter += 1

    def _initialize_coords_dict(self):
        self.coords = {}
        self.coords[self._graph.start_hub.name] = self._get_screen_coords(*self._graph.start_hub.coordinates)
        self.coords[self._graph.end_hub.name] = self._get_screen_coords(*self._graph.end_hub.coordinates)
        for hub in self._graph.hubs.values():
            self.coords[hub.name] = self._get_screen_coords(*hub.coordinates)
        for connection in self._graph.connections:
            self.coords[connection.name] = ((self.coords[connection.hubs[0].name][0] + self.coords[connection.hubs[1].name][0]) / 2, (self.coords[connection.hubs[0].name][1] + self.coords[connection.hubs[1].name][1]) / 2)

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
        self.screen.fill(self.COLORS["black"])
        pygame.display.flip()
        self.font = pygame.font.Font(None, 25)

    def _get_screen_coords(self, x, y):
        return self.converted_coordinates["x"][x], self.converted_coordinates["y"][y]

    def _initialize_drones(self):
        self.drones = [DroneSprite(drone.id, "blue", 25, 25) for drone in self._graph.drones]
        for drone in self.drones:
            drone.draw(self.coords[self._graph.start_hub.name], self.screen)
        pygame.display.flip()

    def _print_places_capacity(self, current_turn):
        for place_name, place_capacity in self._graph.capacity[current_turn].items():
            text = self.font.render(place_capacity, True, "white", "black")
            self.screen.blit(text, (self.coords[place_name][0] - 17.5, self.coords[place_name][1] - 60))

    def _print_next_turn(self):
        if self.actual_turn != len(self._graph.tracks[1]):
            self.screen.fill(self.COLORS["black"])
            pygame.display.flip()
            self._reset_map()
            self.current_turn += 1
            self.actual_turn += 1
            for i, drone in enumerate(self._graph.drones):
                self.drones[i].draw(self.coords[self._graph.tracks[drone.id][self.current_turn][1]], self.screen)
            self._print_places_capacity(self.actual_turn)
            pygame.display.flip()

    def _reset_map(self):
        self._draw_connections()
        self._draw_hubs()
        self._print_names()

    def _print_turn_number(self):
        text = self.font.render("Turn: " + str(self.actual_turn), True, "white", "black")
        self.screen.blit(text, (0, 0))
        pygame.display.flip()

    def display_graph(self):
        self._initialize_pygame()
        self._initialize_coords_dict()
        self._reset_map()
        self._initialize_drones()
        self._print_turn_number()
        self._print_places_capacity(self.actual_turn)
        pygame.display.flip()
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self._print_next_turn()
                        self._print_turn_number()
        pygame.quit()


if __name__ == "__main__":
    view = PygameView("prout")
    view.display_graph()
