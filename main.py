import pygame
import random
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
    try:
        hit_sound = pygame.mixer.Sound("assets/Crie.wav")
        hit_sound.set_volume(parametres.volume_effets)
    except:
        hit_sound = None

    level = "easy"
    background = bg_easy

    WIDTH = background.get_width()
    HEIGHT = background.get_height()

    son_touche_m = pygame.mixer.Sound("assets/Mercredi Addams soundplay.wav")
    son_touche_m.set_volume(1.5)

    player = Joueur()
    all_sprites = pygame.sprite.Group(player)

    obstacles = pygame.sprite.Group()

    score = Score(x=10, y=10)
    health_bar = BarreVie(x=10, y=50)

    inventaire = Inventaire()

    pieces_collectees = 0
    police_pieces = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", 24)

    speed = 3.5

    for i in range(2):
        obs = Obstacle(speed, x_offset=i * 350)
        obstacles.add(obs)
        all_sprites.add(obs)

    seuils_obstacles = [800, 1800, 3000, 4500]
    prochain_seuil = 0

    platforms = pygame.sprite.Group()
    for i in range(2):
        plat = Plateforme(speed, niveau=i, x_offset=i * 500)
        platforms.add(plat)
        all_sprites.add(plat)

    coins = pygame.sprite.Group()
    for i in range(5):
        coin = Piece(speed, x=500 + i * 250)
        coins.add(coin)
        all_sprites.add(coin)

    speed_timer = 0
    speed_increase_interval = 240  # Augmentee toutes les 4s

    clock = pygame.time.Clock()

    bg_x = 0
    running = True

    while running:
        clock.tick(FPS)

        screen_width, screen_height = screen.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                donnees_joueur.ajouter_pieces(pieces_collectees)
                return "quit", score.value

            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
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

                effet = inventaire.gerer_touche(event.key)
                if effet == "grimoire":
                    health_bar.soigner(50)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.set_animation("walk")
                elif event.key == pygame.K_SPACE:
                    player.jump_release()

        inventaire.mise_a_jour()

        if inventaire.effet_est_actif("bougie"):
            effective_speed = speed * 0.5
        else:
            effective_speed = speed

        bg_x -= effective_speed
        if bg_x <= -background.get_width():
            bg_x = 0

        player.update(platforms)

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
        health_bar.mise_a_jour()

        if not inventaire.effet_est_actif("araignee"):
            collision_detected = False
            for obs in obstacles:
                if player.hitbox.colliderect(obs.hitbox):
                    if health_bar.subir_degats(20):
                        pass
                    if hit_sound and not collision_detected:
                        hit_sound.set_volume(parametres.volume_effets)
                        hit_sound.play()
                        collision_detected = True
        for coin in coins:
            if not coin.collectee and player.hitbox.colliderect(coin.rect):
                coin.collecter()
                pieces_collectees += 1

        if inventaire.effet_est_actif("violon"):
            score.add(2)
        else:
            score.add(1)

        if prochain_seuil < len(seuils_obstacles) and score.value >= seuils_obstacles[prochain_seuil]:
            new_obs = Obstacle(speed, x_offset=random.randint(200, 400))
            obstacles.add(new_obs)
            all_sprites.add(new_obs)
            prochain_seuil += 1

        if level == "easy" and score.value >= 2000:
            level = "hard"
            background = bg_hard
            bg_x = 0

            speed = max(speed, 6)

            for obs in obstacles:
                obs.speed = max(obs.speed, 6)
            for plat in platforms:
                plat.set_speed(max(plat.speed, 6))
            for coin in coins:
                coin.set_speed(max(coin.speed, 6))

        speed_timer += 1
        if speed_timer >= speed_increase_interval:
            speed_timer = 0
            speed = min(speed + 0.3, 12)

            for obs in obstacles:
                obs.speed = min(obs.speed + 0.3, 14)
            for plat in platforms:
                plat.set_speed(speed)
            for coin in coins:
                coin.set_speed(speed)
        
        if health_bar.est_mort() or player.is_out_of_screen():
            donnees_joueur.ajouter_pieces(pieces_collectees)
            return "dead", score.value

        offset_x = (screen_width - WIDTH) // 2
        offset_y = (screen_height - HEIGHT) // 2

        screen.fill((0, 0, 0))

        screen.blit(background, (bg_x + offset_x, offset_y))
        screen.blit(background, (bg_x + background.get_width() + offset_x, offset_y))

        for sprite in all_sprites:
            
            if sprite == player and inventaire.effet_est_actif("araignee"):
                if inventaire.obtenir_timer_effet("araignee") % 8 < 4:
                    screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))
            else:
                screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

        score.draw(screen, offset_x, offset_y)
        health_bar.dessiner(screen, offset_x, offset_y)

        texte_pieces = police_pieces.render(f"Pieces: {pieces_collectees} (+{donnees_joueur.pieces})", True, (255, 215, 0))
        screen.blit(texte_pieces, (offset_x + WIDTH - texte_pieces.get_width() - 10, offset_y + 10))

        texte_record = police_pieces.render(f"Record: {donnees_joueur.meilleur_score}", True, (200, 170, 200))
        screen.blit(texte_record, (offset_x + WIDTH - texte_record.get_width() - 10, offset_y + 35))
        inventaire.dessiner(screen, offset_x, offset_y)

        pygame.display.flip()

    return "quit", score.value


def main():
    pygame.init()
    pygame.mixer.init()

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
