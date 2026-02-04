import pygame
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"
FONT_PATH = ASSETS / "fonts" / "Creepster-Regular.ttf"


class Score:
    def __init__(self, x=10, y=10):
        self.value = 0
        self.x = x
        self.y = y
        self.font = pygame.font.Font(FONT_PATH, 36)
        self.color = (255, 255, 255)
        self.shadow_color = (50, 50, 50)

    def add(self, points=1):
        self.value += points

    def reset(self):
        self.value = 0

    def draw(self, screen, offset_x=0, offset_y=0):
        text = f"Score: {self.value}"

        # Ombre pour meilleure lisibilite
        shadow = self.font.render(text, True, self.shadow_color)
        screen.blit(shadow, (self.x + offset_x + 2, self.y + offset_y + 2))

        # Texte principal
        surface = self.font.render(text, True, self.color)
        screen.blit(surface, (self.x + offset_x, self.y + offset_y))
