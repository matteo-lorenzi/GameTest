import pygame
import sys
import pygame_gui
from main import run_game  # Importez la fonction run_game depuis main.py

# Initialisation de Pygame
pygame.init()

# Définition des constantes
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
BLACK = (0, 0, 0)

# Création de la fenêtre de menu
menu_screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Menu")

# Création d'un gestionnaire d'événements GUI pour le menu
menu_gui_manager = pygame_gui.UIManager(WINDOW_SIZE)

# Création des boutons du menu
button_play = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 200), (200, 50)), text="Jouer", manager=menu_gui_manager)
button_settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 300), (200, 50)), text="Paramètres", manager=menu_gui_manager)
button_exit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 400), (200, 50)), text="Quitter", manager=menu_gui_manager)

# Boucle de jeu pour le menu
menu_running = True
while menu_running:
    time_delta = pygame.time.Clock().tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_play:
                    print("Lancement du jeu...")
                    run_game()  # Lancer le jeu en appelant la fonction run_game de main.py
                    menu_running = False  # Arrêter la boucle de menu

                elif event.ui_element == button_settings:
                    print("Paramètres")
                    # Ici, vous pouvez insérer le code pour les paramètres

                elif event.ui_element == button_exit:
                    print("Fermeture du jeu...")
                    pygame.quit()
                    sys.exit()

        menu_gui_manager.process_events(event)

    menu_gui_manager.update(time_delta)

    menu_screen.fill(BLACK)
    menu_gui_manager.draw_ui(menu_screen)
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
