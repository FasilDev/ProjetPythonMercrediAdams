import json
from pathlib import Path

FICHIER_SAUVEGARDE = Path(__file__).parent / "sauvegarde.json"


class DonneesJoueur:
    def __init__(self):
        self.pieces = 0
        self.meilleur_score = 0
        self.objets = {
            "bougie": 0,
            "araignee": 0,
            "violon": 0,
            "grimoire": 0
        }
        self.charger()

    def charger(self):
        """Charger les donnees depuis le fichier"""
        if FICHIER_SAUVEGARDE.exists():
            try:
                with open(FICHIER_SAUVEGARDE, "r") as f:
                    donnees = json.load(f)
                    self.pieces = donnees.get("pieces", 0)
                    self.meilleur_score = donnees.get("meilleur_score", 0)
                    self.objets = donnees.get("objets", self.objets)
            except:
                pass

    def sauvegarder(self):
        """Sauvegarder les donnees dans le fichier"""
        donnees = {
            "pieces": self.pieces,
            "meilleur_score": self.meilleur_score,
            "objets": self.objets
        }
        with open(FICHIER_SAUVEGARDE, "w") as f:
            json.dump(donnees, f)

    def ajouter_pieces(self, montant):
        """Ajouter des pieces"""
        self.pieces += montant
        self.sauvegarder()

    def verifier_record(self, score):
        """Verifie et met a jour le meilleur score. Retourne True si nouveau record."""
        if score > self.meilleur_score:
            self.meilleur_score = score
            self.sauvegarder()
            return True
        return False

    def depenser_pieces(self, montant):
        """Depenser des pieces (retourne True si succes)"""
        if self.pieces >= montant:
            self.pieces -= montant
            self.sauvegarder()
            return True
        return False

    def acheter_objet(self, nom_objet, prix):
        """Acheter un objet (retourne True si succes)"""
        if self.depenser_pieces(prix):
            if nom_objet in self.objets:
                self.objets[nom_objet] += 1
                self.sauvegarder()
            return True
        return False

    def utiliser_objet(self, nom_objet):
        """Utiliser un objet (retourne True si succes)"""
        if nom_objet in self.objets and self.objets[nom_objet] > 0:
            self.objets[nom_objet] -= 1
            self.sauvegarder()
            return True
        return False

    def obtenir_nombre_objet(self, nom_objet):
        """Obtenir le nombre d'un objet"""
        return self.objets.get(nom_objet, 0)


donnees_joueur = DonneesJoueur()
