import pygame
import sys
import pytmx
import math

def load_and_scale_image(image_path, width, height):
    """
    Charge une image depuis le chemin spécifié et la redimensionne aux dimensions spécifiées.

    Args:
        image_path (str): Chemin de l'image à charger.
        width (int): Largeur désirée de l'image redimensionnée.
        height (int): Hauteur désirée de l'image redimensionnée.

    Returns:
        pygame.Surface: Surface contenant l'image chargée et redimensionnée.
    """
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (width, height))

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = load_and_scale_image("../assets/fireball.png", 20, 20)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += self.direction[0] * 10
        self.rect.y += self.direction[1] * 10

def handle_movement(player_rect, tmx_map, is_dashing, dash_direction):
    """
    Gère le mouvement du joueur.

    Args:
        player_rect (pygame.Rect): Rectangle délimitant la position et la taille du joueur.
        tmx_map (pytmx.TiledMap): Carte TMX chargée.
        is_dashing (bool): Indique si le joueur est en train de dasher.
        dash_direction (tuple): Vecteur de direction du dash.
    """
    keys = pygame.key.get_pressed()
    # Mouvement régulier du joueur
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT] and player_rect.right < tmx_map.width * tmx_map.tilewidth:
        player_rect.x += 5
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= 5
    if keys[pygame.K_DOWN] and player_rect.bottom < tmx_map.height * tmx_map.tileheight:
        player_rect.y += 5

    # Gestion du dash
    if is_dashing:
        player_rect.x += dash_direction[0] * 15
        player_rect.y += dash_direction[1] * 15

        # Assurez-vous que le joueur reste dans les limites de la carte
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > tmx_map.width * tmx_map.tilewidth:
            player_rect.right = tmx_map.width * tmx_map.tilewidth
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > tmx_map.height * tmx_map.tileheight:
            player_rect.bottom = tmx_map.height * tmx_map.tileheight

def run_game():
    pygame.init()
    
    # Constantes pour les couleurs et les dimensions de la barre de santé
    HEALTH_BAR_COLOR = (0, 255, 0)
    DAMAGE_COLOR = (255, 0, 0)
    HEALTH_BAR_WIDTH = 50
    HEALTH_BAR_HEIGHT = 10
    HEALTH_BAR_OFFSET_Y = -20
    
    # Dimensions de la fenêtre
    WIDTH, HEIGHT = 800, 600
    WINDOW_SIZE = (WIDTH, HEIGHT)

    # Initialisation de la fenêtre
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Ma Carte et Mon Personnage")

    # Chargement de la carte TMX et du joueur
    tmx_map = pytmx.load_pygame("../assets/map/volcano.tmx")
    player_size = 50
    player_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, player_size, player_size)
    player_image = load_and_scale_image("../assets/player.png", player_size, player_size)

    # Chargement des images pour le cooldown du dash
    cooldown_ready_image = load_and_scale_image("../assets/sprint_up.png", 45, 45)
    cooldown_used_image = load_and_scale_image("../assets/sprint_down.png", 45, 45)

    # Variables pour le dash et la santé du joueur
    is_dashing = False
    dash_cooldown_counter = 0
    player_health = 50
    dash_direction = (0, 0)

    # Groupe pour les boules de feu
    fireballs = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            keys = pygame.key.get_pressed()

            # Gestion du dash
            if not is_dashing:
                if keys[pygame.K_SPACE] and dash_cooldown_counter == 0:
                    is_dashing = True
                    dash_duration = 10  # Durée du dash en frames (5 secondes à 60 images par seconde)
                    dash_cooldown_counter = 2 * 60  # Temps de recharge du dash (5 secondes à 60 images par seconde)
                    # Calculer la direction du dash en fonction des touches de direction enfoncées
                    dash_direction = (0, 0)
                    if keys[pygame.K_LEFT]:
                        dash_direction = (-1, dash_direction[1])
                    elif keys[pygame.K_RIGHT]:
                        dash_direction = (1, dash_direction[1])
                    if keys[pygame.K_UP]:
                        dash_direction = (dash_direction[0], -1)
                    elif keys[pygame.K_DOWN]:
                        dash_direction = (dash_direction[0], 1)
                    
                    # Normalisez la direction du dash
                    magnitude = math.sqrt(dash_direction[0] ** 2 + dash_direction[1] ** 2)
                    if magnitude != 0:
                        dash_direction = (
                            dash_direction[0] / magnitude,
                            dash_direction[1] / magnitude,
                        )

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                # Obtenir les coordonnées de la souris au moment du clic
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Calculer la direction entre la position actuelle de la boule de feu et les coordonnées de la souris
                direction_x = mouse_x - player_rect.centerx
                direction_y = mouse_y - player_rect.centery
                magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
                if magnitude != 0:
                    direction_x /= magnitude
                    direction_y /= magnitude
                # Création d'une boule de feu dans la direction de la souris
                fireball = Fireball(player_rect.centerx, player_rect.centery, (direction_x, direction_y))
                fireballs.add(fireball)

        if is_dashing:
            dash_duration -= 1
            if dash_duration <= 0:
                is_dashing = False

        if dash_cooldown_counter > 0:
            dash_cooldown_counter -= 1

        # Gestion du mouvement du joueur et du rendu
        handle_movement(player_rect, tmx_map, is_dashing, dash_direction)

        camera_x = min(max(player_rect.x - WIDTH // 2, 0), tmx_map.width * tmx_map.tilewidth - WIDTH)
        camera_y = min(max(player_rect.y - HEIGHT // 2, 0), tmx_map.height * tmx_map.tileheight - HEIGHT)

        screen.fill((0, 0, 0))  # Efface l'écran

        # Rendu de la carte
        for layer in tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_map.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * tmx_map.tilewidth - camera_x, y * tmx_map.tileheight - camera_y))

        # Rendu du joueur
        screen.blit(player_image, (player_rect.x - camera_x, player_rect.y - camera_y))

        # Rendu du cooldown du dash
        cooldown_image = cooldown_used_image if dash_cooldown_counter > 0 else cooldown_ready_image
        screen.blit(cooldown_image, (WIDTH - 60, HEIGHT - 60))

        # Rendu des boules de feu
        fireballs.update()
        fireballs.draw(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
