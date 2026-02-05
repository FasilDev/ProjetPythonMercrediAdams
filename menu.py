import pygame
import os
import math
from pathlib import Path
from parametres import parametres, NOMS_TOUCHES

ASSETS = Path(__file__).parent / "assets"


def dessiner_bouton(ecran, rect, texte, police, est_survole, est_selectionne=False):
    """Dessine un bouton moderne gothique"""

    # Couleurs
    if est_selectionne:
        couleur_fond = (120, 60, 120)
        couleur_bordure = (200, 150, 200)
        couleur_texte = (255, 220, 255)
    elif est_survole:
        couleur_fond = (80, 40, 80)
        couleur_bordure = (180, 120, 180)
        couleur_texte = (255, 255, 255)
    else:
        couleur_fond = (40, 20, 40)
        couleur_bordure = (100, 60, 100)
        couleur_texte = (200, 180, 200)

    # Ombre portee
    rect_ombre = rect.copy()
    rect_ombre.x += 4
    rect_ombre.y += 4
    pygame.draw.rect(ecran, (15, 5, 15), rect_ombre, border_radius=12)

    # Fond du bouton
    pygame.draw.rect(ecran, couleur_fond, rect, border_radius=10)

    # Effet de brillance en haut
    rect_brillance = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 4, rect.height // 3)
    surface_brillance = pygame.Surface((rect_brillance.width, rect_brillance.height), pygame.SRCALPHA)
    pygame.draw.rect(surface_brillance, (255, 255, 255, 20), (0, 0, rect_brillance.width, rect_brillance.height), border_radius=8)
    ecran.blit(surface_brillance, rect_brillance)

    # Bordure
    pygame.draw.rect(ecran, couleur_bordure, rect, 2, border_radius=10)

    # Texte centre
    surface_texte = police.render(texte, True, couleur_texte)
    rect_texte = surface_texte.get_rect(center=rect.center)
    ecran.blit(surface_texte, rect_texte)

    # Effet de lueur si survol
    if est_survole:
        lueur = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(lueur, (150, 100, 150, 30), (0, 0, rect.width + 10, rect.height + 10), border_radius=15)
        ecran.blit(lueur, (rect.x - 5, rect.y - 5))


def afficher_menu(ecran):
    horloge = pygame.time.Clock()

    pygame.mixer.music.load(ASSETS / "Cimetiere.mp3")
    pygame.mixer.music.set_volume(parametres.volume_musique)
    pygame.mixer.music.play(-1)

    # Charger les frames du menu
    frames_originales = [
        pygame.image.load(ASSETS / "menu" / "menu_0.png").convert(),
        pygame.image.load(ASSETS / "menu" / "menu_1.png").convert(),
    ]

    index_frame = 0
    derniere_anim = 0
    delai_anim = 150

    # Charger les frames du titre
    titre_frames = []
    titre_path = ASSETS / "menu" / "titre"
    if titre_path.exists():
        for filename in sorted(os.listdir(titre_path)):
            if filename.endswith(".gif") or filename.endswith(".png"):
                img = pygame.image.load(titre_path / filename).convert_alpha()
                titre_frames.append(img)

    titre_i = 0
    titre_last = 0
    titre_delay = 70

    # Animation des boutons
    temps_anim_bouton = 0

    while True:
        horloge.tick(60)
        largeur, hauteur = ecran.get_size()

        # Redimensionner les frames
        frames_redim = [pygame.transform.scale(img, (largeur, hauteur)) for img in frames_originales]

        # Polices adaptees
        taille_police = max(28, int(hauteur * 0.055))
        police = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", taille_police)

        # Taille des boutons
        largeur_btn = max(220, int(largeur * 0.18))
        hauteur_btn = max(50, int(hauteur * 0.1))
        espacement_btn = int(hauteur * 0.025)

        # Animation subtile des boutons
        temps_anim_bouton += 0.05
        decalage_bouton = math.sin(temps_anim_bouton) * 2

        # Position des boutons (centres)
        centre_x = largeur // 2
        debut_y = int(hauteur * 0.4)

        bouton_jouer = pygame.Rect(
            centre_x - largeur_btn // 2,
            debut_y + decalage_bouton,
            largeur_btn, hauteur_btn
        )
        bouton_boutique = pygame.Rect(
            centre_x - largeur_btn // 2,
            debut_y + hauteur_btn + espacement_btn,
            largeur_btn, hauteur_btn
        )
        bouton_parametres = pygame.Rect(
            centre_x - largeur_btn // 2,
            debut_y + (hauteur_btn + espacement_btn) * 2,
            largeur_btn, hauteur_btn
        )
        bouton_quitter = pygame.Rect(
            centre_x - largeur_btn // 2,
            debut_y + (hauteur_btn + espacement_btn) * 3,
            largeur_btn, hauteur_btn
        )

        souris_x, souris_y = pygame.mouse.get_pos()

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return "quit"

            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if bouton_jouer.collidepoint(souris_x, souris_y):
                    pygame.mixer.music.stop()
                    return "jouer"
                if bouton_boutique.collidepoint(souris_x, souris_y):
                    pygame.mixer.music.stop()
                    return "boutique"
                if bouton_parametres.collidepoint(souris_x, souris_y):
                    afficher_parametres(ecran)
                if bouton_quitter.collidepoint(souris_x, souris_y):
                    pygame.mixer.music.stop()
                    return "quit"

        # Animation du fond
        maintenant = pygame.time.get_ticks()
        if maintenant - derniere_anim >= delai_anim:
            derniere_anim = maintenant
            index_frame = (index_frame + 1) % len(frames_redim)

        # Animation du titre
        if titre_frames and maintenant - titre_last >= titre_delay:
            titre_last = maintenant
            titre_i = (titre_i + 1) % len(titre_frames)

        # Affichage du fond
        ecran.blit(frames_redim[index_frame], (0, 0))

        # Overlay leger pour assombrir
        overlay = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 50))
        ecran.blit(overlay, (0, 0))

        # Affichage du titre en haut a droite (plus haut)
        if titre_frames:
            marge_droite = 80  # 50px de plus vers la gauche
            marge_haut = -85   # 50px de plus vers le haut
            titre_img = titre_frames[titre_i]
            ecran.blit(titre_img, (largeur - titre_img.get_width() - marge_droite, marge_haut))

        # Dessiner les boutons
        dessiner_bouton(ecran, bouton_jouer, "JOUER", police,
                       bouton_jouer.collidepoint(souris_x, souris_y))
        dessiner_bouton(ecran, bouton_boutique, "BOUTIQUE", police,
                       bouton_boutique.collidepoint(souris_x, souris_y))
        dessiner_bouton(ecran, bouton_parametres, "PARAMETRES", police,
                       bouton_parametres.collidepoint(souris_x, souris_y))
        dessiner_bouton(ecran, bouton_quitter, "QUITTER", police,
                       bouton_quitter.collidepoint(souris_x, souris_y))

        pygame.display.flip()


def afficher_pause(ecran, capture_fond):
    horloge = pygame.time.Clock()
    largeur, hauteur = ecran.get_size()

    # Polices
    taille_police_titre = max(60, int(hauteur * 0.12))
    taille_police = max(24, int(hauteur * 0.045))
    police_titre = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", taille_police_titre)
    police = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", taille_police)

    # Taille des boutons
    largeur_btn = max(200, int(largeur * 0.16))
    hauteur_btn = max(45, int(hauteur * 0.08))
    espacement_btn = int(hauteur * 0.02)

    centre_x = largeur // 2
    debut_y = int(hauteur * 0.40)

    bouton_continuer = pygame.Rect(
        centre_x - largeur_btn // 2,
        debut_y,
        largeur_btn, hauteur_btn
    )
    bouton_parametres = pygame.Rect(
        centre_x - largeur_btn // 2,
        debut_y + hauteur_btn + espacement_btn,
        largeur_btn, hauteur_btn
    )
    bouton_quitter = pygame.Rect(
        centre_x - largeur_btn // 2,
        debut_y + (hauteur_btn + espacement_btn) * 2,
        largeur_btn, hauteur_btn
    )

    while True:
        horloge.tick(60)
        souris_x, souris_y = pygame.mouse.get_pos()

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return "quit"

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return "continuer"

            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if bouton_continuer.collidepoint(souris_x, souris_y):
                    return "continuer"
                if bouton_parametres.collidepoint(souris_x, souris_y):
                    afficher_parametres(ecran)
                if bouton_quitter.collidepoint(souris_x, souris_y):
                    return "quit"

        # Fond avec capture du jeu
        ecran.blit(capture_fond, (0, 0))

        # Overlay sombre
        overlay = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        ecran.blit(overlay, (0, 0))

        # Panneau central
        largeur_panneau = int(largeur * 0.35)
        hauteur_panneau = int(hauteur * 0.55)
        rect_panneau = pygame.Rect(
            centre_x - largeur_panneau // 2,
            hauteur // 2 - hauteur_panneau // 2,
            largeur_panneau, hauteur_panneau
        )

        # Fond du panneau
        surface_panneau = pygame.Surface((largeur_panneau, hauteur_panneau), pygame.SRCALPHA)
        pygame.draw.rect(surface_panneau, (20, 10, 25, 230), (0, 0, largeur_panneau, hauteur_panneau), border_radius=15)
        pygame.draw.rect(surface_panneau, (100, 60, 100), (0, 0, largeur_panneau, hauteur_panneau), 3, border_radius=15)
        ecran.blit(surface_panneau, rect_panneau)

        # Titre "PAUSE"
        texte_pause = police_titre.render("PAUSE", True, (200, 150, 200))
        ombre_pause = police_titre.render("PAUSE", True, (30, 15, 30))
        rect_pause = texte_pause.get_rect(center=(centre_x, int(hauteur * 0.32)))
        ecran.blit(ombre_pause, (rect_pause.x + 3, rect_pause.y + 3))
        ecran.blit(texte_pause, rect_pause)

        # Boutons
        dessiner_bouton(ecran, bouton_continuer, "CONTINUER", police,
                       bouton_continuer.collidepoint(souris_x, souris_y))
        dessiner_bouton(ecran, bouton_parametres, "PARAMETRES", police,
                       bouton_parametres.collidepoint(souris_x, souris_y))
        dessiner_bouton(ecran, bouton_quitter, "MENU", police,
                       bouton_quitter.collidepoint(souris_x, souris_y))

        pygame.display.flip()


def afficher_parametres(ecran):
    """Affiche le menu des parametres"""
    horloge = pygame.time.Clock()

    # Variable pour savoir si on attend une touche
    attente_touche = None

    while True:
        horloge.tick(60)
        largeur, hauteur = ecran.get_size()

        # Polices
        taille_police_titre = max(50, int(hauteur * 0.1))
        taille_police = max(22, int(hauteur * 0.04))
        taille_police_petite = max(16, int(hauteur * 0.03))
        police_titre = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", taille_police_titre)
        police = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", taille_police)
        police_petite = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", taille_police_petite)

        centre_x = largeur // 2

        # Curseur de volume
        largeur_curseur = int(largeur * 0.3)
        hauteur_curseur = 12
        x_curseur = centre_x - largeur_curseur // 2
        y_curseur = int(hauteur * 0.35)
        rect_curseur = pygame.Rect(x_curseur, y_curseur, largeur_curseur, hauteur_curseur)

        # Position du pointeur du curseur
        x_pointeur = x_curseur + int(parametres.volume_musique * largeur_curseur)
        rect_pointeur = pygame.Rect(x_pointeur - 8, y_curseur - 6, 16, hauteur_curseur + 12)

        # Boutons pour les touches (4 emplacements)
        boutons_touches = []
        y_debut_touches = int(hauteur * 0.48)
        largeur_btn_touche = int(largeur * 0.08)
        hauteur_btn_touche = int(hauteur * 0.07)
        espacement_touches = int(largeur * 0.03)
        largeur_totale_touches = 4 * largeur_btn_touche + 3 * espacement_touches
        x_debut_touches = centre_x - largeur_totale_touches // 2

        noms_objets = ["Bougie", "Araignee", "Violon", "Grimoire"]

        for i in range(4):
            x = x_debut_touches + i * (largeur_btn_touche + espacement_touches)
            boutons_touches.append(pygame.Rect(x, y_debut_touches, largeur_btn_touche, hauteur_btn_touche))

        # Bouton retour
        largeur_btn = max(180, int(largeur * 0.14))
        hauteur_btn = max(45, int(hauteur * 0.08))
        bouton_retour = pygame.Rect(
            centre_x - largeur_btn // 2,
            int(hauteur * 0.78),
            largeur_btn, hauteur_btn
        )

        souris_x, souris_y = pygame.mouse.get_pos()

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return "quit"

            if evenement.type == pygame.KEYDOWN:
                if attente_touche is not None:
                    parametres.definir_touche_objet(attente_touche, evenement.key)
                    attente_touche = None
                elif evenement.key == pygame.K_ESCAPE:
                    return "menu"

            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if rect_curseur.collidepoint(souris_x, souris_y) or rect_pointeur.collidepoint(souris_x, souris_y):
                    nouveau_vol = (souris_x - x_curseur) / largeur_curseur
                    nouveau_vol = max(0, min(1, nouveau_vol))
                    parametres.definir_volume_musique(nouveau_vol)

                for i, btn in enumerate(boutons_touches):
                    if btn.collidepoint(souris_x, souris_y):
                        attente_touche = i

                if bouton_retour.collidepoint(souris_x, souris_y):
                    return "menu"

            if evenement.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if rect_curseur.collidepoint(souris_x, souris_y) or abs(souris_y - y_curseur) < 20:
                    nouveau_vol = (souris_x - x_curseur) / largeur_curseur
                    nouveau_vol = max(0, min(1, nouveau_vol))
                    parametres.definir_volume_musique(nouveau_vol)

        # Fond sombre
        ecran.fill((25, 15, 30))

        # Panneau central
        largeur_panneau = int(largeur * 0.55)
        hauteur_panneau = int(hauteur * 0.75)
        rect_panneau = pygame.Rect(
            centre_x - largeur_panneau // 2,
            int(hauteur * 0.12),
            largeur_panneau, hauteur_panneau
        )
        surface_panneau = pygame.Surface((largeur_panneau, hauteur_panneau), pygame.SRCALPHA)
        pygame.draw.rect(surface_panneau, (35, 20, 40, 240), (0, 0, largeur_panneau, hauteur_panneau), border_radius=15)
        pygame.draw.rect(surface_panneau, (100, 60, 100), (0, 0, largeur_panneau, hauteur_panneau), 3, border_radius=15)
        ecran.blit(surface_panneau, rect_panneau)

        # Titre
        titre = police_titre.render("PARAMETRES", True, (200, 150, 200))
        ombre_titre = police_titre.render("PARAMETRES", True, (30, 15, 30))
        rect_titre = titre.get_rect(center=(centre_x, int(hauteur * 0.2)))
        ecran.blit(ombre_titre, (rect_titre.x + 3, rect_titre.y + 3))
        ecran.blit(titre, rect_titre)

        # Section Volume
        label_vol = police.render("Volume Musique", True, (220, 200, 220))
        ecran.blit(label_vol, (centre_x - label_vol.get_width() // 2, y_curseur - 35))

        # Fond du curseur
        pygame.draw.rect(ecran, (60, 40, 60), rect_curseur, border_radius=6)

        # Remplissage du curseur
        largeur_rempli = int(parametres.volume_musique * largeur_curseur)
        rect_rempli = pygame.Rect(x_curseur, y_curseur, largeur_rempli, hauteur_curseur)
        pygame.draw.rect(ecran, (150, 100, 150), rect_rempli, border_radius=6)

        # Pointeur
        pygame.draw.rect(ecran, (200, 150, 200), rect_pointeur, border_radius=4)
        pygame.draw.rect(ecran, (255, 220, 255), rect_pointeur, 2, border_radius=4)

        # Pourcentage
        texte_pct = police_petite.render(f"{int(parametres.volume_musique * 100)}%", True, (255, 255, 255))
        ecran.blit(texte_pct, (x_curseur + largeur_curseur + 15, y_curseur - 2))

        # Section Touches
        label_touches = police.render("Touches des Objets", True, (220, 200, 220))
        ecran.blit(label_touches, (centre_x - label_touches.get_width() // 2, y_debut_touches - 40))

        # Boutons de touches
        for i, btn in enumerate(boutons_touches):
            en_attente = (attente_touche == i)
            est_survole = btn.collidepoint(souris_x, souris_y)

            if en_attente:
                couleur_fond = (100, 60, 100)
                couleur_bordure = (255, 200, 255)
                couleur_texte = (255, 255, 150)
            elif est_survole:
                couleur_fond = (70, 45, 70)
                couleur_bordure = (180, 120, 180)
                couleur_texte = (255, 255, 255)
            else:
                couleur_fond = (50, 30, 50)
                couleur_bordure = (100, 60, 100)
                couleur_texte = (200, 180, 200)

            pygame.draw.rect(ecran, couleur_fond, btn, border_radius=8)
            pygame.draw.rect(ecran, couleur_bordure, btn, 2, border_radius=8)

            if en_attente:
                texte_touche = police.render("...", True, couleur_texte)
            else:
                nom_touche = parametres.obtenir_nom_touche(parametres.touches_objets[i])
                texte_touche = police.render(nom_touche, True, couleur_texte)

            rect_texte_touche = texte_touche.get_rect(center=btn.center)
            ecran.blit(texte_touche, rect_texte_touche)

            nom_objet = police_petite.render(noms_objets[i], True, (180, 160, 180))
            ecran.blit(nom_objet, (btn.x + btn.width // 2 - nom_objet.get_width() // 2, btn.y + btn.height + 5))

        # Instructions
        if attente_touche is not None:
            instr = police_petite.render("Appuyez sur une touche...", True, (255, 220, 150))
        else:
            instr = police_petite.render("Cliquez pour changer une touche", True, (150, 130, 150))
        ecran.blit(instr, (centre_x - instr.get_width() // 2, y_debut_touches + hauteur_btn_touche + 45))

        # Bouton Retour
        dessiner_bouton(ecran, bouton_retour, "RETOUR", police,
                       bouton_retour.collidepoint(souris_x, souris_y))

        pygame.display.flip()
