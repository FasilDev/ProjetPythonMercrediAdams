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
        self.jump_speed = -12  # Force initiale du saut (un peu plus haut)
        self.gravity = 0.8   # Gravite

        # Saut variable (maintenir espace pour sauter plus haut)
        self.is_jumping = False
        self.jump_held = False
        self.jump_hold_time = 0
        self.max_jump_hold = 15  # Frames max pour maintenir le saut
        self.jump_boost = -0.8   # Boost par frame quand on maintient

        self.image = pygame.Surface((self.walk_w, self.walk_h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = 60
        self.rect.y = self.ground_y

        # Hitbox pour les collisions
        self.hitbox = self.rect.inflate(-20, -10)

    def set_animation(self, anim_type):
        if anim_type == "crouch":
            self.is_crouching = True
        else:
            self.is_crouching = False

    def jump(self):
        # Saut uniquement si on est au sol ou sur une plateforme
        if not self.is_jumping:
            self.vel_y = self.jump_speed
            self.is_jumping = True
            self.jump_held = True
            self.jump_hold_time = 0

    def jump_hold(self):
        # Maintenir le saut pour sauter plus haut
        if self.is_jumping and self.jump_held and self.jump_hold_time < self.max_jump_hold:
            self.vel_y += self.jump_boost
            self.jump_hold_time += 1

    def jump_release(self):
        # Relacher le saut
        self.jump_held = False

    def is_out_of_screen(self):
        # Verifier si le joueur sort de l'ecran (gauche ou bas)
        return self.rect.right < 0 or self.rect.top > HEIGHT

    def update(self, platforms=None):
        # Maintenir le saut si la touche est enfoncee
        if self.jump_held and self.is_jumping:
            self.jump_hold()

        # Sauvegarder position avant mouvement
        old_bottom = self.rect.bottom

        # Appliquer la gravite
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Collision avec les plateformes (seulement en descendant)
        self.on_platform = False
        if platforms and self.vel_y > 0:
            for platform in platforms:
                # Collision simple : si on touche la plateforme
                if self.rect.colliderect(platform.rect):
                    # Verifier qu'on vient du dessus (pas du cote)
                    if old_bottom <= platform.rect.centery:
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.is_jumping = False
                        self.on_platform = True
                        break

        # Ne pas traverser le sol
        if self.rect.bottom > self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
            self.is_jumping = False
        
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

        # Mettre a jour la hitbox
        self.hitbox = self.rect.inflate(-20, -10)
        self.hitbox.center = self.rect.center


class Obstacle(pygame.sprite.Sprite):
    # Variable de classe pour suivre le dernier type d'obstacle
    last_type = None
    last_x = 0

    def __init__(self, speed, x_offset=0):
        super().__init__()

        # Choisir un type d'obstacle (tous les types)
        if Obstacle.last_type == "air":
            # Apres un corbeau, obstacle au sol
            img_path = random.choice([SPIDER_IMG, HYDE_IMG])
            Obstacle.last_type = "ground"
        else:
            # Sinon, un des trois types
            img_path = random.choice([SPIDER_IMG, HYDE_IMG, CORBEAU_IMG])
            Obstacle.last_type = "air" if img_path == CORBEAU_IMG else "ground"

        self.img_path = img_path
        image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.smoothscale(image, (55, 55))
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-15, -15)

        self.speed = speed

        # Position Y selon le type
        if img_path == CORBEAU_IMG:
            # Corbeau en l'air - assez haut pour passer dessous
            self.rect.bottom = HEIGHT - 250
        else:
            # Araignee et Hyde au sol
            self.rect.bottom = HEIGHT - 70

        # Position X avec espacement
        self.rect.left = WIDTH + x_offset + random.randint(200, 350)
        Obstacle.last_x = self.rect.left

    def update(self):
        self.rect.x -= self.speed
        self.hitbox.center = self.rect.center

        if self.rect.right < 0:
            self.reset()


    def reset(self):
        # Choisir un type (eviter 2 corbeaux de suite)
        if Obstacle.last_type == "air":
            img_path = random.choice([SPIDER_IMG, HYDE_IMG])
            Obstacle.last_type = "ground"
        else:
            img_path = random.choice([SPIDER_IMG, HYDE_IMG, CORBEAU_IMG])
            Obstacle.last_type = "air" if img_path == CORBEAU_IMG else "ground"

        self.img_path = img_path
        image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.smoothscale(image, (55, 55))
        self.rect = self.image.get_rect()

        # Position Y selon le type
        if img_path == CORBEAU_IMG:
            self.rect.bottom = HEIGHT - 250
        else:
            self.rect.bottom = HEIGHT - 70

        # Espacement
        min_x = max(WIDTH, Obstacle.last_x) + random.randint(300, 450)
        self.rect.left = min_x
        Obstacle.last_x = self.rect.left

        self.hitbox = self.rect.inflate(-15, -15)
        self.hitbox.center = self.rect.center

        self.speed = min(self.speed + 0.1, 10)            