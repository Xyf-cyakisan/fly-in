from typing import Any
from .Sprite import Sprite
import pygame
from ..pygame_utils import COLORS


class ConnectionSprite(Sprite):
    def __init__(self, name: str, hubs: tuple[str, str]) -> None:
        self.name: str = name
        self.hubs: tuple[str, str] = hubs

    def draw(self, coordinates: tuple[tuple[float, float]],
             extras: dict[str, Any]) -> None:
        screen = extras.get("screen")
        pygame.draw.line(
                screen,
                COLORS["grey"],
                coordinates[0],
                coordinates[1],
                20,
        )
