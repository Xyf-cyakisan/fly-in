from typing import Any
import pygame
from abc import ABC, abstractmethod


class Sprite(ABC, pygame.sprite.Sprite):
    @abstractmethod
    def draw(self, coordinates: tuple[float, float],
             extras: dict[str, Any]) -> None:
        pass
