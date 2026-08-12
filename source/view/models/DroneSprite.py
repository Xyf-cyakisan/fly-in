import pygame


class DroneSprite(pygame.sprite.Sprite):
    def __init__(self, id: int, color: tuple[int, int, int], width: int,
                 height: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.width: int = width
        self.height: int = height
        self.image: pygame.Surface = pygame.Surface([width, height])
        self.image.fill(color)
        self.square: pygame.Rect = self.image.get_rect()
        self.id: int = id

    def draw(self, coordinates: tuple[int, int],
             screen: pygame.surface.Surface, font: pygame.font.Font) -> None:
        self.square.center = coordinates
        screen.blit(self.image, self.square)
        number = font.render(str(self.id), True, "white")
        screen.blit(number, (coordinates[0] - self.width // 4,
                             coordinates[1] - self.height // 4))
