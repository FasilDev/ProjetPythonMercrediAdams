import pygame
import os

def afficher_menu(screen):
    pygame.mixer.music.load("assets/Cimetiere.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Charger les frames du menu (une seule fois)
    frames_originales = [
        pygame.image.load("assets/menu/menu_0.png").convert(),
        pygame.image.load("assets/menu/menu_1.png").convert(),
    ]

    frame_index = 0
    last_anim = 0
    anim_delay = 150  # ms
    
    titre_frames = []

    titre_path = "assets/menu/titre"

    # Charger toutes les frames du titre automatiquement
    for filename in sorted(os.listdir(titre_path)):
        if filename.endswith(".gif") or filename.endswith(".png"):
            img = pygame.image.load(os.path.join(titre_path, filename)).convert_alpha()
            titre_frames.append(img)

    titre_i = 0
    titre_last = 0
    titre_delay = 70  # ms (proche de 0.07s)

    while True:
        # Recalculer la taille à chaque frame (comme dans la boutique)
        largeur, hauteur = screen.get_size()

        # Redimensionner les frames à chaque frame
        frames = [pygame.transform.scale(img, (largeur, hauteur)) for img in frames_originales]

        # Recalculer les positions des boutons
        font = pygame.font.Font("assets/fonts/Creepster-Regular.ttf", 25)

        bouton_jouer = pygame.Rect(
            largeur // 2 - 50,
            hauteur - 230,
            100, 30
        )

        bouton_boutique = pygame.Rect(
            largeur // 2 - 50,
            hauteur - 170,
            100, 30
        )

        bouton_quitter = pygame.Rect(
            largeur // 2 - 50,
            hauteur - 110,
            100, 30
        )

        souris_x, souris_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_jouer.collidepoint(souris_x, souris_y):
                    pygame.mixer.music.stop()
                    return "jouer"
                if bouton_boutique.collidepoint(souris_x, souris_y):
                    pygame.mixer.music.stop()
                    return "boutique"
                if bouton_quitter.collidepoint(souris_x, souris_y):
                    pygame.mixer.music.stop()
                    return "quit"

        # Animation du menu
        now = pygame.time.get_ticks()
        if now - last_anim >= anim_delay:
            last_anim = now
            frame_index = (frame_index + 1) % len(frames)

        # Animation du titre
        if now - titre_last >= titre_delay:
            titre_last = now
            titre_i = (titre_i + 1) % len(titre_frames)

        # Affichage
        screen.blit(frames[frame_index], (0, 0))

        # Affichage du titre en haut à droite (avec marge)
        marge = 20
        titre_img = titre_frames[titre_i]
        screen.blit(titre_img, (largeur - titre_img.get_width() - marge, marge))

        # Boutons
        couleur = (150, 100, 180) if bouton_jouer.collidepoint(souris_x, souris_y) else (80, 40, 100)
        pygame.draw.rect(screen, couleur, bouton_jouer)
        screen.blit(font.render("JOUER", True, (255, 255, 255)),
                    (bouton_jouer.x + 18, bouton_jouer.y + 5))

        couleur = (150, 100, 180) if bouton_boutique.collidepoint(souris_x, souris_y) else (80, 40, 100)
        pygame.draw.rect(screen, couleur, bouton_boutique)
        screen.blit(font.render("BOUTIQUE", True, (255, 255, 255)),
                    (bouton_boutique.x + 8, bouton_boutique.y + 5))

        couleur = (150, 100, 180) if bouton_quitter.collidepoint(souris_x, souris_y) else (80, 40, 100)
        pygame.draw.rect(screen, couleur, bouton_quitter)
        screen.blit(font.render("QUITTER", True, (255, 255, 255)),
                    (bouton_quitter.x + 7, bouton_quitter.y + 5))

        pygame.display.flip()

def afficher_pause(screen, background_capture):
    # Menu pause
    largeur, hauteur = screen.get_size()

    # Overlay semi-transparent
    overlay = pygame.Surface((largeur, hauteur))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))

    font_titre = pygame.font.Font("assets/fonts/Creepster-Regular.ttf", 80)
    font = pygame.font.Font("assets/fonts/Creepster-Regular.ttf", 50)

    # Boutons
    bouton_continuer = pygame.Rect(
        largeur // 2 - 125,
        hauteur // 2 - 40,
        250, 50
    )

    bouton_quitter = pygame.Rect(
        largeur // 2 - 125,
        hauteur // 2 + 40,
        250, 50
    )

    while True:
        souris_x, souris_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "continuer"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_continuer.collidepoint(souris_x, souris_y):
                    return "continuer"
                if bouton_quitter.collidepoint(souris_x, souris_y):
                    return "quit"

        screen.blit(background_capture, (0, 0))
        screen.blit(overlay, (0, 0))

        # Titre "PAUSE"
        texte_pause = font_titre.render("PAUSE", True, (255, 255, 255))
        rect_pause = texte_pause.get_rect(center=(largeur // 2, hauteur // 2 - 120))
        screen.blit(texte_pause, rect_pause)

        # Bouton Continuer
        couleur = (150, 100, 180) if bouton_continuer.collidepoint(souris_x, souris_y) else (80, 40, 100)
        pygame.draw.rect(screen, couleur, bouton_continuer)
        screen.blit(font.render("CONTINUER", True, (255, 255, 255)),
                    (bouton_continuer.x + 15, bouton_continuer.y + 10))

        # Bouton Quitter
        couleur = (150, 100, 180) if bouton_quitter.collidepoint(souris_x, souris_y) else (80, 40, 100)
        pygame.draw.rect(screen, couleur, bouton_quitter)
        screen.blit(font.render("QUITTER", True, (255, 255, 255)),
                    (bouton_quitter.x + 55, bouton_quitter.y + 10))

        pygame.display.flip()