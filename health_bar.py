import pygame


class HealthBar:
    def __init__(self, x=10, y=50, max_health=100, width=200, height=20):
        self.x = x
        self.y = y
        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height

        # Couleurs
        self.bg_color = (50, 50, 50)
        self.border_color = (255, 255, 255)
        self.health_color = (180, 0, 0)
        self.health_color_low = (255, 0, 0)

        # Invincibilite temporaire apres degats
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 60  # 1 seconde a 60 FPS

    def take_damage(self, amount=20):
        if not self.invincible:
            self.current_health = max(0, self.current_health - amount)
            self.invincible = True
            self.invincible_timer = self.invincible_duration
            return True
        return False

    def heal(self, amount=10):
        self.current_health = min(self.max_health, self.current_health + amount)

    def is_dead(self):
        return self.current_health <= 0

    def reset(self):
        self.current_health = self.max_health
        self.invincible = False
        self.invincible_timer = 0

    def update(self):
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def draw(self, screen, offset_x=0, offset_y=0):
        x = self.x + offset_x
        y = self.y + offset_y

        # Fond de la barre
        pygame.draw.rect(screen, self.bg_color, (x, y, self.width, self.height))

        # Barre de vie
        health_ratio = self.current_health / self.max_health
        health_width = int(self.width * health_ratio)

        # Couleur selon le niveau de vie
        if health_ratio < 0.3:
            color = self.health_color_low
        else:
            color = self.health_color

        # Clignotement si invincible
        if self.invincible and self.invincible_timer % 10 < 5:
            color = (255, 255, 255)

        if health_width > 0:
            pygame.draw.rect(screen, color, (x, y, health_width, self.height))

        # Bordure
        pygame.draw.rect(screen, self.border_color, (x, y, self.width, self.height), 2)
