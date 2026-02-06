import pygame
import json
from pathlib import Path

FICHIER_PARAMETRES = Path(__file__).parent / "parametres.json"

# Noms des touches pour l'affichage
NOMS_TOUCHES = {
    pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3", pygame.K_4: "4",
    pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8",
    pygame.K_9: "9", pygame.K_0: "0",
    pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D",
    pygame.K_e: "E", pygame.K_f: "F", pygame.K_g: "G", pygame.K_h: "H",
    pygame.K_i: "I", pygame.K_j: "J", pygame.K_k: "K", pygame.K_l: "L",
    pygame.K_m: "M", pygame.K_n: "N", pygame.K_o: "O", pygame.K_p: "P",
    pygame.K_q: "Q", pygame.K_r: "R", pygame.K_s: "S", pygame.K_t: "T",
    pygame.K_u: "U", pygame.K_v: "V", pygame.K_w: "W", pygame.K_x: "X",
    pygame.K_y: "Y", pygame.K_z: "Z",
    pygame.K_F1: "F1", pygame.K_F2: "F2", pygame.K_F3: "F3", pygame.K_F4: "F4",
    pygame.K_F5: "F5", pygame.K_F6: "F6", pygame.K_F7: "F7", pygame.K_F8: "F8",
}


class Parametres:
    def __init__(self):
        # Valeurs par defaut
        self.volume_musique = 0.5
        self.volume_effets = 0.6

        # Touches pour les objets (par defaut 1, 2, 3, 4)
        self.touches_objets = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]

        self.charger()

    def charger(self):
        """Charger les parametres depuis le fichier"""
        if FICHIER_PARAMETRES.exists():
            try:
                with open(FICHIER_PARAMETRES, "r") as f:
                    donnees = json.load(f)
                    self.volume_musique = donnees.get("volume_musique", 0.5)
                    self.volume_effets = donnees.get("volume_effets", 0.6)
                    # Charger les touches
                    touches = donnees.get("touches_objets", [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4])
                    self.touches_objets = [int(t) for t in touches]
            except:
                pass

    def sauvegarder(self):
        """Sauvegarder les parametres"""
        donnees = {
            "volume_musique": self.volume_musique,
            "volume_effets": self.volume_effets,
            "touches_objets": self.touches_objets
        }
        with open(FICHIER_PARAMETRES, "w") as f:
            json.dump(donnees, f)

    def definir_volume_musique(self, volume):
        self.volume_musique = max(0, min(1, volume))
        pygame.mixer.music.set_volume(self.volume_musique)
        self.sauvegarder()

    def definir_touche_objet(self, index_slot, touche):
        if 0 <= index_slot < 4:
            self.touches_objets[index_slot] = touche
            self.sauvegarder()

    def obtenir_nom_touche(self, touche):
        return NOMS_TOUCHES.get(touche, "?")


# Instance globale
parametres = Parametres()
