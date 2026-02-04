import pygame
from sprites import Player, Obstacle
from menu import afficher_menu, afficher_pause
from boutique import afficher_boutique

FPS = 60

def main():
    pygame.init()
    pygame.mixer.init()

    # Taille de base du jeu
    screen = pygame.display.set_mode((800, 450))
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

    # Adapter la fenêtre à la taille du fond
    WIDTH = background.get_width()
    HEIGHT = background.get_height()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Joueur
    player = Player()
    all_sprites = pygame.sprite.Group(player)
 
    # Obstacles
    obstacles = pygame.sprite.Group()
    speed = 2  # Utilise la même vitesse que le défilement
    for i in range(3):  # 3 obstacles
        obs = Obstacle(speed + i * 0.5)
        obstacles.add(obs)
        all_sprites.add(obs) 

    clock = pygame.time.Clock()

    bg_x = 0
    speed = 2
    running = True

    while running:
        clock.tick(FPS)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
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
                elif event.key == pygame.K_SPACE:  # Saut avec ESPACE
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
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + background.get_width(), 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()