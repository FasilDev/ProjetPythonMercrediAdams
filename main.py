import pygame
from pathlib import Path
from personnages import Joueur, Obstacle
from menu import afficher_menu, afficher_pause
from boutique import afficher_boutique
from score import Score
from barre_vie import BarreVie
from plateforme import Plateforme
from piece import Piece
from fin_partie import afficher_fin_partie
from donnees_joueur import donnees_joueur
from inventaire import Inventaire
from parametres import parametres

FPS = 60
ASSETS = Path(__file__).parent / "assets"


def jouer(screen, bg_easy, bg_hard):
    # Son de collision
    try:
        hit_sound = pygame.mixer.Sound("assets/Crie.wav")
        hit_sound.set_volume(parametres.volume_effets)
    except:
        hit_sound = None

    level = "easy"
    background = bg_easy

    # Taille du fond
    WIDTH = background.get_width()
    HEIGHT = background.get_height()

    son_touche_m = pygame.mixer.Sound("assets/Mercredi Addams soundplay.wav")
    son_touche_m.set_volume(1.5)

    # Joueur
    player = Joueur()
    all_sprites = pygame.sprite.Group(player)

    obstacles = pygame.sprite.Group()

    # Score et barre de vie
    score = Score(x=10, y=10)
    health_bar = BarreVie(x=10, y=50)

    # Inventaire
    inventaire = Inventaire()

    # Compteur de pieces collectees cette partie
    pieces_collectees = 0
    police_pieces = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", 24)

    # Vitesse de base
    speed = 2

    for i in range(3):
        obs = Obstacle(speed, x_offset=i * 350)
        obstacles.add(obs)
        all_sprites.add(obs)

    # Plateformes (2 plateformes seulement, bien espacees)
    platforms = pygame.sprite.Group()
    for i in range(2):
        plat = Plateforme(speed, niveau=i, x_offset=i * 500)
        platforms.add(plat)
        all_sprites.add(plat)

    # Pieces (reparties avec reset automatique)
    coins = pygame.sprite.Group()
    for i in range(5):
        coin = Piece(speed, x=500 + i * 250)
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
                donnees_joueur.ajouter_pieces(pieces_collectees)
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
                        donnees_joueur.ajouter_pieces(pieces_collectees)
                        return "menu", score.value

                if event.key == pygame.K_m:
                    son_touche_m.play()

                if event.key == pygame.K_DOWN:
                    player.set_animation("crouch")
                elif event.key == pygame.K_SPACE:
                    player.jump()

                # Utiliser les objets (touches configurables)
                effet = inventaire.gerer_touche(event.key)
                if effet == "grimoire":
                    # Grimoire : restaure 50% de vie
                    health_bar.soigner(50)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.set_animation("walk")
                elif event.key == pygame.K_SPACE:
                    player.jump_release()

        # UPDATE
        inventaire.mise_a_jour()

        # Calculer la vitesse effective (bougie = ralentit de 2x)
        if inventaire.effet_est_actif("bougie"):
            effective_speed = speed * 0.5
        else:
            effective_speed = speed

        bg_x -= effective_speed
        if bg_x <= -background.get_width():
            bg_x = 0

        # Mise a jour du joueur avec les plateformes
        player.update(platforms)

        # Mise a jour des autres sprites avec vitesse effective
        for obs in obstacles:
            old_speed = obs.speed
            obs.speed = old_speed * (0.5 if inventaire.effet_est_actif("bougie") else 1)
            obs.update()
            obs.speed = old_speed
        for plat in platforms:
            old_speed = plat.speed
            plat.speed = old_speed * (0.5 if inventaire.effet_est_actif("bougie") else 1)
            plat.update()
            plat.speed = old_speed
        for coin in coins:
            old_speed = coin.speed
            coin.speed = old_speed * (0.5 if inventaire.effet_est_actif("bougie") else 1)
            coin.update()
            coin.speed = old_speed

        # Mise a jour de la barre de vie
        health_bar.mise_a_jour()

        # Collision avec les obstacles (sauf si invincible avec araignee)
        if not inventaire.effet_est_actif("araignee"):
            collision_detected = False
            for obs in obstacles:
                if player.hitbox.colliderect(obs.hitbox):
                    if health_bar.subir_degats(20):
                        pass
                    # Son de cri (une seule fois par frame)
                    if hit_sound and not collision_detected:
                        hit_sound.play()
                        collision_detected = True

        # Collision avec les pieces
        for coin in coins:
            if not coin.collectee and player.hitbox.colliderect(coin.rect):
                coin.collecter()
                pieces_collectees += 1

        # Augmenter le score avec le temps (double si violon actif)
        if inventaire.effet_est_actif("violon"):
            score.add(2)
        else:
            score.add(1)

        # Passage automatique en difficile a 2000
        if level == "easy" and score.value >= 2000:
            level = "hard"
            background = bg_hard
            bg_x = 0

            speed = 6

            for obs in obstacles:
                obs.speed = 6
            for plat in platforms:
                plat.set_speed(6)
            for coin in coins:
                coin.set_speed(6)

        # Augmenter la vitesse progressivement
        speed_timer += 1
        if speed_timer >= speed_increase_interval:
            speed_timer = 0
            speed = min(speed + 0.4, 10)

            for obs in obstacles:
                obs.speed = min(obs.speed + 0.4, 12)
            for plat in platforms:
                plat.set_speed(speed)
            for coin in coins:
                coin.set_speed(speed)

        # Verifier si le joueur est mort ou sort de l'ecran
        if health_bar.est_mort() or player.is_out_of_screen():
            donnees_joueur.ajouter_pieces(pieces_collectees)
            return "dead", score.value

        # RENDER
        offset_x = (screen_width - WIDTH) // 2
        offset_y = (screen_height - HEIGHT) // 2

        screen.fill((0, 0, 0))

        screen.blit(background, (bg_x + offset_x, offset_y))
        screen.blit(background, (bg_x + background.get_width() + offset_x, offset_y))

        # Afficher les sprites (personnage clignote si invincible)
        for sprite in all_sprites:
            # Clignotement du joueur si invincible (araignee)
            if sprite == player and inventaire.effet_est_actif("araignee"):
                if inventaire.obtenir_timer_effet("araignee") % 8 < 4:
                    screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))
                # Sinon on ne l'affiche pas (effet clignotement)
            else:
                screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

        score.draw(screen, offset_x, offset_y)
        health_bar.dessiner(screen, offset_x, offset_y)

        # Afficher le compteur de pieces (en haut a droite)
        texte_pieces = police_pieces.render(f"Pieces: {pieces_collectees} (+{donnees_joueur.pieces})", True, (255, 215, 0))
        screen.blit(texte_pieces, (offset_x + WIDTH - texte_pieces.get_width() - 10, offset_y + 10))

        # Afficher l'inventaire
        inventaire.dessiner(screen, offset_x, offset_y)

        pygame.display.flip()

    return "quit", score.value


def main():
    pygame.init()
    pygame.mixer.init()

    # Lancement en plein ecran
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Mercredi Addams - Runner")

    # Boucle principale du jeu
    while True:
        choix = afficher_menu(screen)

        if choix == "quit":
            break

        elif choix == "boutique":
            resultat = afficher_boutique(screen)
            if resultat == "quit":
                break
            continue

        elif choix == "jouer":
            pygame.mixer.music.load("assets/Wednesday Addams  Dance.mp3")
            pygame.mixer.music.set_volume(parametres.volume_musique)
            pygame.mixer.music.play(-1)

            bg_easy = pygame.image.load("assets/bgmercredi1.webp").convert()
            bg_hard = pygame.image.load("assets/bgmercredi.jpg").convert()

            while True:
                resultat, score_final = jouer(screen, bg_easy, bg_hard)

                if resultat == "quit":
                    pygame.quit()
                    return

                elif resultat == "dead":
                    pygame.mixer.music.stop()
                    choix_game_over = afficher_fin_partie(screen, score_final)

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
