import pygame
import sys
import json

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
    def go(self, direction):
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
        if current_level.get("is_dangerous", False) and is_dangerous_place(new_x, new_y):
            game_over()
            pygame.quit()
            sys.exit()

        self.grid_x, self.grid_y = new_x, new_y

    def get_position(self):
        return self.grid_x * GRID_SIZE, self.grid_y * GRID_SIZE
    

def is_dangerous_place(x, y):
    # Fetch dangerous_zones from the current level
    dangerous_zones = current_level.get("dangerous_zones", [])
    return [x, y] in dangerous_zones

def load_levels():
    with open("levels.txt", "r") as file:
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

def display_game_before_start(moves_sequence, current_level):
    hero = Hero()
    goal_x, goal_y = current_level["goal"]

    window.fill(BLACK)
    draw_grid()

    # Draw dangerous places on the grid (if any) and move them
    if current_level.get("is_dangerous", False):
        move_dangerous_zones(current_level)

    # Draw the initial position of the agent (square)
    pygame.draw.rect(window, WHITE, (hero.get_position()[0], hero.get_position()[1], SQUARE_SIZE, SQUARE_SIZE))

    # Draw the goal position
    pygame.draw.rect(window, GREEN, (goal_x * GRID_SIZE, goal_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()

    # Show the initial state to the user
    print("Press Enter to start the game.")
    wait_for_enter()

    # Clear the goal position after pressing Enter
    window.fill(BLACK)
    draw_grid()
    pygame.draw.rect(window, WHITE, (hero.get_position()[0], hero.get_position()[1], SQUARE_SIZE, SQUARE_SIZE))
    pygame.display.flip()

    # Play the game for the current level
    move_square(moves_sequence, current_level)


def move_dangerous_zones(current_level):
    # Simulate the movement of dangerous zones
    dangerous_zones = current_level.get("dangerous_zones", [])
    for zone in dangerous_zones:
        x, y = zone["position"]
        moves = zone.get("moves", [])
        for move in moves:
            if move == 'up':
                y = max(0, y - 1)
            elif move == 'down':
                y = min(GRID_ROWS - 1, y + 1)
            elif move == 'left':
                x = max(0, x - 1)
            elif move == 'right':
                x = min(GRID_COLS - 1, x + 1)
            zone["position"] = (x, y)
            # Draw dangerous zones on the grid
            window.fill(BLACK)
            draw_grid()
            for zone in dangerous_zones:
                x, y = zone["position"]
                pygame.draw.rect(window, DANGEROUS_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.display.flip()
            pygame.time.delay(DELAY)

def move_position(position, direction):
    x, y = position
    if direction == 'up':
        y = max(0, y - 1)
    elif direction == 'down':
        y = min(GRID_ROWS - 1, y + 1)
    elif direction == 'left':
        x = max(0, x - 1)
    elif direction == 'right':
        x = min(GRID_COLS - 1, x + 1)
    return [x, y]


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

        # Move the dangerous zones
        move_dangerous_zones(current_level)

        # Execute the move
        hero.go(move)

        # Draw everything
        window.fill(BLACK)
        draw_grid()
        pygame.draw.rect(window, WHITE, (hero.get_position()[0], hero.get_position()[1], SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(window, GREEN, (goal_x * GRID_SIZE, goal_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        # Draw dangerous places on the grid (if any)
        if current_level.get("is_dangerous", False):
            for zone in current_level["dangerous_zones"]:
                x, y = zone["position"]
                pygame.draw.rect(window, DANGEROUS_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.display.flip()

        # Add a delay between each move
        pygame.time.delay(DELAY)

        # Check if the square reached the goal
        if hero.get_position() == (goal_x * GRID_SIZE, goal_y * GRID_SIZE):
            print("Congratulations! You reached the goal!")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    with open("levels.txt", "r") as file:
        levels_data = json.load(file)

    # Get the level index from the user
    print("Choose a level (0 - {}):".format(len(levels_data) - 1))
    level_index = int(input())
    if level_index < 0 or level_index >= len(levels_data):
        print("Invalid level index. Exiting...")
        sys.exit()

    current_level = levels_data[level_index]
    with open("script.txt", "r") as file:
        script_content = file.read()

    # Create a hero object
    hero = Hero()

    # Execute the script
    exec(script_content, globals(), locals())

    # Get the moves list from the hero object
    moves_sequence = hero.moves_list

    # Display the game to the user before starting
    display_game_before_start(moves_sequence, current_level)
