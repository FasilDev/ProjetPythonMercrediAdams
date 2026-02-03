import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.sheet = pygame.image.load("assets/mercrediadamsprite.png").convert_alpha()

        self.frame_w = 30
        self.frame_h = 60

        # Les 5 frames de marche
        self.walk_frames = [0, 1, 2, 3, 4]
        self.walk_i = 0

        self.last_anim = 0
        self.anim_delay = 100  # Ajuste la vitesse ici

        self.set_frame(self.walk_frames[self.walk_i])

        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 300

    def set_frame(self, frame_index):
        x = frame_index * self.frame_w
        self.image = pygame.Surface((self.frame_w, self.frame_h), pygame.SRCALPHA)
        self.image.blit(self.sheet, (0, 0), (x, 0, self.frame_w, self.frame_h))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim >= self.anim_delay:
            self.last_anim = now
            self.walk_i = (self.walk_i + 1) % len(self.walk_frames)
            self.set_frame(self.walk_frames[self.walk_i])