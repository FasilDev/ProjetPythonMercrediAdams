import pygame
from pathlib import Path
import random

# Taille d'écran
WIDTH, HEIGHT = 800, 450

# Dossier des assets
ASSETS = Path(__file__).parent / "assets"
SPIDER_IMG = ASSETS / "spider.webp"
HYDE_IMG = ASSETS / "hyde_sprite.png"
HYDE_SHEET = ASSETS / "hyde_sprite.png"   
HYDE_FRAME_W = 265
HYDE_FRAME_H = 415
HYDE_FRAMES = 2
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
        self.ground_y = 380
        self.vel_y = 0
        self.jump_speed = -12
        self.gravity = 0.8

        # Saut variable
        self.is_jumping = False
        self.jump_held = False
        self.jump_hold_time = 0
        self.max_jump_hold = 15
        self.jump_boost = -0.8

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
        if not self.is_jumping:
            self.vel_y = self.jump_speed
            self.is_jumping = True
            self.jump_held = True
            self.jump_hold_time = 0

    def jump_hold(self):
        if self.is_jumping and self.jump_held and self.jump_hold_time < self.max_jump_hold:
            self.vel_y += self.jump_boost
            self.jump_hold_time += 1

    def jump_release(self):
        self.jump_held = False

    def is_out_of_screen(self):
        return self.rect.right < 0 or self.rect.top > HEIGHT

    def update(self, platforms=None):
        if self.jump_held and self.is_jumping:
            self.jump_hold()

        old_bottom = self.rect.bottom

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        self.on_platform = False
        if platforms and self.vel_y > 0:
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if old_bottom <= platform.rect.top:
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.is_jumping = False
                        self.on_platform = True
                        break

        if self.rect.bottom > self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
            self.is_jumping = False
        
        self.timer += 1
        
        if self.timer >= 7:
            self.timer = 0
            self.frame += 1
            
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
            
            self.rect = self.image.get_rect()
            self.rect.x = old_x
            self.rect.y = old_y

        self.hitbox = self.rect.inflate(-20, -10)
        self.hitbox.center = self.rect.center


class Obstacle(pygame.sprite.Sprite):
    last_type = None
    last_x = 0

    def __init__(self, speed, x_offset=0):
        super().__init__()

        self.speed = speed

        #si obstacle bougent = animation 
        self.is_animated = (self.speed > 0)

        # Animation Hyde
        self.hyde_sheet = None
        self.hyde_i = 0
        self.hyde_last = 0
        self.hyde_delay = 90

        self.set_type()

        # Position Y - Hyde au sol
        self.rect.bottom = HEIGHT - 40

        # Position X
        self.rect.left = WIDTH + x_offset + random.randint(200, 350)
        Obstacle.last_x = self.rect.left

    def set_type(self):
        """Charge Hyde statique ou animé"""
        
        if self.is_animated:
            # Hyde ANIMÉ (avec sprite sheet)
            self.hyde_sheet = pygame.image.load(HYDE_SHEET).convert_alpha()
            self.hyde_i = 0
            self.hyde_last = 0
            self.image = self.get_hyde_frame(self.hyde_i)
        else:
            # Hyde STATIQUE (juste la première pose)
            self.hyde_sheet = pygame.image.load(HYDE_SHEET).convert_alpha()
            self.image = self.get_hyde_frame(0)  # Toujours la frame 0

        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-15, -15)

    def get_hyde_frame(self, i):
        """Découpe une frame dans la sheet Hyde."""
        x = i * HYDE_FRAME_W
        frame = pygame.Surface((HYDE_FRAME_W, HYDE_FRAME_H), pygame.SRCALPHA)
        frame.blit(self.hyde_sheet, (0, 0), (x, 0, HYDE_FRAME_W, HYDE_FRAME_H))
        frame = pygame.transform.smoothscale(frame, (90, 135))
        return frame

    def update(self):
        self.rect.x -= self.speed

        # Animation SEULEMENT si Hyde est animé
        if self.is_animated:
            now = pygame.time.get_ticks()
            if now - self.hyde_last >= self.hyde_delay:
                self.hyde_last = now
                self.hyde_i = (self.hyde_i + 1) % HYDE_FRAMES

                old_center = self.rect.center
                self.image = self.get_hyde_frame(self.hyde_i)
                self.rect = self.image.get_rect(center=old_center)

        self.hitbox = self.rect.inflate(-15, -15)
        self.hitbox.center = self.rect.center

        if self.rect.right < 0:
            self.reset()

    def reset(self):
        # Rechoisir aléatoirement statique ou animé
        self.is_animated = (self.speed > 0)
        
        self.set_type()

        # Position Y - Hyde au sol
        self.rect.bottom = HEIGHT - 40

        # Espacement
        min_x = max(WIDTH, Obstacle.last_x) + random.randint(300, 450)
        self.rect.left = min_x
        Obstacle.last_x = self.rect.left

        self.hitbox = self.rect.inflate(-15, -15)
        self.hitbox.center = self.rect.center

        # Augmenter la vitesse
        self.speed = min(self.speed + 0.1, 10)