import pygame
from pathlib import Path
import random

# Taille d'écran
WIDTH, HEIGHT = 800, 450

# Dossier des assets
ASSETS = Path(__file__).parent / "assets"
SPIDER_IMG = ASSETS / "spider.webp"
HYDE_IMG = ASSETS / "hyde.webp"
CORBEAU_IMG = ASSETS / "corbeau.webp"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Charger les sprites
        self.walk_sheet = pygame.image.load("assets/mercrediadamspritemarche.png").convert_alpha()
        self.crouch_sheet = pygame.image.load("assets/mercrediadamspritecouche.png").convert_alpha()

        # Taille d'une frame
        self.walk_w = 43
        self.walk_h = 55
        self.crouch_w = 52
        self.crouch_h = 55

        # Animation
        self.frame = 0
        self.is_crouching = False
        self.timer = 0

        # Saut
        self.ground_y = 380  # Position du sol
        self.vel_y = 0       # Vitesse verticale
        self.jump_speed = -20  # Force du saut (négatif = vers le haut)
        self.gravity = 0.8   # Gravité

        self.image = pygame.Surface((self.walk_w, self.walk_h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = 60
        self.rect.y = self.ground_y

    def set_animation(self, anim_type):
        if anim_type == "crouch":
            self.is_crouching = True
        else:
            self.is_crouching = False

    def jump(self):
        # Saut uniquement si on est au sol
        if self.rect.bottom >= self.ground_y - 1:
            self.vel_y = self.jump_speed

    def update(self):
        #Appliquer la gravité
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        
        # Ne pas traverser le sol
        if self.rect.bottom > self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
        
        # Animation
        self.timer += 1
        
        if self.timer >= 7:
            self.timer = 0
            self.frame += 1
            
            # Sauvegarder la position
            old_x = self.rect.x
            old_y = self.rect.y
            
            if self.is_crouching:
                if self.frame >= 2:
                    self.frame = 0
                x = self.frame * self.crouch_w
                self.image = pygame.Surface((self.crouch_w, self.crouch_h), pygame.SRCALPHA)
                self.image.blit(self.crouch_sheet, (0, 0), (x, 0, self.crouch_w, self.crouch_h))
                self.image = pygame.transform.scale(self.image, (self.crouch_w * 2, self.crouch_h * 2))
            else:
                if self.frame >= 5:
                    self.frame = 0
                x = self.frame * self.walk_w
                self.image = pygame.Surface((self.walk_w, self.walk_h), pygame.SRCALPHA)
                self.image.blit(self.walk_sheet, (0, 0), (x, 0, self.walk_w, self.walk_h))
                self.image = pygame.transform.scale(self.image, (self.walk_w * 2, self.walk_h * 2))
            
            # Remettre la position
            self.rect = self.image.get_rect()
            self.rect.x = old_x
            self.rect.y = old_y


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        # Choisir une image au hasard
        img_path = random.choice([SPIDER_IMG, HYDE_IMG, CORBEAU_IMG])

        image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.smoothscale(image, (64, 64))  # ajuste la taille
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-20, -20)

        self.speed = speed
        # Position différente selon le type d'obstacle
        if img_path == CORBEAU_IMG:
            self.rect.bottom = HEIGHT - 150
        else:
            self.rect.bottom = HEIGHT - 70

        self.rect.left = WIDTH + random.randint(100, 500)

    def update(self):
        self.rect.x -= self.speed
        self.hitbox.center = self.rect.center

        if self.rect.right < 0:
            self.reset()


    def reset(self):
        img_path = random.choice([SPIDER_IMG, HYDE_IMG, CORBEAU_IMG])
        image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.smoothscale(image, (64, 64))
        self.rect = self.image.get_rect(center=self.rect.center)

        # Position différente selon le type d'obstacle
        if img_path == CORBEAU_IMG:
            self.rect.bottom = HEIGHT - 150  # Corbeau vole plus haut
        else:
            self.rect.bottom = HEIGHT - 70

        self.rect.left = WIDTH + random.randint(200, 600)

        self.hitbox = self.rect.inflate(-20, -20)
        self.hitbox.center = self.rect.center

        # Augmenter la vitesse pour la difficulté
        self.speed = min(self.speed + 0.1, 10)            