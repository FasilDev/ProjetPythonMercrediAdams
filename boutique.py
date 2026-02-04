import pygame

def afficher_boutique(screen):
    largeur, hauteur = screen.get_size()
    
    # Charger l'image de la boutique
    fond_boutique = pygame.image.load("assets/boutique/Boutique_Wednesday.webp").convert()
    fond_boutique = pygame.transform.scale(fond_boutique, (largeur, hauteur))
    
    font = pygame.font.Font("assets/fonts/Creepster-Regular.ttf", 25)
    
    # Définition des 4 objets
    items = [
        {"nom": "🕯️ Bougie", "effet": "Ralentit obstacles 10s"},
        {"nom": "🕷️ Araignee", "effet": "Invincibilite courte"},
        {"nom": "🎻 Violon", "effet": "Double le score 15s"},
        {"nom": "📖 Grimoire", "effet": "Detruit 1 obstacle"}
    ]
    
    # Position des items
    
    boutons_items = [
        pygame.Rect(250, 300, 150, 80),  
        pygame.Rect(600, 300, 150, 80),  
        pygame.Rect(250, 420, 150, 80),   
        pygame.Rect(600, 420, 150, 80)   
    ]
    
    # Bouton RETOUR
    bouton_retour = pygame.Rect(largeur // 2 - 100, hauteur - 80, 200, 50)
    
    item_selectionne = None  # Pour savoir quel item est sélectionné
    
    while True:
        souris_x, souris_y = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                for i, bouton in enumerate(boutons_items):
                    if bouton.collidepoint(souris_x, souris_y):
                        item_selectionne = items[i]
                        print(f"Sélectionné : {item_selectionne['nom']} - {item_selectionne['effet']}")
                
                
                if bouton_retour.collidepoint(souris_x, souris_y):
                    return "menu"
        
        # Affichage du fond
        screen.blit(fond_boutique, (0, 0))
        
        # Affichage des 4 items dans la vitrine
        for i, (bouton, item) in enumerate(zip(boutons_items, items)):
            
            s = pygame.Surface((bouton.width, bouton.height))
            
            # Change de couleur si la souris est dessus
            if bouton.collidepoint(souris_x, souris_y):
                s.set_alpha(100)  
                s.fill((255, 200, 100))  
            else:
                s.set_alpha(50)  
                s.fill((80, 40, 100)) 
            
            screen.blit(s, (bouton.x, bouton.y))
            
            
            pygame.draw.rect(screen, (150, 100, 180), bouton, 2)
            
            
            texte = font.render(item["nom"], True, (255, 255, 255))
            screen.blit(texte, (bouton.x + 10, bouton.y + 25))
        
        
        if item_selectionne:
            texte_selection = font.render(f"Choisi: {item_selectionne['nom']}", True, (255, 200, 100))
            screen.blit(texte_selection, (largeur // 2 - texte_selection.get_width() // 2, 30))
            
            
            font_petit = pygame.font.Font(None, 20)
            texte_effet = font_petit.render(item_selectionne['effet'], True, (200, 200, 200))
            screen.blit(texte_effet, (largeur // 2 - texte_effet.get_width() // 2, 65))
        
        # Bouton RETOUR
        couleur = (150, 100, 180) if bouton_retour.collidepoint(souris_x, souris_y) else (80, 40, 100)
        pygame.draw.rect(screen, couleur, bouton_retour)
        texte_retour = font.render("RETOUR", True, (255, 255, 255))
        screen.blit(texte_retour, (bouton_retour.x + 40, bouton_retour.y + 15))
        
        pygame.display.flip()