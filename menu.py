import pygame
    
def afficher_menu(screen):
    largeur, hauteur = screen.get_size()

    pygame.mixer.music.load("assets/Cimetiere.mp3") 
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Charger les frames du menu
    frames = [
        pygame.image.load("assets/menu/menu_0.png").convert(),
        pygame.image.load("assets/menu/menu_1.png").convert(),
    ]

    # Redimensionner chaque frame à la taille de la fenêtre
    frames = [pygame.transform.scale(img, (largeur, hauteur)) for img in frames]

    frame_index = 0
    last_anim = 0
    anim_delay = 150  # ms

    font = pygame.font.Font("assets/fonts/Creepster-Regular.ttf", 50)

    bouton_jouer = pygame.Rect(
        largeur // 2 - 125,
        hauteur // 2 - 120,
        200, 50
    )
    bouton_boutique = pygame.Rect(
        largeur // 2 - 125,
        hauteur // 2 - 40,
        200, 50
    )

    bouton_quitter = pygame.Rect(
        largeur // 2 - 125,
        hauteur // 2 + 40,
        200, 50
    )

    while True:
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

        # 🔹 Animation du menu
        now = pygame.time.get_ticks()
        if now - last_anim >= anim_delay:
            last_anim = now
            frame_index = (frame_index + 1) % len(frames)

        # 🔹 Affichage
        screen.blit(frames[frame_index], (0, 0))

        # Boutons
        couleur = (150, 100, 180) if bouton_jouer.collidepoint(souris_x, souris_y) else (80, 40, 100)
        pygame.draw.rect(screen, couleur, bouton_jouer)
        screen.blit(font.render("JOUER", True, (255, 255, 255)),
                    (bouton_jouer.x + 80, bouton_jouer.y + 20))
        
        couleur = (150, 100, 180) if bouton_boutique.collidepoint(souris_x, souris_y) else (80, 40, 100)
        pygame.draw.rect(screen, couleur, bouton_boutique)
        screen.blit(font.render("BOUTIQUE", True, (255, 255, 255)),
                    (bouton_boutique.x + 15, bouton_boutique.y + 20))

        couleur = (150, 100, 180) if bouton_quitter.collidepoint(souris_x, souris_y) else (80, 40, 100)
        pygame.draw.rect(screen, couleur, bouton_quitter)
        screen.blit(font.render("QUITTER", True, (255, 255, 255)),
                    (bouton_quitter.x + 55, bouton_quitter.y + 20))

        pygame.display.flip()


def afficher_pause(screen):
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