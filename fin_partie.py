import pygame
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"
CHEMIN_POLICE = ASSETS / "fonts" / "Creepster-Regular.ttf"


def afficher_fin_partie(ecran, score_final):
    """Affiche l'ecran Game Over et retourne le choix du joueur"""
    # Charger le son Game Over
    try:
        son_game_over = pygame.mixer.Sound("assets/Game Over.wav")
        son_game_over.set_volume(0.7)
        son_game_over.play()
    except:
        son_game_over = None
        print("Impossible de charger Game Over.wav")

    horloge = pygame.time.Clock()

    # Polices
    police_titre = pygame.font.Font(CHEMIN_POLICE, 72)
    police_score = pygame.font.Font(CHEMIN_POLICE, 36)
    police_bouton = pygame.font.Font(CHEMIN_POLICE, 32)

    # Couleurs
    couleur_fond = (20, 10, 20)
    couleur_titre = (180, 0, 0)
    couleur_texte = (255, 255, 255)
    couleur_bouton = (60, 40, 60)
    couleur_survol = (100, 70, 100)

    # Taille de base
    LARGEUR_BASE, HAUTEUR_BASE = 800, 450

    en_cours = True
    while en_cours:
        largeur_ecran, hauteur_ecran = ecran.get_size()

        # Calculer le scale
        scale_x = largeur_ecran / LARGEUR_BASE
        scale_y = hauteur_ecran / HAUTEUR_BASE
        scale = min(scale_x, scale_y)

        # Offset pour centrer
        offset_x = (largeur_ecran - LARGEUR_BASE * scale) // 2
        offset_y = (hauteur_ecran - HAUTEUR_BASE * scale) // 2

        # Fond semi-transparent
        ecran.fill(couleur_fond)

        # Titre GAME OVER
        titre = police_titre.render("GAME OVER", True, couleur_titre)
        rect_titre = titre.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 3))
        ecran.blit(titre, rect_titre)

        # Score final
        texte_score = police_score.render(f"Score: {score_final}", True, couleur_texte)
        rect_score = texte_score.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 2 - 20))
        ecran.blit(texte_score, rect_score)

        # Boutons
        largeur_bouton = 200
        hauteur_bouton = 50
        y_bouton = hauteur_ecran // 2 + 50

        # Bouton Rejouer
        rect_rejouer = pygame.Rect(
            largeur_ecran // 2 - largeur_bouton - 20,
            y_bouton,
            largeur_bouton,
            hauteur_bouton
        )

        # Bouton Menu
        rect_menu = pygame.Rect(
            largeur_ecran // 2 + 20,
            y_bouton,
            largeur_bouton,
            hauteur_bouton
        )

        # Detecter survol souris
        pos_souris = pygame.mouse.get_pos()
        survol_rejouer = rect_rejouer.collidepoint(pos_souris)
        survol_menu = rect_menu.collidepoint(pos_souris)

        # Dessiner bouton Rejouer
        pygame.draw.rect(ecran, couleur_survol if survol_rejouer else couleur_bouton, rect_rejouer)
        pygame.draw.rect(ecran, couleur_texte, rect_rejouer, 2)
        texte_rejouer = police_bouton.render("REJOUER", True, couleur_texte)
        ecran.blit(texte_rejouer, texte_rejouer.get_rect(center=rect_rejouer.center))

        # Dessiner bouton Menu
        pygame.draw.rect(ecran, couleur_survol if survol_menu else couleur_bouton, rect_menu)
        pygame.draw.rect(ecran, couleur_texte, rect_menu, 2)
        texte_menu = police_bouton.render("MENU", True, couleur_texte)
        ecran.blit(texte_menu, texte_menu.get_rect(center=rect_menu.center))

        # Gestion des evenements
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return "quit"

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return "menu"
                if evenement.key == pygame.K_SPACE or evenement.key == pygame.K_RETURN:
                    return "rejouer"

            if evenement.type == pygame.MOUSEBUTTONDOWN:
                if evenement.button == 1:
                    if rect_rejouer.collidepoint(pos_souris):
                        return "rejouer"
                    if rect_menu.collidepoint(pos_souris):
                        return "menu"

        pygame.display.flip()
        horloge.tick(60)

    return "quit"
