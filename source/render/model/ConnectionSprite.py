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


class ConnectionSprite(Sprite):
    def __init__(self, name: str, hubs: list[str]) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.__name: str = name
        self.__hubs: list[str] = hubs

    def get_name(self) -> str:
        return self.__name

    def draw(self, coordinates: tuple[float, float],
             extras: dict[str, Any]) -> None:
        sc_coords = extras.get("coordinates")
        if isinstance(sc_coords, tuple) and all(isinstance(number, (float, int)
                                                           )
                                                for number in sc_coords):
            potential_screen = extras.get("screen")
            if isinstance(potential_screen, pygame.surface.Surface):
                screen: pygame.surface.Surface = potential_screen
            pygame.draw.line(
                    screen,
                    COLORS["grey"],
                    coordinates,
                    sc_coords,
                    20,
            )
