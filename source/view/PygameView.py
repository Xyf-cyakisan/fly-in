import os

from ..model.Graph import Graph
from .models import DroneSprite

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
try:
    import pygame
except ImportError:
    import sys

    print(
        "Error: Pygame module not found, please use "
        "the 'make install' before running the program"
    )
    sys.exit(1)


class PygameView:

    COLORS: dict[str, str | tuple[int, int, int]] = {
        "default": "white",
        "black": (0, 0, 0),
        "darkgrey": (40, 40, 45),
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
        "grey": (192, 192, 192),
    }

    def __init__(self, graph: Graph) -> None:
        self._graph: Graph = graph
        self.current_turn: int = -1
        self.actual_turn: int = 0

    def _draw_circle(self, color: str | tuple[int, int, int],
                     coords: tuple[float, float], hub_type: str) -> None:
        hub_type_color = {
            "priority": "blue",
            "normal": "black",
            "restricted": "red",
            "blocked": "brown",
        }
        around = hub_type_color[hub_type]
        pygame.draw.circle(self.screen, around, coords, 35)
        pygame.draw.circle(self.screen, color, coords, 30)

    def _draw_connections(self) -> None:
        for connection in self._graph.connections:
            pygame.draw.line(
                self.screen,
                self.COLORS["grey"],
                self.coords[connection.hubs[0].name],
                self.coords[connection.hubs[1].name],
                20,
            )

    def _draw_hubs(self) -> None:
        for hub in self._graph.hubs.values():
            hub_type = getattr(hub, "type", None)
            if hub_type is None:
                hub_type = "normal"
            self._draw_circle(
                self.COLORS[getattr(hub, "color", "default")],
                self.coords[hub.name], hub_type
            )

    def _print_names(self) -> None:
        for hub in self._graph.hubs.values():
            text = self.font.render(hub.name, True, "white", "black")
            coords = self.coords[hub.name]
            coords = (coords[0] - 35, coords[1] + 45)
            self.screen.blit(text, coords)

    def _set_distance_between_hubs(self) -> dict[str, dict[int, float]]:
        min_v = {}
        min_v["x"] = min(
            [hub.coordinates[0] for hub in self._graph.hubs.values()]
        )
        min_v["y"] = min(
            [hub.coordinates[1] for hub in self._graph.hubs.values()]
        )
        max_v = {}
        max_v["x"] = max(
            [hub.coordinates[0] for hub in self._graph.hubs.values()]
        )
        max_v["y"] = max(
            [hub.coordinates[1] for hub in self._graph.hubs.values()]
        )
        covered_by_map_x = self.screen_x * 0.85
        covered_by_map_y = self.screen_y * 0.90
        distance_between = {
            "x": (
                (covered_by_map_x - 35) // abs(max_v["x"] - min_v["x"])
                if abs(max_v["x"] - min_v["x"]) != 0
                else 0
            ),
            "y": (
                (covered_by_map_y - 35) // abs(max_v["y"] - min_v["y"])
                if abs(max_v["y"] - min_v["y"]) != 0
                else 0
            ),
        }
        converted_coordinates: dict[str, dict[int, float]] = {"x": {}, "y": {}}
        counter = 0
        if distance_between["y"] == 0:
            converted_coordinates["y"][min_v["y"]] = self.screen_y // 2
        else:
            for coord in range(min_v["y"], max_v["y"] + 1):
                converted_coordinates["y"][coord] = (
                    distance_between["y"] * counter + self.screen_y * 0.05
                    if counter != 0
                    else self.screen_y * 0.05
                )
                counter += 1
            counter = 0
        if distance_between["x"] == 0:
            converted_coordinates["x"][min_v["y"]] = self.screen_x // 2
        else:
            for coord in range(min_v["x"], max_v["x"] + 1):
                converted_coordinates["x"][coord] = (
                    distance_between["x"] * counter + self.screen_x * 0.075
                    if counter != 0
                    else self.screen_x * 0.075
                )
                counter += 1
        return converted_coordinates

    def _initialize_coords_dict(self) -> None:
        converted_coordinates = self._set_distance_between_hubs()
        self.coords = {}
        for hub in self._graph.hubs.values():
            self.coords[hub.name] = (
                converted_coordinates["x"][hub.coordinates[0]],
                converted_coordinates["y"][hub.coordinates[1]],
            )
        for connection in self._graph.connections:
            self.coords[connection.name] = (
                (
                    self.coords[connection.hubs[0].name][0]
                    + self.coords[connection.hubs[1].name][0]
                )
                / 2,
                (
                    self.coords[connection.hubs[0].name][1]
                    + self.coords[connection.hubs[1].name][1]
                )
                / 2,
            )

    def _initialize_pygame(self) -> None:
        pygame.init()
        pygame.font.init()
        self.screen_x, self.screen_y = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h,
        )
        pygame.display.set_icon(
            pygame.image.load("source/assets/fly-in_icone." "png")
        )
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Fly-in")
        self.screen.fill(self.COLORS["darkgrey"])
        self.font = pygame.font.Font(None, 25)

    def _initialize_drones(self) -> None:
        self.drones = [
            DroneSprite(drone.id, "blue", 25, 25)
            for drone in self._graph.drones
        ]
        for drone in self.drones:
            drone.draw(
                self.coords[self._graph.start_hub.name], self.screen, self.font
            )

    def _print_places_capacity(self, current_turn: int) -> None:
        for place_name, place_capacity in self._graph.capacity[
            current_turn
        ].items():
            text = self.font.render(place_capacity, True, "white", "black")
            self.screen.blit(
                text,
                (
                    self.coords[place_name][0] - 17.5,
                    self.coords[place_name][1] - 60,
                ),
            )

    def _print_next_turn(self) -> None:
        if self.actual_turn != len(self._graph.tracks[1]):
            self.screen.fill(self.COLORS["darkgrey"])
            self._reset_map()
            self.current_turn += 1
            self.actual_turn += 1
            for i, drone in enumerate(self._graph.drones):
                self.drones[i].draw(
                    self.coords[
                        self._graph.tracks[drone.id][self.current_turn][1]
                    ],
                    self.screen,
                    self.font,
                )
            self._print_places_capacity(self.actual_turn)
            self._print_turn_number()
            print(f"Turn {self.current_turn + 1}: ", end="")
            for drone in self._graph.drones:
                print(
                    self._graph.tracks[drone.id][self.current_turn][0],
                    end=(
                        " "
                        if self._graph.tracks[drone.id][self.current_turn][0]
                        != ""
                        else ""
                    ),
                )
            print()
            pygame.display.flip()

    def _reset_map(self) -> None:
        self._draw_connections()
        self._draw_hubs()
        self._print_names()

    def _print_turn_number(self) -> None:
        text = self.font.render(
            "Turn: " + str(self.actual_turn), True, "white", "black"
        )
        self.screen.blit(text, (0, 0))

    def _reset_whole_visual(self) -> None:
        self.actual_turn = 0
        self.current_turn = -1
        self.screen.fill(self.COLORS["darkgrey"])
        self._reset_map()
        self._initialize_drones()
        self._print_turn_number()
        self._print_places_capacity(self.actual_turn)
        pygame.display.flip()

    def display_graph(self) -> None:
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
                    elif event.key == pygame.K_r:
                        self._reset_whole_visual()
        pygame.quit()
