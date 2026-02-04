import pygame
import random

WIDTH, HEIGHT = 800, 450


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed, x=None, y=None):
        super().__init__()

        self.size = 24
        self.speed = speed

        # Animation de la piece
        self.frame = 0
        self.timer = 0
        self.animation_speed = 5

        # Creer la surface
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self._draw_coin()

        self.rect = self.image.get_rect()

        # Position initiale
        if x is None:
            self.rect.x = WIDTH + random.randint(100, 600)
        else:
            self.rect.x = x

        if y is None:
            # Position aleatoire en hauteur
            self.rect.y = random.randint(HEIGHT - 250, HEIGHT - 100)
        else:
            self.rect.y = y

        self.collected = False
        self.value = 10  # Valeur de la piece

    def _draw_coin(self):
        self.image.fill((0, 0, 0, 0))

        # Couleurs de la piece (style dore/bronze)
        center = self.size // 2

        # Animation simple : la piece "pulse"
        pulse = abs(self.frame - 2)
        radius = center - 2 - pulse

        # Cercle exterieur (bordure)
        pygame.draw.circle(self.image, (180, 140, 50), (center, center), radius + 2)
        # Cercle interieur (piece)
        pygame.draw.circle(self.image, (255, 200, 80), (center, center), radius)
        # Reflet
        pygame.draw.circle(self.image, (255, 230, 150), (center - 2, center - 2), radius // 3)

    def update(self):
        # Les pieces collectees reapparaissent apres un delai
        if self.collected:
            self.timer += 1
            if self.timer >= 120:  # 2 secondes a 60 FPS
                self.reset()
            return

        self.rect.x -= self.speed

        # Animation
        self.timer += 1
        if self.timer >= self.animation_speed:
            self.timer = 0
            self.frame = (self.frame + 1) % 4
            self._draw_coin()

        # Reinitialiser quand elle sort de l'ecran
        if self.rect.right < 0:
            self.reset()

    def reset(self):
        self.rect.x = WIDTH + random.randint(100, 400)
        # Hauteurs variees : sol, milieu, ou en hauteur
        heights = [HEIGHT - 100, HEIGHT - 150, HEIGHT - 200, HEIGHT - 280]
        self.rect.y = random.choice(heights)
        self.collected = False
        self.timer = 0

    def collect(self):
        self.collected = True
        self.timer = 0  # Reset timer pour reapparition
        self.rect.x = -100  # Cacher la piece
        return self.value

    def set_speed(self, speed):
        self.speed = speed
