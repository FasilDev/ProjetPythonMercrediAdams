import pygame
from pathlib import Path
import random

# Taille d'ecran
WIDTH, HEIGHT = 800, 450

# Dossier des assets
ASSETS = Path(__file__).parent / "assets"
SPIDER_IMG = ASSETS / "spider.webp"
HYDE_SHEET = ASSETS / "hyde_sprite.png"
HYDE_FRAME_W = 265
HYDE_FRAME_H = 415
HYDE_FRAMES = 2
CORBEAU_IMG = ASSETS / "ravenfly.png"
CORBEAU_FRAME_W = 64  # ✅ Corrigé (au lieu de 128)
CORBEAU_FRAME_H = 64  # ✅ Hauteur correcte
CORBEAU_FRAMES = 4


class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Charger les sprites
        self.sheet_marche = pygame.image.load("assets/mercrediadamspritemarche.png").convert_alpha()
        self.sheet_accroupi = pygame.image.load("assets/mercrediadamspritecouche.png").convert_alpha()

        # Taille d'une frame
        self.marche_w = 43
        self.marche_h = 55
        self.accroupi_w = 52
        self.accroupi_h = 55

        # Animation
        self.frame = 0
        self.est_accroupi = False
        self.timer = 0

        # Saut
        self.sol_y = 380
        self.vel_y = 0
        self.vitesse_saut = -10
        self.gravite = 0.8

        # Saut variable
        self.en_saut = False
        self.saut_maintenu = False
        self.temps_saut_maintenu = 0
        self.max_temps_saut = 15
        self.boost_saut = -0.8

        self.image = pygame.Surface((self.marche_w, self.marche_h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = 60
        self.rect.y = self.sol_y

        # Hitbox pour les collisions
        self.hitbox = self.rect.inflate(-20, -10)

    def set_animation(self, type_anim):
        if type_anim == "crouch":
            self.est_accroupi = True
        else:
            self.est_accroupi = False

    def jump(self):
        if not self.en_saut:
            self.vel_y = self.vitesse_saut
            self.en_saut = True
            self.saut_maintenu = True
            self.temps_saut_maintenu = 0

    def jump_hold(self):
        if self.en_saut and self.saut_maintenu and self.temps_saut_maintenu < self.max_temps_saut:
            self.vel_y += self.boost_saut
            self.temps_saut_maintenu += 1

    def jump_release(self):
        self.saut_maintenu = False

    def is_out_of_screen(self):
        return self.rect.right < 0 or self.rect.top > HEIGHT

    def update(self, plateformes=None):
        if self.saut_maintenu and self.en_saut:
            self.jump_hold()

        ancien_bas = self.rect.bottom

        self.vel_y += self.gravite
        self.rect.y += self.vel_y

        self.sur_plateforme = False
        if plateformes and self.vel_y > 0:
            for plateforme in plateformes:
                if self.rect.colliderect(plateforme.rect):
                    if ancien_bas <= plateforme.rect.top:
                        self.rect.bottom = plateforme.rect.top
                        self.vel_y = 0
                        self.en_saut = False
                        self.sur_plateforme = True
                        break

        if self.rect.bottom > self.sol_y:
            self.rect.bottom = self.sol_y
            self.vel_y = 0
            self.en_saut = False

        self.timer += 1

        if self.timer >= 7:
            self.timer = 0
            self.frame += 1

            ancien_x = self.rect.x
            ancien_y = self.rect.y

            if self.est_accroupi:
                if self.frame >= 2:
                    self.frame = 0
                x = self.frame * self.accroupi_w
                self.image = pygame.Surface((self.accroupi_w, self.accroupi_h), pygame.SRCALPHA)
                self.image.blit(self.sheet_accroupi, (0, 0), (x, 0, self.accroupi_w, self.accroupi_h))
                self.image = pygame.transform.scale(self.image, (self.accroupi_w * 2, self.accroupi_h * 2))
            else:
                if self.frame >= 5:
                    self.frame = 0
                x = self.frame * self.marche_w
                self.image = pygame.Surface((self.marche_w, self.marche_h), pygame.SRCALPHA)
                self.image.blit(self.sheet_marche, (0, 0), (x, 0, self.marche_w, self.marche_h))
                self.image = pygame.transform.scale(self.image, (self.marche_w * 2, self.marche_h * 2))

            self.rect = self.image.get_rect()
            self.rect.x = ancien_x
            self.rect.y = ancien_y

        self.hitbox = self.rect.inflate(-20, -10)
        self.hitbox.center = self.rect.center


class Obstacle(pygame.sprite.Sprite):
    dernier_type = None
    last_x = 0

    def __init__(self, speed, x_offset=0):
        super().__init__()

        self.speed = speed

        # Type d'obstacle: "hyde", "araignee", "corbeau"
        self.obstacle_type = None

        # Animation Hyde
        self.hyde_sheet = None
        self.hyde_i = 0
        self.hyde_last = 0
        self.hyde_delay = 90
        self.hyde_mobile = False
        self.hyde_vitesse_extra = 0

        # Animation Corbeau
        self.corbeau_sheet = None
        self.corbeau_i = 0
        self.corbeau_last = 0
        self.corbeau_delay = 100  # ✅ Un peu plus lent pour mieux voir l'animation

        self.set_type()

        # Position X
        self.rect.left = WIDTH + x_offset + random.randint(200, 350)
        Obstacle.last_x = self.rect.left

    def set_type(self):
        """Choisit aleatoirement un type d'obstacle"""

        # Eviter deux corbeaux de suite
        if Obstacle.dernier_type == "corbeau":
            self.obstacle_type = random.choice(["hyde", "araignee"])
        else:
            self.obstacle_type = random.choice(["hyde", "araignee", "corbeau"])

        Obstacle.dernier_type = self.obstacle_type

        # Charger l'image selon le type
        if self.obstacle_type == "hyde":
            self.hyde_sheet = pygame.image.load(HYDE_SHEET).convert_alpha()
            self.hyde_i = 0
            self.hyde_last = 0
            self.hyde_mobile = random.choice([True, False])
            self.hyde_vitesse_extra = 2 if self.hyde_mobile else 0
            self.image = self.get_hyde_frame(self.hyde_i)
            self.rect = self.image.get_rect()
            self.rect.bottom = HEIGHT - 60

        elif self.obstacle_type == "araignee":
            image = pygame.image.load(SPIDER_IMG).convert_alpha()
            self.image = pygame.transform.smoothscale(image, (55, 55))
            self.rect = self.image.get_rect()
            self.rect.bottom = HEIGHT - 70

        elif self.obstacle_type == "corbeau":
            self.corbeau_sheet = pygame.image.load(CORBEAU_IMG).convert_alpha()
            self.corbeau_i = 0
            self.corbeau_last = 0
            self.image = self.get_corbeau_frame(self.corbeau_i)
            self.rect = self.image.get_rect()
            self.rect.bottom = HEIGHT - 250

        # Hitbox reduite
        self.hitbox = self.rect.inflate(-25, -25)

    def get_hyde_frame(self, i):
        """Decoupe une frame dans la sheet Hyde."""
        x = i * HYDE_FRAME_W
        frame = pygame.Surface((HYDE_FRAME_W, HYDE_FRAME_H), pygame.SRCALPHA)
        frame.blit(self.hyde_sheet, (0, 0), (x, 0, HYDE_FRAME_W, HYDE_FRAME_H))
        frame = pygame.transform.smoothscale(frame, (90, 135))
        return frame
    
    def get_corbeau_frame(self, i):
        """Decoupe une frame dans la sheet Corbeau."""
        x = i * CORBEAU_FRAME_W
        frame = pygame.Surface((CORBEAU_FRAME_W, CORBEAU_FRAME_H), pygame.SRCALPHA)
        frame.blit(self.corbeau_sheet, (0, 0), (x, 0, CORBEAU_FRAME_W, CORBEAU_FRAME_H))
        frame = pygame.transform.smoothscale(frame, (80, 80))  # ✅ Taille carrée pour garder les proportions
        return frame

    def update(self):
        # Deplacement
        vitesse_totale = self.speed
        if self.obstacle_type == "hyde" and self.hyde_mobile:
            vitesse_totale += self.hyde_vitesse_extra

        self.rect.x -= vitesse_totale

        # Animation Hyde
        if self.obstacle_type == "hyde":
            now = pygame.time.get_ticks()
            if now - self.hyde_last >= self.hyde_delay:
                self.hyde_last = now
                self.hyde_i = (self.hyde_i + 1) % HYDE_FRAMES

                old_center = self.rect.center
                self.image = self.get_hyde_frame(self.hyde_i)
                self.rect = self.image.get_rect(center=old_center)

        # Animation Corbeau
        if self.obstacle_type == "corbeau":
            now = pygame.time.get_ticks()
            if now - self.corbeau_last >= self.corbeau_delay:
                self.corbeau_last = now
                self.corbeau_i = (self.corbeau_i + 1) % CORBEAU_FRAMES

                old_center = self.rect.center
                self.image = self.get_corbeau_frame(self.corbeau_i)
                self.rect = self.image.get_rect(center=old_center)

        # Hitbox
        self.hitbox = self.rect.inflate(-25, -25)
        self.hitbox.center = self.rect.center

        if self.rect.right < 0:
            self.reset()

    def reset(self):
        # Choisir un nouveau type
        self.set_type()

        # Espacement
        min_x = max(WIDTH, Obstacle.last_x) + random.randint(300, 450)
        self.rect.left = min_x
        Obstacle.last_x = self.rect.left

        # Hitbox
        self.hitbox = self.rect.inflate(-25, -25)
        self.hitbox.center = self.rect.center

        # Augmenter la vitesse
        self.speed = min(self.speed + 0.1, 10)