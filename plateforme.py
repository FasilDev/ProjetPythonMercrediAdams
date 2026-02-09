import pygame
import random

WIDTH, HEIGHT = 800, 450

NIVEAUX_PLATEFORME = [
    HEIGHT - 160,   # Niveau bas
    HEIGHT - 230,   # Niveau haut
]


class Plateforme(pygame.sprite.Sprite):
    def __init__(self, vitesse, niveau=None, x_offset=0):
        super().__init__()

        self.largeur = random.randint(100, 140)
        self.hauteur = 12

        # Creer la surface de la plateforme
        self.image = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)

        self.couleur = (60, 40, 60)
        self.couleur_bordure = (100, 70, 100)
        self.couleur_dessus = (90, 70, 90)

        self._dessiner_plateforme()

        self.rect = self.image.get_rect()
        self.speed = vitesse

        if niveau is None:
            self.niveau = random.randint(0, 1)
        else:
            self.niveau = min(niveau, 1)

        self.rect.y = NIVEAUX_PLATEFORME[self.niveau]

        self.rect.x = WIDTH + x_offset + random.randint(50, 100)

    def _dessiner_plateforme(self):
        self.image.fill((0, 0, 0, 0))

        pygame.draw.rect(self.image, self.couleur, (0, 2, self.largeur, self.hauteur - 2))

        pygame.draw.rect(self.image, self.couleur_dessus, (0, 0, self.largeur, 4))

        pygame.draw.rect(self.image, self.couleur_bordure, (0, 0, self.largeur, self.hauteur), 2)

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.reinitialiser()

    def reinitialiser(self):
        self.niveau = 1 - self.niveau
        self.rect.y = NIVEAUX_PLATEFORME[self.niveau]

        self.rect.x = WIDTH + random.randint(400, 600)

        self.largeur = random.randint(100, 140)
        self.image = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)
        self._dessiner_plateforme()

        old_y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(400, 600)
        self.rect.y = old_y

    def set_speed(self, vitesse):
        self.speed = vitesse
