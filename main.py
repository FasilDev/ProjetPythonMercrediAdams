import pygame
from sprites import Player, Obstacle
from menu import afficher_menu, afficher_pause
from boutique import afficher_boutique
from score import Score
from health_bar import HealthBar
from platform import Platform
from coin import Coin
from game_over import afficher_game_over

FPS = 60


def jouer(screen, background):
    """Lance une partie et retourne le choix a la fin (rejouer/menu/quit)"""

    # Taille du fond
    WIDTH = background.get_width()
    HEIGHT = background.get_height()

    # Joueur
    player = Player()
    all_sprites = pygame.sprite.Group(player)

    # Score et barre de vie
    score = Score(x=10, y=10)
    health_bar = HealthBar(x=10, y=50)

    # Vitesse de base (plus rapide)
    speed = 4

    # Obstacles (3 obstacles avec tous les types)
    Obstacle.last_type = None
    Obstacle.last_x = 0
    obstacles = pygame.sprite.Group()
    for i in range(3):
        obs = Obstacle(speed, x_offset=i * 350)
        obstacles.add(obs)
        all_sprites.add(obs)

    # Plateformes (2 plateformes seulement, bien espacees)
    platforms = pygame.sprite.Group()
    for i in range(2):
        plat = Platform(speed, level=i, x_offset=i * 500)
        platforms.add(plat)
        all_sprites.add(plat)

    # Pieces (reparties avec reset automatique)
    coins = pygame.sprite.Group()
    for i in range(5):
        coin = Coin(speed, x=500 + i * 250)
        coins.add(coin)
        all_sprites.add(coin)

    # Timer pour augmenter la vitesse
    speed_timer = 0
    speed_increase_interval = 240  # Augmenter toutes les 4 secondes

    clock = pygame.time.Clock()

    bg_x = 0
    running = True

    while running:
        clock.tick(FPS)

        # Recuperer la taille actuelle de la fenetre
        screen_width, screen_height = screen.get_size()

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score.value

            # Gestion du redimensionnement de fenetre
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                # F11 pour basculer en plein ecran
                if event.key == pygame.K_F11:
                    if screen.get_flags() & pygame.FULLSCREEN:
                        screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

                if event.key == pygame.K_ESCAPE:
                    background_capture = screen.copy()
                    pygame.mixer.music.pause()
                    choix_pause = afficher_pause(screen, background_capture)

                    if choix_pause == "continuer":
                        pygame.mixer.music.unpause()
                    elif choix_pause == "quit":
                        return "menu", score.value

                if event.key == pygame.K_DOWN:
                    player.set_animation("crouch")
                elif event.key == pygame.K_SPACE:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.set_animation("walk")
                elif event.key == pygame.K_SPACE:
                    player.jump_release()

        # UPDATE
        bg_x -= speed
        if bg_x <= -background.get_width():
            bg_x = 0

        # Mise a jour du joueur avec les plateformes
        player.update(platforms)

        # Mise a jour des autres sprites
        for obs in obstacles:
            obs.update()
        for plat in platforms:
            plat.update()
        for coin in coins:
            coin.update()

        # Mise a jour de la barre de vie
        health_bar.update()

        # Collision avec les obstacles
        for obs in obstacles:
            if player.hitbox.colliderect(obs.hitbox):
                if health_bar.take_damage(20):
                    pass

        # Collision avec les pieces
        for coin in coins:
            if not coin.collected and player.hitbox.colliderect(coin.rect):
                points = coin.collect()
                score.add(points)

        # Augmenter le score avec le temps
        score.add(1)

        # Augmenter la vitesse progressivement
        speed_timer += 1
        if speed_timer >= speed_increase_interval:
            speed_timer = 0
            speed = min(speed + 0.4, 10)  # Vitesse max de 10

            # Mettre a jour la vitesse de tous les elements
            for obs in obstacles:
                obs.speed = min(obs.speed + 0.4, 12)
            for plat in platforms:
                plat.set_speed(speed)
            for coin in coins:
                coin.set_speed(speed)

        # Verifier si le joueur est mort ou sort de l'ecran
        if health_bar.is_dead() or player.is_out_of_screen():
            return "dead", score.value

        # RENDER
        offset_x = (screen_width - WIDTH) // 2
        offset_y = (screen_height - HEIGHT) // 2

        screen.fill((0, 0, 0))

        screen.blit(background, (bg_x + offset_x, offset_y))
        screen.blit(background, (bg_x + background.get_width() + offset_x, offset_y))

        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

        score.draw(screen, offset_x, offset_y)
        health_bar.draw(screen, offset_x, offset_y)

        pygame.display.flip()

    return "quit", score.value


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
    pygame.display.set_caption("Mercredi Addams - Runner")

    # Boucle principale du jeu
    while True:
        # Menu principal
        choix = afficher_menu(screen)

        if choix == "quit":
            break

        elif choix == "boutique":
            resultat = afficher_boutique(screen)
            if resultat == "quit":
                break
            continue

        elif choix == "jouer":
            # Charger la musique et le fond
            pygame.mixer.music.load("assets/Wednesday Addams  Dance.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

            background = pygame.image.load("assets/bgmercredi.jpg").convert()

            # Boucle de jeu (permet de rejouer)
            while True:
                resultat, score_final = jouer(screen, background)

                if resultat == "quit":
                    pygame.quit()
                    return

                elif resultat == "dead":
                    pygame.mixer.music.stop()
                    choix_game_over = afficher_game_over(screen, score_final)

                    if choix_game_over == "rejouer":
                        pygame.mixer.music.play(-1)
                        continue
                    elif choix_game_over == "menu":
                        break
                    elif choix_game_over == "quit":
                        pygame.quit()
                        return

                elif resultat == "menu":
                    pygame.mixer.music.stop()
                    break

    pygame.quit()


if __name__ == "__main__":
    main()
