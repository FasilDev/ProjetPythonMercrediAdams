import pygame


class BarreVie:
    def __init__(self, x=10, y=50, vie_max=100, largeur=200, hauteur=20):
        self.x = x
        self.y = y
        self.vie_max = vie_max
        self.vie_actuelle = vie_max
        self.largeur = largeur
        self.hauteur = hauteur

        # Couleurs
        self.couleur_fond = (50, 50, 50)
        self.couleur_bordure = (255, 255, 255)
        self.couleur_vie = (180, 0, 0)
        self.couleur_vie_basse = (255, 0, 0)

        # Invincibilite temporaire apres degats
        self.invincible = False
        self.timer_invincible = 0
        self.duree_invincible = 60  # 1 seconde a 60 FPS

    def subir_degats(self, montant=20):
        if not self.invincible:
            self.vie_actuelle = max(0, self.vie_actuelle - montant)
            self.invincible = True
            self.timer_invincible = self.duree_invincible
            return True
        return False

    def soigner(self, montant=10):
        self.vie_actuelle = min(self.vie_max, self.vie_actuelle + montant)

    def est_mort(self):
        return self.vie_actuelle <= 0

    def reinitialiser(self):
        self.vie_actuelle = self.vie_max
        self.invincible = False
        self.timer_invincible = 0

    def mise_a_jour(self):
        if self.invincible:
            self.timer_invincible -= 1
            if self.timer_invincible <= 0:
                self.invincible = False

    def dessiner(self, ecran, offset_x=0, offset_y=0):
        x = self.x + offset_x
        y = self.y + offset_y

        # Fond de la barre
        pygame.draw.rect(ecran, self.couleur_fond, (x, y, self.largeur, self.hauteur))

        # Barre de vie
        ratio_vie = self.vie_actuelle / self.vie_max
        largeur_vie = int(self.largeur * ratio_vie)

        # Couleur selon le niveau de vie
        if ratio_vie < 0.3:
            couleur = self.couleur_vie_basse
        else:
            couleur = self.couleur_vie

        # Clignotement si invincible
        if self.invincible and self.timer_invincible % 10 < 5:
            couleur = (255, 255, 255)

        if largeur_vie > 0:
            pygame.draw.rect(ecran, couleur, (x, y, largeur_vie, self.hauteur))

        # Bordure
        pygame.draw.rect(ecran, self.couleur_bordure, (x, y, self.largeur, self.hauteur), 2)
