import pygame


class DroneSprite(pygame.sprite.Sprite):
    def __init__(self, id, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.square = self.image.get_rect()
        self.id = id

    def draw(self, coordinates, screen):
        self.square.center = coordinates
        screen.blit(self.image, self.square)
