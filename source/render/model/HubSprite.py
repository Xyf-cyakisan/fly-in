from typing import Any
from .Sprite import Sprite
import pygame
from ..pygame_utils import COLORS


class HubSprite(Sprite):
    def __init__(self, name: str, capacity: list[str],
                 color: tuple[int, int, int], hub_type: str) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.name: str = name
        self.capacity: list[str] = capacity
        self.color: tuple[int, int, int] = color
        self.hub_type: str = hub_type

    def update_capacity(self, coordinates: tuple[float, float],
                        extras: dict[str, Any]) -> None:
        screen = extras.get("screen")
        font = extras.get("font")
        text = font.render(self.capacity[extras.get("turn")], True,
                           "white", "black")
        screen.blit(text, (coordinates[0] - 17.5, coordinates[1] - 60))

    def draw(self, coordinates: tuple[float, float],
             extras: dict[str, Any]) -> None:
        screen = extras.get("screen")
        font = extras.get("font")
        hub_type_color = {
            "priority": "blue",
            "normal": "black",
            "restricted": "red",
            "blocked": "brown",
        }
        around = COLORS[hub_type_color[self.hub_type]]
        pygame.draw.circle(screen, around, coordinates, 35)
        pygame.draw.circle(screen, self.color, coordinates, 30)
        text = font.render(self.name, True, "white", "black")
        coords = (coordinates[0] - 35, coordinates[1] + 45)
        screen.blit(text, coords)
        self.update_capacity(coordinates, extras)
