import pygame
from pathlib import Path
from donnees_joueur import donnees_joueur
from parametres import parametres

ASSETS = Path(__file__).parent / "assets"


class Inventaire:
    def __init__(self):
        # Charger les images des objets
        self.images = {
            "bougie": pygame.image.load(ASSETS / "boutique" / "Bougie_boutique.webp").convert_alpha(),
            "araignee": pygame.image.load(ASSETS / "boutique" / "Araignee_boutique.webp").convert_alpha(),
            "violon": pygame.image.load(ASSETS / "boutique" / "Violon_boutique.webp").convert_alpha(),
            "grimoire": pygame.image.load(ASSETS / "boutique" / "Grimoire_boutique.webp").convert_alpha()
        }

        # Ordre des emplacements
        self.emplacements = ["bougie", "araignee", "violon", "grimoire"]

        # Taille
        self.taille_emplacement = 50
        self.espacement = 5

        # Police
        self.police = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", 14)

        # Effets actifs
        self.effets_actifs = {
            "bougie": {"actif": False, "timer": 0, "duree": 600},      # ralenti
            "araignee": {"actif": False, "timer": 0, "duree": 180},    # 3s invincibilite
            "violon": {"actif": False, "timer": 0, "duree": 900},      # 15s double score
            "grimoire": {"actif": False, "timer": 0, "duree": 1}       # Instantane
        }

        # temps avant de pouvoir reutiliser un objet
        self.cooldowns = {
            "bougie": {"timer": 0, "duree": 300},      # 5s de cooldown
            "araignee": {"timer": 0, "duree": 600},    # 10s de cooldown
            "violon": {"timer": 0, "duree": 300},      # 5s de cooldown
            "grimoire": {"timer": 0, "duree": 180}     # 3s de cooldown
        }

    def utiliser_objet(self, index_emplacement):
        """Utiliser un objet de l'emplacement (retourne l'effet a appliquer ou None)"""
        if index_emplacement < 0 or index_emplacement >= len(self.emplacements):
            return None

        cle_objet = self.emplacements[index_emplacement]

        if donnees_joueur.obtenir_nombre_objet(cle_objet) > 0:
            en_cooldown = self.cooldowns[cle_objet]["timer"] > 0
            if not en_cooldown:
                if cle_objet == "grimoire" or not self.effets_actifs[cle_objet]["actif"]:
                    if donnees_joueur.utiliser_objet(cle_objet):
                        self.effets_actifs[cle_objet]["actif"] = True
                        self.effets_actifs[cle_objet]["timer"] = self.effets_actifs[cle_objet]["duree"]
                        return cle_objet
        return None

    def mise_a_jour(self):
        """Mettre a jour les timers des effets et cooldowns"""
        for cle, effet in self.effets_actifs.items():
            if effet["actif"] and effet["timer"] > 0:
                effet["timer"] -= 1
                if effet["timer"] <= 0:
                    effet["actif"] = False
                    self.cooldowns[cle]["timer"] = self.cooldowns[cle]["duree"]

        for cle, cooldown in self.cooldowns.items():
            if cooldown["timer"] > 0:
                cooldown["timer"] -= 1

    def effet_est_actif(self, cle_objet):
        """Verifier si un effet est actif"""
        return self.effets_actifs.get(cle_objet, {}).get("actif", False)

    def obtenir_timer_effet(self, cle_objet):
        """Obtenir le timer restant d'un effet"""
        return self.effets_actifs.get(cle_objet, {}).get("timer", 0)

    def gerer_touche(self, touche):
        """Gerer l'appui sur une touche (retourne l'effet ou None)"""
        for i, t in enumerate(parametres.touches_objets):
            if touche == t:
                return self.utiliser_objet(i)
        return None

    def dessiner(self, ecran, decalage_x=0, decalage_y=0):

        largeur_ecran, hauteur_ecran = ecran.get_size()

        largeur_totale = len(self.emplacements) * (self.taille_emplacement + self.espacement) - self.espacement
        debut_x = largeur_ecran // 2 - largeur_totale // 2
        debut_y = hauteur_ecran - self.taille_emplacement - 20

        for i, cle_objet in enumerate(self.emplacements):
            x = debut_x + i * (self.taille_emplacement + self.espacement)
            y = debut_y

            # Fond de l'emplacement
            rect_emplacement = pygame.Rect(x, y, self.taille_emplacement, self.taille_emplacement)

            if self.effets_actifs[cle_objet]["actif"]:
                couleur_fond = (100, 200, 100, 150)  
            elif self.cooldowns[cle_objet]["timer"] > 0:
                couleur_fond = (100, 50, 50, 180)    
            else:
                couleur_fond = (40, 20, 40, 180)

            surface = pygame.Surface((self.taille_emplacement, self.taille_emplacement), pygame.SRCALPHA)
            surface.fill(couleur_fond)
            ecran.blit(surface, (x, y))

            
            pygame.draw.rect(ecran, (100, 70, 100), rect_emplacement, 2)

            nombre = donnees_joueur.obtenir_nombre_objet(cle_objet)
            if nombre > 0:
                img = pygame.transform.smoothscale(self.images[cle_objet], (self.taille_emplacement - 8, self.taille_emplacement - 8))
                ecran.blit(img, (x + 4, y + 4))

                # Nombre d'objets
                texte_nombre = self.police.render(f"x{nombre}", True, (255, 255, 255))
                ecran.blit(texte_nombre, (x + self.taille_emplacement - texte_nombre.get_width() - 2, y + self.taille_emplacement - texte_nombre.get_height()))

            # Touche (configurable)
            nom_touche = parametres.obtenir_nom_touche(parametres.touches_objets[i])
            texte_touche = self.police.render(nom_touche, True, (255, 215, 0))
            ecran.blit(texte_touche, (x + 2, y + 2))

            if self.effets_actifs[cle_objet]["actif"]:
                timer = self.effets_actifs[cle_objet]["timer"]
                secondes = timer // 60
                texte_timer = self.police.render(f"{secondes}s", True, (150, 255, 150))
                ecran.blit(texte_timer, (x + self.taille_emplacement // 2 - texte_timer.get_width() // 2, y - 15))
            elif self.cooldowns[cle_objet]["timer"] > 0:
                timer = self.cooldowns[cle_objet]["timer"]
                secondes = timer // 60 + 1  # Arrondir vers le haut
                texte_timer = self.police.render(f"{secondes}s", True, (255, 100, 100))
                ecran.blit(texte_timer, (x + self.taille_emplacement // 2 - texte_timer.get_width() // 2, y - 15))
