import pygame
from sprites import Player, Obstacle
from menu import afficher_menu, afficher_pause
from boutique import afficher_boutique

FPS = 60

def main():
    pygame.init()
    pygame.mixer.init()

    # Taille de base du jeu 
    screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
    pygame.display.set_caption("Mercredi Addams - Runner")

    # Boucle pour gérer menu et boutique
    while True:
        choix = afficher_menu(screen)
        
        if choix == "quit":
            pygame.quit()
            return
        
        # Gestion de la boutique
        elif choix == "boutique":
            resultat = afficher_boutique(screen)
            if resultat == "quit":
                pygame.quit()
                return
        
        elif choix == "jouer":
            break 
    
    # Musique du jeu
    pygame.mixer.music.load("assets/Wednesday Addams  Dance.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    # Fond du jeu
    background = pygame.image.load("assets/bgmercredi.jpg").convert()

    # Taille du fond 
    WIDTH = background.get_width()
    HEIGHT = background.get_height()

    # Joueur
    player = Player()
    all_sprites = pygame.sprite.Group(player)
 
    # Obstacles
    obstacles = pygame.sprite.Group()
    speed = 2
    for i in range(3):
        obs = Obstacle(speed + i * 0.5)
        obstacles.add(obs)
        all_sprites.add(obs) 

    clock = pygame.time.Clock()

    bg_x = 0
    running = True

    while running:
        clock.tick(FPS)

        # Récupérer la taille actuelle de la fenêtre
        screen_width, screen_height = screen.get_size()

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Gestion du redimensionnement de fenêtre
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                # F11 pour basculer en plein écran
                if event.key == pygame.K_F11:
                    if screen.get_flags() & pygame.FULLSCREEN:
                        # Sortir du plein écran
                        screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
                    else:
                        # Passer en plein écran
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                
                if event.key == pygame.K_ESCAPE:
                    background_capture = screen.copy()
                    pygame.mixer.music.pause()
                    choix_pause = afficher_pause(screen, background_capture)
                    
                    if choix_pause == "continuer":
                        pygame.mixer.music.unpause()
                    elif choix_pause == "quit":
                        running = False
                        
                if event.key == pygame.K_DOWN:
                    player.set_animation("crouch")
                elif event.key == pygame.K_SPACE:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.set_animation("walk")

        # UPDATE
        bg_x -= speed
        if bg_x <= -background.get_width():
            bg_x = 0

        all_sprites.update()

        # RENDER
        # Calculer les offsets pour centrer le jeu
        offset_x = (screen_width - WIDTH) // 2
        offset_y = (screen_height - HEIGHT) // 2
        
        # Fond noir pour les bandes
        screen.fill((0, 0, 0))
        
        # Dessiner le fond centré
        screen.blit(background, (bg_x + offset_x, offset_y))
        screen.blit(background, (bg_x + background.get_width() + offset_x, offset_y))
        
        # Dessiner les sprites avec le décalage
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()