import pygame
import sys

from game import Game

# Init
pygame.init()

# Window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Couleur
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
DARK_GREY = (100, 100, 100)
LIGHT_GREY = (220, 220, 220)

# Police mains en l'air
font = pygame.font.Font(None, 36)

# GameState
current_control_mode = "Souris"  # "Souris" ou "Clavier"
current_difficulty = "Facile"  # "Facile", "Moyen" ou "Difficile"

def draw_button(screen, font, text, rect, mouse_pos, action=None):
    button_rect = pygame.Rect(rect)

    color = LIGHT_GREY if button_rect.collidepoint(mouse_pos) else GREY
    pygame.draw.rect(screen, color, button_rect)
    
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

    if button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        if action:
            action()

def draw_checkbox(screen, font, label, position, is_checked, mouse_pos):
    box_size = 20
    padding = 5
    text_surf = font.render(label, True, BLACK)
    text_rect = text_surf.get_rect(left=position[0] + box_size + padding * 2, centery=position[1] + box_size // 2)
    box_rect = pygame.Rect(position, (box_size, box_size))

    # Checkbox
    pygame.draw.rect(screen, DARK_GREY, box_rect, 2)
    if is_checked:
        pygame.draw.rect(screen, LIGHT_GREY, box_rect.inflate(-6, -6))

    screen.blit(text_surf, text_rect)

    if box_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        return True
    return False

def main_menu():
    global current_control_mode, current_difficulty
    running = True

    while running:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Button quit
        draw_button(screen, font, "Quitter", (325, 460, 150, 50), mouse_pos, quit_game)

        # Button play
        draw_button(screen, font, "Lancer le jeu", (325, 400, 150, 50), mouse_pos, launch_game)

        if draw_checkbox(screen, font, "Souris", (50, 100), current_control_mode == "Souris", mouse_pos):
            current_control_mode = "Souris"
        if draw_checkbox(screen, font, "Clavier", (250, 100), current_control_mode == "Clavier", mouse_pos):
            current_control_mode = "Clavier"

        # Difficulty
        if draw_checkbox(screen, font, "Facile", (50, 150), current_difficulty == "Facile", mouse_pos):
            current_difficulty = "Facile"
        if draw_checkbox(screen, font, "Moyen", (250, 150), current_difficulty == "Moyen", mouse_pos):
            current_difficulty = "Moyen"
        if draw_checkbox(screen, font, "Difficile", (450, 150), current_difficulty == "Difficile", mouse_pos):
            current_difficulty = "Difficile"

        pygame.display.flip()

def quit_game():
    pygame.quit()
    sys.exit()

def launch_game():

    if current_difficulty == "Facile":
        nbrFood, nbrPiege = 5, 2
    elif current_difficulty == "Moyen":
        nbrFood, nbrPiege = 3, 3
    else:  # "Difficile"
        nbrFood, nbrPiege = 2, 4
    
    game_instance = Game(nbrFood, nbrPiege, current_coSntrol_mode)
    game_instance.run() 


if __name__ == "__main__":
    pygame.init()
    main_menu()
