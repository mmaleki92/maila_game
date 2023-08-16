import pygame
import sys
import json
import os
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 50
GRID_ROWS = HEIGHT // GRID_SIZE
GRID_COLS = WIDTH // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DANGEROUS_COLOR = (255, 0, 0)  # Red for dangerous places
SQUARE_SIZE = GRID_SIZE
STEP_SIZE = GRID_SIZE
DELAY = 500  # milliseconds (adjust as needed)
GREEN = (0, 255, 0)
# Create the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Square to the Goal")
font = pygame.font.Font(None, 36)  # Font for game over message

class Hero:
    def __init__(self):
        self.grid_x, self.grid_y = 0, 0 # GRID_COLS // 2, GRID_ROWS // 2
        self.moves_list = []  # List to store moves
    def go(self, direction, init=False):
        self.moves_list.append(direction)  # Append the move to the list
        new_x, new_y = self.grid_x, self.grid_y  # New position based on the move

        if direction == 'up':
            new_y = max(0, self.grid_y - 1)
        elif direction == 'down':
            new_y = min(GRID_ROWS - 1, self.grid_y + 1)
        elif direction == 'left':
            new_x = max(0, self.grid_x - 1)
        elif direction == 'right':
            new_x = min(GRID_COLS - 1, self.grid_x + 1)
        # Check if the new position is a dangerous place
        if init and is_dangerous_place(new_x, new_y):
            # 
            return False
            # pygame.quit()
            # sys.exit()

        self.grid_x, self.grid_y = new_x, new_y

    def get_position(self):
        return self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE
    

def is_dangerous_place(x, y):
    # Fetch dangerous_zones from the current level
    dangerous_zones = current_level.get("dangerous_zones", [])
    # print(dangerous_zones)
    return [x, y] in dangerous_zones

def load_levels():
    with open("levels.json", "r") as file:
        levels_data = json.load(file)
    return levels_data
def get_current_level(level_index, levels_data):
    if 0 <= level_index < len(levels_data):
        return levels_data[level_index]
    return None


def game_over():
    # Fill the screen with red
    window.fill(RED)
    game_over_text = font.render("Game Over! You stepped on a dangerous place!", True, BLACK)
    window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()

    # Wait for the user to press "Enter" to continue
    wait_for_enter()

# Function to draw the dashed grid lines
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(window, WHITE, (x, 0), (x, HEIGHT), 2)
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(window, WHITE, (0, y), (WIDTH, y), 2)

def wait_for_enter():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
def reset_game():
    window.fill(BLACK)
    draw_grid()
    pygame.display.flip()

    # Reset hero's position and moves list
    hero.grid_x, hero.grid_y = 0, 0
    hero.moves_list = []


def message(text, color=WHITE):
    # Fill the screen with red
    # window.fill(WHITE)
    game_over_text = font.render(text, True, color)
    window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()

    # Wait for the user to press "Enter" to continue
    # wait_for_enter()


def display_game_before_start(moves_sequence, current_level):
    hero = Hero()
    goal_x, goal_y = current_level["goal"]

    window.fill(BLACK)
    draw_grid()
    pygame.draw.rect(window, GREEN, (goal_x * GRID_SIZE, goal_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw dangerous places on the grid (if any)
    if current_level.get("is_dangerous", False):
        for x in range(GRID_COLS):
            for y in range(GRID_ROWS):
                if is_dangerous_place(x, y):
                    pygame.draw.rect(window, DANGEROUS_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the initial position of the agent (square)
    pygame.draw.rect(window, WHITE, (hero.get_position()[0], hero.get_position()[1], SQUARE_SIZE, SQUARE_SIZE))

    pygame.display.flip()

    
    message("Press Enter to Start!", WHITE)

    wait_for_enter()

    # Play the game for the current level
    move_square(moves_sequence, current_level)
def game_won():
    # Fill the screen with green
    window.fill(GREEN)
    game_won_text = font.render("Congratulations! You reached the goal!", True, BLACK)
    window.blit(game_won_text, (WIDTH // 2 - game_won_text.get_width() // 2, HEIGHT // 2 - game_won_text.get_height() // 2))
    pygame.display.flip()

    # Wait for the user to press "Enter" to continue
    wait_for_enter()
def ask_for_restart_or_quit():
    # Fill the screen with blue
    window.fill((0, 0, 255))
    restart_quit_text = font.render("Press 'R' to restart, 'Q' to quit, or 'L' to choose a different level.", True, WHITE)
    window.blit(restart_quit_text, (WIDTH // 2 - restart_quit_text.get_width() // 2, HEIGHT // 2 - restart_quit_text.get_height() // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_l:
                    return False

def move_square(moves, current_level):
    hero = Hero()
    # Goal position
    goal_x, goal_y = current_level["goal"]

    # Draw the goal position once before the game loop
    window.fill(BLACK)
    draw_grid()
    pygame.draw.rect(window, GREEN, (goal_x * GRID_SIZE, goal_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.display.flip()
    
    # Main game loop
    for move in moves:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Execute the move
        step = hero.go(move, init=True)
        if step == False:
            game_over()
            message("Game Over! You stepped on a dangerous place!", RED)
            step = True
        # Draw everything
        window.fill(BLACK)
        draw_grid()
        pygame.draw.rect(window, WHITE, (hero.get_position()[0], hero.get_position()[1], SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(window, GREEN, (goal_x * GRID_SIZE, goal_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        # Draw dangerous places on the grid (if any)
        if current_level.get("is_dangerous", False):
            for x in range(GRID_COLS):
                for y in range(GRID_ROWS):
                    if is_dangerous_place(x, y):
                        pygame.draw.rect(window, DANGEROUS_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                        
        pygame.display.flip()

        # Add a delay between each move
        pygame.time.delay(DELAY)

        # Check if the square reached the goal
        if hero.get_position() == (goal_x * GRID_SIZE, goal_y * GRID_SIZE):
            game_won()
            message("Winner!", GREEN)
            step = True

    return step
def display_levels(levels_data):
    level_rects = []
    for i, level in enumerate(levels_data):
        x, y = i % GRID_COLS, i // GRID_COLS
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        level_rects.append(rect)
        pygame.draw.rect(window, GREEN, rect)
        # Display level number on the square
        level_number_text = font.render(str(i), True, BLACK)
        window.blit(level_number_text, (x * GRID_SIZE + GRID_SIZE // 2 - level_number_text.get_width() // 2,
                                         y * GRID_SIZE + GRID_SIZE // 2 - level_number_text.get_height() // 2))
    pygame.display.flip()
    return level_rects

def choose_level(levels_data):
    level_rects = display_levels(levels_data)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(level_rects):
                    if rect.collidepoint(event.pos):
                        return i
            elif event.type == pygame.MOUSEMOTION:
                # Change color when hovering over a level square
                for i, rect in enumerate(level_rects):
                    if rect.collidepoint(event.pos):
                        pygame.draw.rect(window, RED, rect)
                        level_number_text = font.render(str(i), True, WHITE)
                        window.blit(level_number_text, (rect.x + GRID_SIZE // 2 - level_number_text.get_width() // 2,
                                                         rect.y + GRID_SIZE // 2 - level_number_text.get_height() // 2))
                    else:
                        pygame.draw.rect(window, GREEN, rect)
                        level_number_text = font.render(str(i), True, BLACK)
                        window.blit(level_number_text, (rect.x + GRID_SIZE // 2 - level_number_text.get_width() // 2,
                                                         rect.y + GRID_SIZE // 2 - level_number_text.get_height() // 2))
        pygame.display.flip()

if __name__ == "__main__":
    with open("levels.json", "r") as file:
        levels_data = json.load(file)

    while True:
        # Get the level index from the user
        level_index = choose_level(levels_data)
        if level_index < 0 or level_index >= len(levels_data):
            print("Invalid level index. Exiting...")
            sys.exit()

        current_level = levels_data[level_index]
        with open("script.py", "r") as file:
            script_content = file.read()

        # Create a hero object
        hero = Hero()

        # Execute the script
        exec(script_content, globals(), locals())

        # Get the moves list from the hero object
        moves_sequence = hero.moves_list

        display_game_before_start(moves_sequence, current_level)
        
        wait_for_enter()
        
        restart = move_square(moves_sequence, current_level)
        print(restart)
        # Display the game and handle the result
        # while True:

        #     for event in pygame.event.get():
        #         if event.type == pygame.K_r:
        #             restart = True
                    
