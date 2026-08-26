from typing import Any
try:
    import pygame
except ImportError:
    import sys
    print(
        "\033[0;31mError: 'Pygame' module not found,"
        "please run 'make install' command before 'make run'\033[0m"
    )
    sys.exit(4)
from .Sprite import Sprite


class DroneSprite(Sprite):
    def __init__(self, id: int, color: str | tuple[int, int, int], width: int,
                 height: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.__width: int = width
        self.__height: int = height
        self.__image: pygame.Surface = pygame.Surface([width, height])
        self.__image.fill(color)
        self.__square: pygame.Rect = self.__image.get_rect()
        self.__id: int = id

    def get_id(self) -> int:
        return self.__id

    def draw(self, coordinates: tuple[float, float],
             extras: dict[str, Any]) -> None:
        potential_screen = extras.get("screen")
        if isinstance(potential_screen, pygame.surface.Surface):
            screen: pygame.surface.Surface = potential_screen
        potential_font = extras.get("font")
        if isinstance(potential_font, pygame.font.Font):
            font: pygame.font.Font = potential_font
        sc_coords = extras.get("coordinates", None)
        if sc_coords is None:
            self.__square.center = (int(coordinates[0]), int(coordinates[1]))
        else:
            coordinates = (int((coordinates[0] + sc_coords[0]) / 2),
                           int((coordinates[1] + sc_coords[1]) / 2))
            self.__square.center = coordinates
        screen.blit(self.__image, self.__square)
        number = font.render(str(self.__id), True, "white")
        screen.blit(number, (coordinates[0] - self.__width // 4,
                             coordinates[1] - self.__height // 4))
