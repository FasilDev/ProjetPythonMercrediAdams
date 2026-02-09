import pygame
from pathlib import Path
from donnees_joueur import donnees_joueur
from parametres import parametres

ASSETS = Path(__file__).parent / "assets"


def afficher_boutique(ecran):
    
    fond_boutique = pygame.image.load(ASSETS / "boutique" / "Boutique_Wednesday.webp").convert()

    img_bougie = pygame.image.load(ASSETS / "boutique" / "Bougie_boutique.webp").convert_alpha()
    img_araignee = pygame.image.load(ASSETS / "boutique" / "Araignee_boutique.webp").convert_alpha()
    img_violon = pygame.image.load(ASSETS / "boutique" / "Violon_boutique.webp").convert_alpha()
    img_grimoire = pygame.image.load(ASSETS / "boutique" / "Grimoire_boutique.webp").convert_alpha()

    try:
        son_achat = pygame.mixer.Sound("assets/cash.wav")
        son_achat.set_volume(parametres.volume_effets)
    except:
        son_achat = None

    noms_touches = [parametres.obtenir_nom_touche(t) for t in parametres.touches_objets]
    objets = [
        {"nom": "Bougie", "cle": "bougie", "effet": f"Ralentit le jeu 10s (touche {noms_touches[0]})", "prix": 50, "image": img_bougie},
        {"nom": "Araignee", "cle": "araignee", "effet": f"Invincibilite 3s (touche {noms_touches[1]})", "prix": 100, "image": img_araignee},
        {"nom": "Violon", "cle": "violon", "effet": f"Double le score 15s (touche {noms_touches[2]})", "prix": 75, "image": img_violon},
        {"nom": "Grimoire", "cle": "grimoire", "effet": f"Restaure 50% vie (touche {noms_touches[3]})", "prix": 150, "image": img_grimoire}
    ]

    message = None
    timer_message = 0
    horloge = pygame.time.Clock()

    while True:
        horloge.tick(60)

        if timer_message > 0:
            timer_message -= 1
        else:
            message = None

        largeur, hauteur = ecran.get_size()

        fond_redim = pygame.transform.scale(fond_boutique, (largeur, hauteur))

        taille_police = max(18, int(hauteur * 0.04))
        taille_police_prix = max(14, int(hauteur * 0.03))
        taille_police_pieces = max(20, int(hauteur * 0.045))
        police = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", taille_police)
        police_prix = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", taille_police_prix)
        police_pieces = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", taille_police_pieces)

        taille_objet = int(hauteur * 0.1)

        rect_violet_x = int(largeur * 0.52) + 300  # 300px vers la droite
        rect_violet_y = int(hauteur * 0.72) - 50   # 50px vers le haut

        espacement = int(largeur * 0.08)

        positions = [
            (rect_violet_x - espacement * 1.5, rect_violet_y),
            (rect_violet_x - espacement * 0.5, rect_violet_y),
            (rect_violet_x + espacement * 0.5, rect_violet_y),
            (rect_violet_x + espacement * 1.5, rect_violet_y)
        ]

        boutons_objets = []
        for pos in positions:
            x = int(pos[0] - taille_objet // 2)
            y = int(pos[1] - taille_objet // 2)
            boutons_objets.append(pygame.Rect(x, y, taille_objet, taille_objet + 25))

        largeur_retour = int(largeur * 0.15)
        hauteur_retour = int(hauteur * 0.07)
        bouton_retour = pygame.Rect(
            largeur // 2 - largeur_retour // 2,
            int(hauteur * 0.88),
            largeur_retour,
            hauteur_retour
        )

        souris_x, souris_y = pygame.mouse.get_pos()

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return "quit"

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return "menu"

            if evenement.type == pygame.MOUSEBUTTONDOWN:
                for i, bouton in enumerate(boutons_objets):
                    if bouton.collidepoint(souris_x, souris_y):
                        objet = objets[i]
                        if donnees_joueur.acheter_objet(objet["cle"], objet["prix"]):
                            message = f"{objet['nom']} achete!"
                            timer_message = 120 
                            if son_achat:
                                son_achat.play()
                        else:
                            message = "Pas assez de pieces!"
                            timer_message = 120

                if bouton_retour.collidepoint(souris_x, souris_y):
                    return "menu"

        ecran.blit(fond_redim, (0, 0))

        texte_pieces = police_pieces.render(f"Pieces: {donnees_joueur.pieces}", True, (255, 215, 0))
        ecran.blit(texte_pieces, (20, 20))

        for i, (bouton, objet) in enumerate(zip(boutons_objets, objets)):
            if bouton.collidepoint(souris_x, souris_y):
                taille = int(taille_objet * 1.15)
                img_redim = pygame.transform.smoothscale(objet["image"], (taille, taille))
                img_x = bouton.x + (taille_objet - taille) // 2
                img_y = bouton.y + (taille_objet - taille) // 2
            else:
                img_redim = pygame.transform.smoothscale(objet["image"], (taille_objet, taille_objet))
                img_x = bouton.x
                img_y = bouton.y

            ecran.blit(img_redim, (img_x, img_y))

            texte_prix = police_prix.render(f"{objet['prix']} pts", True, (255, 215, 0))
            prix_x = bouton.x + (taille_objet - texte_prix.get_width()) // 2
            prix_y = bouton.y + taille_objet + 3
            ecran.blit(texte_prix, (prix_x, prix_y))

            possede = donnees_joueur.obtenir_nombre_objet(objet["cle"])
            if possede > 0:
                texte_possede = police_prix.render(f"x{possede}", True, (150, 255, 150))
                ecran.blit(texte_possede, (bouton.x + taille_objet - 20, bouton.y - 5))

        if message:
            couleur = (150, 255, 150) if "achete" in message else (255, 100, 100)
            texte_msg = police.render(message, True, couleur)
            ecran.blit(texte_msg, (largeur // 2 - texte_msg.get_width() // 2, int(hauteur * 0.35)))

        for i, bouton in enumerate(boutons_objets):
            if bouton.collidepoint(souris_x, souris_y):
                objet = objets[i]
                info_y = int(hauteur * 0.42)
                texte = police.render(f"{objet['nom']}: {objet['effet']}", True, (255, 220, 150))
                ecran.blit(texte, (largeur // 2 - texte.get_width() // 2, info_y))
                break

        couleur = (120, 80, 140) if bouton_retour.collidepoint(souris_x, souris_y) else (60, 30, 60)
        pygame.draw.rect(ecran, couleur, bouton_retour, border_radius=5)
        pygame.draw.rect(ecran, (150, 100, 180), bouton_retour, 2, border_radius=5)
        texte_retour = police.render("RETOUR", True, (255, 255, 255))
        ecran.blit(texte_retour, (
            bouton_retour.x + (bouton_retour.width - texte_retour.get_width()) // 2,
            bouton_retour.y + (bouton_retour.height - texte_retour.get_height()) // 2
        ))

        pygame.display.flip()
