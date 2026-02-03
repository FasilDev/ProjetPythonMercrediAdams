import pygame

def afficher_menu(screen):

    background = pygame.image.load("assets/Menu jeu 3.gif").convert()
    font = pygame.font.Font(None, 50)
    

    bouton_jouer = pygame.Rect(250, 250, 300, 70)
    bouton_quitter = pygame.Rect(250, 350, 300, 70)

    couleur_bouton = (80, 40, 100)

    menu_actif = True

    while True:
        souris_x, souris_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_jouer.collidepoint(souris_x, souris_y):
                    return "jouer"
                if bouton_quitter.collidepoint(souris_x, souris_y):
                    return "quit"

        screen.blit(background, (0, 0))


        if bouton_jouer.collidepoint(souris_x, souris_y):
            pygame.draw.rect(screen, (150, 100, 180), bouton_jouer)
        else:
            pygame.draw.rect(screen, (80, 40, 100), bouton_jouer)

        texte_jouer = font.render("JOUER", True, (255, 255, 255))
        screen.blit(texte_jouer, (330, 270))


        if bouton_quitter.collidepoint(souris_x, souris_y):
            pygame.draw.rect(screen, (150, 100, 180), bouton_quitter)
        else:
            pygame.draw.rect(screen, (80, 40, 100), bouton_quitter)

        texte_quitter = font.render("QUITTER", True, (255, 255, 255))
        screen.blit(texte_quitter, (305, 370))

        pygame.display.flip()