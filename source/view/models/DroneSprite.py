import pygame


class DroneSprite(pygame.sprite.Sprite):
    def __init__(self, id, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.square = self.image.get_rect()
        self.id = id

    def draw(self, coordinates, screen, font):
        self.square.center = coordinates
        screen.blit(self.image, self.square)
        number = font.render(str(self.id), True, "white")
        screen.blit(number, (coordinates[0] - self.width // 4,
                             coordinates[1] - self.height // 4))
