import os
from typing import Any
from ..model.Hub import Hub
from ..model.Connection import Connection
from .model import DroneSprite, Sprite, HubSprite, ConnectionSprite
from .pygame_utils import COLORS
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
try:
    import pygame
except ImportError:
    import sys

    print(
        "Error: Pygame module not found, please use "
        "the 'make install' before running the program"
    )
    sys.exit(4)


class Renderer:
    def __init__(
        self,
        nb_drones: int,
        start_hub: Hub,
        hubs: dict[str, Hub],
        connections: list[Connection],
        tracks: dict[int, list[tuple[str, str] | str]],
        capacity: dict[str, list[str]],
    ) -> None:
        self.__nb_drones: int = nb_drones
        self.__tracks: dict[int, list[tuple[str, str] | str]] = tracks
        self.__current_turn: int = -1
        self.__actual_turn: int = 0
        self._initialize_pygame()
        self._initialize_coords_dict(hubs, connections)
        self._initialize_sprites(capacity, start_hub, list(hubs.values()),
                                 connections)

    def _set_distance_between_hubs(self, hubs: dict[str, Hub]
                                   ) -> dict[str, dict[int, float]]:
        min_v = {}
        min_v["x"] = min([hub.coordinates[0] for hub in hubs.values()])
        min_v["y"] = min([hub.coordinates[1] for hub in hubs.values()])
        max_v = {}
        max_v["x"] = max([hub.coordinates[0] for hub in hubs.values()])
        max_v["y"] = max([hub.coordinates[1] for hub in hubs.values()])
        covered_by_map_x = self.__screen_x * 0.85
        covered_by_map_y = self.__screen_y * 0.90
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
            converted_coordinates["y"][min_v["y"]] = self.__screen_y // 2
        else:
            for coord in range(min_v["y"], max_v["y"] + 1):
                converted_coordinates["y"][coord] = (
                    distance_between["y"] * counter + self.__screen_y * 0.05
                    if counter != 0
                    else self.__screen_y * 0.05
                )
                counter += 1
            counter = 0
        if distance_between["x"] == 0:
            converted_coordinates["x"][min_v["y"]] = self.__screen_x // 2
        else:
            for coord in range(min_v["x"], max_v["x"] + 1):
                converted_coordinates["x"][coord] = (
                    distance_between["x"] * counter + self.__screen_x * 0.075
                    if counter != 0
                    else self.__screen_x * 0.075
                )
                counter += 1
        return converted_coordinates

    def _initialize_coords_dict(self, hubs: dict[str, Hub],
                                connections: list[Connection]) -> None:
        converted_coordinates = self._set_distance_between_hubs(hubs)
        self.__coords: dict[str, Any] = {}
        for hub in hubs.values():
            self.__coords[hub.name] = (
                converted_coordinates["x"][hub.coordinates[0]],
                converted_coordinates["y"][hub.coordinates[1]],
            )
        for connection in connections:
            self.__coords[connection.name] = (
                (
                    self.__coords[connection.hubs[0].name][0],
                    self.__coords[connection.hubs[0].name][1]
                ),
                (
                    self.__coords[connection.hubs[1].name][0],
                    self.__coords[connection.hubs[1].name][1]
                )
            )

    def _initialize_pygame(self) -> None:
        pygame.init()
        pygame.font.init()
        self.__screen_x, self.__screen_y = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h,
        )

    def _initialize_sprites(self, capacity: dict[str, list[str]],
                            start_hub: Hub,
                            hubs: list[Hub],
                            connections: list[Connection]) -> None:
        self.__start_hub: HubSprite = HubSprite(
            start_hub.name, capacity[start_hub.name],
            COLORS[getattr(start_hub, "color", "default")],
            getattr(start_hub, "type", "normal"))
        self.__still_sprites: list[Sprite] = [
            ConnectionSprite(connection.name, [hub.name for hub in
                                               connection.hubs]) for
            connection in connections]
        self.__still_sprites.extend([HubSprite(hub.name, capacity[hub.name],
                                    COLORS[getattr(hub, "color", "default")],
                                    getattr(hub, "type", "normal")) for hub
                                    in hubs if hub.name != start_hub.name])
        self.__still_sprites.append(self.__start_hub)
        self.__drones: list[DroneSprite] = [DroneSprite(id, "blue", 25, 25)
                                            for id in
                                            range(1, self.__nb_drones + 1)]

    def _initialize_window(self) -> None:
        pygame.display.set_icon(
            pygame.image.load("source/assets/Fly-in_icone." "png")
        )
        self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.__clock = pygame.time.Clock()
        pygame.display.set_caption("Fly-in")
        self.__screen.fill(COLORS["darkgrey"])
        self.__font = pygame.font.Font(None, 25)

    def _initialize_drones(self) -> None:
        for drone in self.__drones:
            drone.draw(
                self.__coords[self.__start_hub.name],
                {"screen": self.__screen,
                 "font": self.__font}
            )

    def _print_victory(self) -> None:
        victory_font = pygame.font.Font("source/assets/Victory.ttf", 500)
        message = "Victory!"
        rainbow_colors = [
            COLORS["red"],
            COLORS["orange"],
            COLORS["yellow"],
            COLORS["green"],
            COLORS["cyan"],
            COLORS["blue"],
            COLORS["violet"],
        ]
        letter_surfaces = [
            victory_font.render(
                letter, True, rainbow_colors[index % len(rainbow_colors)]
            )
            for index, letter in enumerate(message)
        ]
        total_width = sum(surface.get_width() for surface in letter_surfaces)
        x = (self.__screen_x // 2) - (total_width // 2)
        y = (self.__screen_y // 2) - (victory_font.get_height() // 2)
        for i, surface in enumerate(letter_surfaces):
            self.__screen.blit(surface, (x, y))
            if i + 1 != len(message) and message[i + 1] != "y":
                x += surface.get_width()
            else:
                x += letter_surfaces[i - 1].get_width() // 3

    def _update_capacity(self) -> None:
        for sprite in self.__still_sprites:
            if isinstance(sprite, HubSprite):
                extras = {"screen": self.__screen,
                          "font": self.__font,
                          "type": getattr(sprite,
                                          "type",
                                          None),
                          "turn": self.__actual_turn}
                sprite.update_capacity(self.__coords[sprite.name], extras)

    def _print_next_turn(self) -> None:
        if self.__actual_turn != len(self.__tracks[1]):
            self.__screen.fill(COLORS["darkgrey"])
            self._reset_map()
            self.__current_turn += 1
            self.__actual_turn += 1
            for drone in self.__drones:
                extras = {"screen": self.__screen,
                          "font": self.__font}
                coords = self.__coords[
                        self.__tracks[drone.id][self.__current_turn][1]
                    ]
                if isinstance(coords[0], tuple):
                    extras["coordinates"] = coords[1]
                    coords = coords[0]
                drone.draw(coords, extras)
            self._update_capacity()
            self._print_turn_number()
            if self.__actual_turn == len(self.__tracks[1]):
                self._print_victory()
            print(f"Turn {self.__current_turn + 1}: ", end="")
            for drone in self.__drones:
                print(
                    self.__tracks[drone.id][self.__current_turn][0],
                    end=(
                        " "
                        if self.__tracks[drone.id][self.__current_turn][0]
                        != ""
                        else ""
                    ),
                )
            print()
            pygame.display.flip()

    def _reset_map(self) -> None:
        for sprite in self.__still_sprites:
            coords = self.__coords[getattr(sprite, "name")]
            extras = {"screen": self.__screen,
                      "font": self.__font,
                      "type": getattr(sprite,
                                      "type",
                                      None),
                      "turn": self.__actual_turn}
            if isinstance(coords[0], tuple):
                extras["coordinates"] = coords[1]
                coords = coords[0]
            sprite.draw(coords, extras)

    def _print_turn_number(self) -> None:
        text = self.__font.render(
            "Turn: " + str(self.__actual_turn), True, "white", "black"
        )
        self.__screen.blit(text, (0, 0))

    def _reset_whole_visual(self) -> None:
        self.__actual_turn = 0
        self.__current_turn = -1
        self.__screen.fill(COLORS["darkgrey"])
        self._reset_map()
        self._update_capacity()
        self._initialize_drones()
        self._print_turn_number()
        pygame.display.flip()

    def display_simulation(self) -> None:
        self._initialize_window()
        self._reset_map()
        self._update_capacity()
        self._initialize_drones()
        self._print_turn_number()
        pygame.display.flip()
        running = True
        while running:
            self.__clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self._print_next_turn()
                    elif event.key == pygame.K_r:
                        self._reset_whole_visual()
        pygame.quit()
