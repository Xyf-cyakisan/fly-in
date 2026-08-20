from typing import Any
from .Sprite import Sprite
import pygame
from ..pygame_utils import COLORS


class ConnectionSprite(Sprite):
    def __init__(self, name: str, hubs: list[str]) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.name: str = name
        self.hubs: list[str] = hubs

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
