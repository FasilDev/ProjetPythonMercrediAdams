import pygame
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"
FONT_PATH = ASSETS / "fonts" / "Creepster-Regular.ttf"


def afficher_game_over(screen, score_final):
    """Affiche l'ecran Game Over et retourne le choix du joueur"""
    # Charger le son Game Over
    try:
        game_over_sound = pygame.mixer.Sound("assets/Game Over.wav")
        game_over_sound.set_volume(0.7)
        game_over_sound.play()
    except:
        game_over_sound = None
        print("Impossible de charger Game Over.wav")
        
    clock = pygame.time.Clock()

    # Polices
    font_title = pygame.font.Font(FONT_PATH, 72)
    font_score = pygame.font.Font(FONT_PATH, 36)
    font_button = pygame.font.Font(FONT_PATH, 32)

    # Couleurs
    bg_color = (20, 10, 20)
    title_color = (180, 0, 0)
    text_color = (255, 255, 255)
    button_color = (60, 40, 60)
    button_hover = (100, 70, 100)

    # Taille de base
    BASE_WIDTH, BASE_HEIGHT = 800, 450

    running = True
    while running:
        screen_width, screen_height = screen.get_size()

        # Calculer le scale
        scale_x = screen_width / BASE_WIDTH
        scale_y = screen_height / BASE_HEIGHT
        scale = min(scale_x, scale_y)

        # Offset pour centrer
        offset_x = (screen_width - BASE_WIDTH * scale) // 2
        offset_y = (screen_height - BASE_HEIGHT * scale) // 2

        # Fond semi-transparent
        screen.fill(bg_color)

        # Titre GAME OVER
        title = font_title.render("GAME OVER", True, title_color)
        title_rect = title.get_rect(center=(screen_width // 2, screen_height // 3))
        screen.blit(title, title_rect)

        # Score final
        score_text = font_score.render(f"Score: {score_final}", True, text_color)
        score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 20))
        screen.blit(score_text, score_rect)

        # Boutons
        button_width = 200
        button_height = 50
        button_y = screen_height // 2 + 50

        # Bouton Rejouer
        rejouer_rect = pygame.Rect(
            screen_width // 2 - button_width - 20,
            button_y,
            button_width,
            button_height
        )

        # Bouton Menu
        menu_rect = pygame.Rect(
            screen_width // 2 + 20,
            button_y,
            button_width,
            button_height
        )

        # Detecter survol souris
        mouse_pos = pygame.mouse.get_pos()
        rejouer_hover = rejouer_rect.collidepoint(mouse_pos)
        menu_hover = menu_rect.collidepoint(mouse_pos)

        # Dessiner bouton Rejouer
        pygame.draw.rect(screen, button_hover if rejouer_hover else button_color, rejouer_rect)
        pygame.draw.rect(screen, text_color, rejouer_rect, 2)
        rejouer_text = font_button.render("REJOUER", True, text_color)
        screen.blit(rejouer_text, rejouer_text.get_rect(center=rejouer_rect.center))

        # Dessiner bouton Menu
        pygame.draw.rect(screen, button_hover if menu_hover else button_color, menu_rect)
        pygame.draw.rect(screen, text_color, menu_rect, 2)
        menu_text = font_button.render("MENU", True, text_color)
        screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))

        # Gestion des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return "rejouer"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rejouer_rect.collidepoint(mouse_pos):
                        return "rejouer"
                    if menu_rect.collidepoint(mouse_pos):
                        return "menu"

        pygame.display.flip()
        clock.tick(60)

    return "quit"
