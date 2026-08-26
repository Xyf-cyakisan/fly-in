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
from abc import ABC, abstractmethod


class Sprite(ABC, pygame.sprite.Sprite):
    @abstractmethod
    def draw(self, coordinates: tuple[float, float],
             extras: dict[str, Any]) -> None:
        pass
