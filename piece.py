import pygame
import random

WIDTH, HEIGHT = 800, 450


class Piece(pygame.sprite.Sprite):
    def __init__(self, vitesse, x=None, y=None):
        super().__init__()

        self.taille = 24
        self.speed = vitesse

        # Animation de la piece
        self.frame = 0
        self.timer = 0
        self.vitesse_anim = 5

        # Creer la surface
        self.image = pygame.Surface((self.taille, self.taille), pygame.SRCALPHA)
        self._dessiner_piece()

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

        self.collectee = False
        self.valeur = 10  # Valeur de la piece

    def _dessiner_piece(self):
        self.image.fill((0, 0, 0, 0))

        # Couleurs de la piece (style dore/bronze)
        centre = self.taille // 2

        # Animation simple : la piece "pulse"
        pulse = abs(self.frame - 2)
        rayon = centre - 2 - pulse

        # Cercle exterieur (bordure)
        pygame.draw.circle(self.image, (180, 140, 50), (centre, centre), rayon + 2)
        # Cercle interieur (piece)
        pygame.draw.circle(self.image, (255, 200, 80), (centre, centre), rayon)
        # Reflet
        pygame.draw.circle(self.image, (255, 230, 150), (centre - 2, centre - 2), rayon // 3)

    def update(self):
        # Les pieces collectees reapparaissent apres un delai
        if self.collectee:
            self.timer += 1
            if self.timer >= 120:  # 2 secondes a 60 FPS
                self.reinitialiser()
            return

        self.rect.x -= self.speed

        # Animation
        self.timer += 1
        if self.timer >= self.vitesse_anim:
            self.timer = 0
            self.frame = (self.frame + 1) % 4
            self._dessiner_piece()

        # Reinitialiser quand elle sort de l'ecran
        if self.rect.right < 0:
            self.reinitialiser()

    def reinitialiser(self):
        self.rect.x = WIDTH + random.randint(100, 400)
        # Hauteurs variees : sol, milieu, ou en hauteur
        hauteurs = [HEIGHT - 100, HEIGHT - 150, HEIGHT - 200, HEIGHT - 280]
        self.rect.y = random.choice(hauteurs)
        self.collectee = False
        self.timer = 0

    def collecter(self):
        self.collectee = True
        self.timer = 0  # Reset timer pour reapparition
        self.rect.x = -100  # Cacher la piece
        return self.valeur

    def set_speed(self, vitesse):
        self.speed = vitesse
