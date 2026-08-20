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
        potential_screen = extras.get("screen")
        if isinstance(potential_screen, pygame.surface.Surface):
            screen: pygame.surface.Surface = potential_screen
        potential_font = extras.get("font")
        if isinstance(potential_font, pygame.font.Font):
            font: pygame.font.Font = potential_font
        sc_coords = extras.get("coordinates", None)
        if sc_coords is None:
            self.square.center = (int(coordinates[0]), int(coordinates[1]))
        else:
            coordinates = (int((coordinates[0] + sc_coords[0]) / 2),
                           int((coordinates[1] + sc_coords[1]) / 2))
            self.square.center = coordinates
        screen.blit(self.image, self.square)
        number = font.render(str(self.id), True, "white")
        screen.blit(number, (coordinates[0] - self.width // 4,
                             coordinates[1] - self.height // 4))
