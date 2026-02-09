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
ProjetPythonMercrediAdams-main/
│
├── 📄 Fichiers Python Principaux
│   ├── main.py                         # Point d'entrée du jeu
│   ├── menu.py                         # Menu principal
│   ├── personnages.py                  # Classes Joueur, Obstacle
│   ├── boutique.py                     # Système de boutique
│   ├── plateforme.py                   # Gestion des plateformes
│   ├── piece.py                        # Gestion des pièces
│   ├── score.py                        # Système de score
│   ├── barre_vie.py                    # Barre de vie
│   ├── fin_partie.py                   # Écran de fin de partie
│   ├── donnees_joueur.py               # Données du joueur
│   ├── inventaire.py                   # Système d'inventaire
│   └── parametres.py                   # Paramètres du jeu
│
├── 📋 Fichiers de Configuration
│   ├── parametres.json                 # Configuration du jeu
│   ├── sauvegarde.json                 # Fichier de sauvegarde
│   └── README.md                       # Documentation
│
├── 🗂️ __pycache__/                     # Cache Python (généré automatiquement)
│   ├── barre_vie.cpython-311.pyc
│   ├── boutique.cpython-311.pyc
│   ├── donnees_joueur.cpython-311.pyc
│   ├── fin_partie.cpython-311.pyc
│   ├── inventaire.cpython-311.pyc
│   ├── menu.cpython-311.pyc
│   ├── parametres.cpython-311.pyc
│   ├── personnages.cpython-311.pyc
│   ├── piece.cpython-311.pyc
│   ├── plateforme.cpython-311.pyc
│   └── score.cpython-311.pyc
│
└── 📁 assets/                          # Ressources du jeu
    │
    ├── 🎨 Backgrounds (Fonds)
    │   ├── bgmercredi.jpg              # Fond principal du jeu
    │   └── bgmercredi1.webp            # Fond alternatif
    │
    ├── 🎭 Sprites Personnage Principal
    │   ├── mercrediadamspritecouche.png    # Sprite couché
    │   └── mercrediadamspritemarche.png    # Sprite en marche
    │
    ├── 👾 Sprites Obstacles
    │   ├── hyde_sprite.png             # Obstacle Hyde
    │   └── spider.webp                 # Araignée obstacle
    │
    ├── 💎 Sprites Pièces/Objets
    │   ├── piquequifaitmal.png         # Pièce/piège (PNG)
    │   ├── piquequifaitmal.webp        # Pièce/piège (WEBP)
    │   └── ravenfly.png                # Corbeau volant
    │
    ├── 🛍️ boutique/                    # Images de la boutique
    │   ├── Araignee_boutique.webp      
    │   ├── Bougie_boutique.webp
    │   ├── Boutique_Wednesday.webp
    │   ├── Grimoire_boutique.webp
    │   └── Violon_boutique.webp
    │
    ├── 🔤 fonts/                       # Polices
    │   └── Creepster-Regular.ttf
    │
    ├── 📱 menu/                        # Images et animations du menu
    │   ├── menu_0.png
    │   ├── menu_1.png
    │   └── titre/                      # Animation titre (91 frames)
    │       ├── frame_00_delay-0.07s.gif
    │       ├── frame_01_delay-0.06s.gif
    │       ├── frame_02_delay-0.07s.gif
    │       ├── ... (frames 03 à 89)
    │       └── frame_90_delay-0.07s.gif
    │
    └── 🎵 Audio (Sons & Musique)
        ├── Cimetiere.mp3                # Musique d'ambiance cimetière
        ├── Crie.wav                     # Son de cri
        ├── Game Over.wav                # Son de fin de partie
        ├── cash.wav                     # Son de collecte de pièces
        ├── Mercredi Addams soundplay.wav # Son de jeu
        └── Wednesday Addams Dance.mp3    # Musique de danse
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
- Musique : Cimetiere.mp3 et Wednesday Addamps Dance.mp3
- Sons : Crie.wav / Game Over.wav / cash.wav / Mercredi Addams soundplay.wav (Easter Egg)
- Inspiration : Série Mercredi

