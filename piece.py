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

        if x is None:
            self.rect.x = WIDTH + random.randint(100, 600)
        else:
            self.rect.x = x

        if y is None:
            self.rect.y = random.randint(HEIGHT - 280, HEIGHT - 140)
        else:
            self.rect.y = y

        self.collectee = False
        self.valeur = 10  

    def _dessiner_piece(self):
        self.image.fill((0, 0, 0, 0))

        # Couleurs de la piece
        centre = self.taille // 2

        pulse = abs(self.frame - 2)
        rayon = centre - 2 - pulse

        pygame.draw.circle(self.image, (180, 140, 50), (centre, centre), rayon + 2)

        pygame.draw.circle(self.image, (255, 200, 80), (centre, centre), rayon)

        pygame.draw.circle(self.image, (255, 230, 150), (centre - 2, centre - 2), rayon // 3)

    def update(self):
        # Les pieces collectees reapparaissent apres un delai
        if self.collectee:
            self.timer += 1
            if self.timer >= 120: 
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
        # Hauteurs variees 
        hauteurs = [HEIGHT - 140, HEIGHT - 180, HEIGHT - 220, HEIGHT - 280]
        self.rect.y = random.choice(hauteurs)
        self.collectee = False
        self.timer = 0

    def collecter(self):
        self.collectee = True
        self.timer = 0  
        self.rect.x = -100  
        return self.valeur

    def set_speed(self, vitesse):
        self.speed = vitesse
