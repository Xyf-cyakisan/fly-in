from typing import Any
from .Sprite import Sprite
try:
    import pygame
except ImportError:
    import sys
    print(
        "\033[0;31mError: 'Pygame' module not found,"
        "please run 'make install' command before 'make run'\033[0m"
    )
    sys.exit(4)
from ..pygame_utils import COLORS


class HubSprite(Sprite):
    def __init__(self, name: str, capacity: list[str],
                 color: tuple[int, int, int] | str, hub_type: str) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.__name: str = name
        self.__capacity: list[str] = capacity
        self.__color: tuple[int, int, int] | str = color
        self.__hub_type: str = hub_type

    def get_name(self) -> str:
        return self.__name

    def update_capacity(self, coordinates: tuple[float, float],
                        extras: dict[str, Any]) -> None:
        potential_screen = extras.get("screen")
        if isinstance(potential_screen, pygame.surface.Surface):
            screen: pygame.surface.Surface = potential_screen
        potential_font = extras.get("font")
        if isinstance(potential_font, pygame.font.Font):
            font: pygame.font.Font = potential_font
        turn = extras.get("turn")
        if isinstance(turn, int):
            text = font.render(self.__capacity[turn], True,
                               "white", "black")
            screen.blit(text, (coordinates[0] - 17.5, coordinates[1] - 60))

    def draw(self, coordinates: tuple[float, float],
             extras: dict[str, Any]) -> None:
        potential_screen = extras.get("screen")
        if isinstance(potential_screen, pygame.surface.Surface):
            screen: pygame.surface.Surface = potential_screen
        potential_font = extras.get("font")
        if isinstance(potential_font, pygame.font.Font):
            font: pygame.font.Font = potential_font
        hub_type_color = {
            "priority": "blue",
            "normal": "black",
            "restricted": "red",
            "blocked": "brown",
        }
        around = COLORS[hub_type_color[self.__hub_type]]
        pygame.draw.circle(screen, around, coordinates, 35)
        if self.__color != "rainbow":
            pygame.draw.circle(screen, self.__color, coordinates, 30)
        else:
            rainbow_colors = [
                COLORS["red"],
                COLORS["orange"],
                COLORS["yellow"],
                COLORS["green"],
                COLORS["cyan"],
                COLORS["blue"],
                COLORS["violet"],
            ]
            for color, radius in zip(rainbow_colors, range(30, 0, -3)):
                pygame.draw.circle(screen, color, coordinates, radius)
        text = font.render(self.__name, True, "white", "black")
        coords = (coordinates[0] - 35, coordinates[1] + 45)
        screen.blit(text, coords)
