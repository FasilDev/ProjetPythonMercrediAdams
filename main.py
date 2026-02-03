import pygame
from sprites import Player
from menu import afficher_menu

FPS = 60

def main():
    pygame.init()

    # Création de la fenetre
    screen = pygame.display.set_mode((800, 450))

    # Chargement du fond
    background = pygame.image.load("assets/bgmercredi.jpg").convert()

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # On adapte la fenêtre à la taille du fond
    WIDTH = background.get_width()
    HEIGHT = background.get_height()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    choix = afficher_menu(screen)
    if choix == "quit":
        pygame.quit()
        return

    bg_x = 0
    speed = 2
    running = True


    while running:
        clock.tick(FPS)

        # UPDATE
        bg_x -= speed
        if bg_x <= -background.get_width():
            bg_x = 0
        all_sprites.update()

        # EVENEMENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Exemple : changer d'animation avec les touches
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Flèche bas = baissé
                    player.set_animation('crouch')
                elif event.key == pygame.K_SPACE:  # Espace = perdu
                    player.set_animation('dead')
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:  # Relâche flèche bas = marche
                    player.set_animation('walk')

        # RENDER 
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + background.get_width(), 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
