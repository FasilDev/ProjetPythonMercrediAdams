import pygame
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"


def afficher_boutique(screen):
    # Charger l'image de la boutique
    fond_boutique = pygame.image.load(ASSETS / "boutique" / "Boutique_Wednesday.webp").convert()

    # Charger les images des items
    img_bougie = pygame.image.load(ASSETS / "boutique" / "Bougie_boutique.webp").convert_alpha()
    img_araignee = pygame.image.load(ASSETS / "boutique" / "Araignee_boutique.webp").convert_alpha()
    img_violon = pygame.image.load(ASSETS / "boutique" / "Violon_boutique.webp").convert_alpha()
    img_grimoire = pygame.image.load(ASSETS / "boutique" / "Grimoire_boutique.webp").convert_alpha()

    # Definition des items avec leurs images
    items = [
        {"nom": "Bougie", "effet": "Ralentit obstacles 10s", "prix": 50, "image": img_bougie},
        {"nom": "Araignee", "effet": "Invincibilite courte", "prix": 100, "image": img_araignee},
        {"nom": "Violon", "effet": "Double le score 15s", "prix": 75, "image": img_violon},
        {"nom": "Grimoire", "effet": "Detruit 1 obstacle", "prix": 150, "image": img_grimoire}
    ]

    item_selectionne = None
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        largeur, hauteur = screen.get_size()

        # Fond qui prend TOUT l'ecran (etire)
        fond_scaled = pygame.transform.scale(fond_boutique, (largeur, hauteur))

        # Polices adaptees a la taille
        font_size = max(18, int(hauteur * 0.04))
        font_prix_size = max(14, int(hauteur * 0.03))
        font = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", font_size)
        font_prix = pygame.font.Font(ASSETS / "fonts" / "Creepster-Regular.ttf", font_prix_size)

        # Taille des items proportionnelle
        item_size = int(hauteur * 0.1)

        # Position du rectangle violet dans l'image (en pourcentage)
        # Le rectangle violet est en bas au centre-droit de la maison
        rect_violet_x = int(largeur * 0.52)  # Centre du rectangle violet
        rect_violet_y = int(hauteur * 0.72)  # Hauteur du rectangle violet

        # Espacement entre les items
        espacement = int(largeur * 0.11)

        # Positions des 4 items dans le rectangle violet (en ligne)
        positions = [
            (rect_violet_x - espacement * 1.5, rect_violet_y),
            (rect_violet_x - espacement * 0.5, rect_violet_y),
            (rect_violet_x + espacement * 0.5, rect_violet_y),
            (rect_violet_x + espacement * 1.5, rect_violet_y)
        ]

        # Calculer les zones cliquables
        boutons_items = []
        for pos in positions:
            x = int(pos[0] - item_size // 2)
            y = int(pos[1] - item_size // 2)
            boutons_items.append(pygame.Rect(x, y, item_size, item_size + 25))

        # Bouton RETOUR
        retour_w = int(largeur * 0.15)
        retour_h = int(hauteur * 0.07)
        bouton_retour = pygame.Rect(
            largeur // 2 - retour_w // 2,
            int(hauteur * 0.88),
            retour_w,
            retour_h
        )

        souris_x, souris_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, bouton in enumerate(boutons_items):
                    if bouton.collidepoint(souris_x, souris_y):
                        item_selectionne = items[i]

                if bouton_retour.collidepoint(souris_x, souris_y):
                    return "menu"

        # Affichage du fond (tout l'ecran)
        screen.blit(fond_scaled, (0, 0))

        # Affichage des items
        for i, (bouton, item) in enumerate(zip(boutons_items, items)):
            # Image de l'item
            if bouton.collidepoint(souris_x, souris_y):
                # Agrandir au survol
                size = int(item_size * 1.15)
                img_scaled = pygame.transform.smoothscale(item["image"], (size, size))
                img_x = bouton.x + (item_size - size) // 2
                img_y = bouton.y + (item_size - size) // 2
            else:
                img_scaled = pygame.transform.smoothscale(item["image"], (item_size, item_size))
                img_x = bouton.x
                img_y = bouton.y

            screen.blit(img_scaled, (img_x, img_y))

            # Prix en dessous
            prix_text = font_prix.render(f"{item['prix']} pts", True, (255, 215, 0))
            prix_x = bouton.x + (item_size - prix_text.get_width()) // 2
            prix_y = bouton.y + item_size + 3
            screen.blit(prix_text, (prix_x, prix_y))

        # Info sur l'item selectionne
        if item_selectionne:
            info_y = int(hauteur * 0.55)
            texte = font.render(f"{item_selectionne['nom']}: {item_selectionne['effet']}", True, (255, 220, 150))
            screen.blit(texte, (largeur // 2 - texte.get_width() // 2, info_y))

        # Bouton RETOUR
        couleur = (120, 80, 140) if bouton_retour.collidepoint(souris_x, souris_y) else (60, 30, 60)
        pygame.draw.rect(screen, couleur, bouton_retour, border_radius=5)
        pygame.draw.rect(screen, (150, 100, 180), bouton_retour, 2, border_radius=5)
        texte_retour = font.render("RETOUR", True, (255, 255, 255))
        screen.blit(texte_retour, (
            bouton_retour.x + (bouton_retour.width - texte_retour.get_width()) // 2,
            bouton_retour.y + (bouton_retour.height - texte_retour.get_height()) // 2
        ))

        pygame.display.flip()
