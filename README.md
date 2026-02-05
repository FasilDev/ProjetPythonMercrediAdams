# 🎮 Mercredi Addams - Shadow Run

## 📖 Description
Jeu de type runner de Mercredi Addams.
Courir ou mourir : Mercredi n'a pas le temps pour les distractions entre esquives millimétrées et collecte de pièce d'or, guidez-la dans une course sans fin à travers des lieux que même vos pires cauchemars n'oseraient imaginer.

Projet réalisé dans le cadre de la Piscine Python 2026.

## 🎯 Objectifs du jeu
- Esquiver les obstacles (Hyde, corbeaux, etc.)
- Collecter les pièces d'or pour la boutique !
- Battre votre meilleur score pour impressionner la famille Addams
- Débloquer des power-ups dans la boutique

## 🕹️ Comment jouer
- **ESPACE** : Sauter
- **FLÈCHE BAS** : Se baisser
- **ÉCHAP** : Menu pause

## 🚀 Installation et lancement

### Prérequis
- Python 3.9 ou supérieur
- Pygame 2.0 ou supérieur

### Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-repo/ProjetPython_MercrediAdams.git
cd ProjetPython_MercrediAdams
```

2. Installer les dépendances :
```bash
pip install pygame
```

3. Lancer le jeu :
```bash
python main.py
```

## 📂 Structure du projet
```
ProjetPython_MercrediAdams/
├── main.py                    # Point d'entrée du jeu
├── menu.py                    # Menu principal
├── game.py                    # Logique du jeu
├── sprites.py                 # Classes des personnages et objets
├── boutique.py                # Système de boutique
├── platform.py                # Gestion des plateformes
├── coin.py                    # Gestion des pièces
├── score.py                   # Système de score
├── game_over.py               # Écran de fin de partie
├── health_bar.py              # Barre de vie
├── assets/                    # Ressources du jeu
│   ├── boutique/              # Images de la boutique
│   │   ├── Bougie_boutique.webp
│   │   ├── Boutique_Wednesday.webp
│   │   ├── Grimoire_boutique.webp
│   │   └── Violon_boutique.webp
│   ├── fonts/                 # Polices
│   │   └── Creepster-Regular.ttf
│   ├── menu/                  # Images du menu
│   │   ├── menu_0.png
│   │   └── menu_1.png
│   ├── sounds/                # Sons et musique
│   │   └── Cimetiere.mp3
│   ├── bgmercredi.jpg         # Fond de jeu
│   ├── corbeau.webp           # Obstacle
│   ├── hyde.webp              # Obstacle
│   ├── mercrediadam sprite...  # Sprite du personnage
│   ├── spider.webp            # Obstacle
│   └── Wednesday Addams ...   # Sprite du personnage
└── README.md                  # Documentation du projet
```

## 🎨 Fonctionnalités
- ✅ Menu animé avec musique d'ambiance
- ✅ Système de score
- ✅ Difficulté progressive
- ✅ Boutique pour acheter des power-ups
- ✅ Menu pause
- ✅ Écran Game Over avec score final
- ✅ Effets sonores

## 🏪 Boutique
- 🕷️ : 100 pièces pour une invincibilitée courte
- 🕯️ : 50 pièces pour ralentir un obstacle pendant 10s
- 📖 : 150 pièces pour détruire un obstacle
- 🎻 : 75 pièces pour double xp pendant 15s 

## 👥 Équipe
- **[PATIN Lucas]**
- **[ENCINAS Esteban]**
- **[MOUGAMADOU N. Fasil]**
- **[KURZA Gabriela]**

## 🎵 Crédits
- Police : Creepster (Google Fonts)
- Musique : [Source]
- Sons : [Source]
- Inspiration : Série Mercredi

