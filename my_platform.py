import pygame
import random

WIDTH, HEIGHT = 800, 450

# Plateformes plus hautes (pas a ras du sol)
PLATFORM_LEVELS = [
    HEIGHT - 160,   # Niveau bas
    HEIGHT - 230,   # Niveau haut
]


class Platform(pygame.sprite.Sprite):
    def __init__(self, speed, level=None, x_offset=0):
        super().__init__()

        # Dimensions de la plateforme
        self.width = random.randint(100, 140)
        self.height = 12

        # Creer la surface de la plateforme
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Style gothique pour la plateforme
        self.color = (60, 40, 60)
        self.border_color = (100, 70, 100)
        self.top_color = (90, 70, 90)

        self._draw_platform()

        self.rect = self.image.get_rect()
        self.speed = speed

        # Niveau de hauteur (0 ou 1 seulement)
        if level is None:
            self.level = random.randint(0, 1)
        else:
            self.level = min(level, 1)

        self.rect.y = PLATFORM_LEVELS[self.level]

        # Position X avec offset pour bon espacement
        self.rect.x = WIDTH + x_offset + random.randint(50, 100)

    def _draw_platform(self):
        self.image.fill((0, 0, 0, 0))

        # Corps de la plateforme
        pygame.draw.rect(self.image, self.color, (0, 2, self.width, self.height - 2))

        # Surface superieure
        pygame.draw.rect(self.image, self.top_color, (0, 0, self.width, 4))

        # Bordure
        pygame.draw.rect(self.image, self.border_color, (0, 0, self.width, self.height), 2)

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.reset()

    def reset(self):
        # Alterner entre les 2 niveaux
        self.level = 1 - self.level
        self.rect.y = PLATFORM_LEVELS[self.level]

        # Grand espacement
        self.rect.x = WIDTH + random.randint(400, 600)

        # Nouvelle largeur
        self.width = random.randint(100, 140)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._draw_platform()

        old_y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(400, 600)
        self.rect.y = old_y

    def set_speed(self, speed):
        self.speed = speed
