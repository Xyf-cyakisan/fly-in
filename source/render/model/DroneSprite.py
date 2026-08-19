from typing import Any
import pygame
from .Sprite import Sprite


class DroneSprite(Sprite):
    def __init__(self, id: int, color: str | tuple[int, int, int], width: int,
                 height: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.width: int = width
        self.height: int = height
        self.image: pygame.Surface = pygame.Surface([width, height])
        self.image.fill(color)
        self.square: pygame.Rect = self.image.get_rect()
        self.id: int = id

    def draw(self, coordinates: tuple[float, float],
             extras: dict[str, Any]) -> None:
        screen = extras.get("screen")
        font = extras.get("font")
        self.square.center = (int(coordinates[0]), int(coordinates[1]))
        screen.blit(self.image, self.square)
        number = font.render(str(self.id), True, "white")
        screen.blit(number, (coordinates[0] - self.width // 4,
                             coordinates[1] - self.height // 4))
