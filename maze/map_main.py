import pygame
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
GREEN = (0, 255, 0)
DANGEROUS_COLOR = (255, 0, 0)

# Create the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Create Level and Place Dangerous Zones")

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(window, WHITE, (x, 0), (x, HEIGHT), 2)
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(window, WHITE, (0, y), (WIDTH, y), 2)

def save_level(level_data):
    # Load existing levels from the file, if available
    try:
        with open("levels.json", "r") as file:
            existing_levels = json.load(file)
    except FileNotFoundError:
        existing_levels = []

    # Append the new level_data to the existing levels
    existing_levels.append(level_data)

    # Write the updated levels back to the file with indentation
    with open("levels.json", "w") as file:
        json.dump(existing_levels, file, indent=4)

def create_level():
    level_data = {}
    dangerous_zones = []

    # Create the level by allowing the user to place dangerous zones with mouse clicks
    running = True
    while running:

  
        for event in pygame.event.get():
            pygame.draw.rect(window, GREEN, (GRID_COLS * GRID_SIZE - GRID_SIZE, GRID_ROWS * GRID_SIZE - GRID_SIZE, GRID_SIZE, GRID_SIZE))  # Draw the goal
            pygame.display.flip()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // GRID_SIZE, y // GRID_SIZE
                if [grid_x, grid_y] not in dangerous_zones:
                    dangerous_zones.append([grid_x, grid_y])
                else:
                    dangerous_zones.remove([grid_x, grid_y])
                pygame.draw.rect(window, BLACK, (0, 0, WIDTH, HEIGHT))  # Clear the screen
                draw_grid()
                pygame.draw.rect(window, GREEN, (GRID_COLS * GRID_SIZE - GRID_SIZE, GRID_ROWS * GRID_SIZE - GRID_SIZE, GRID_SIZE, GRID_SIZE))  # Draw the goal
                
                for zone in dangerous_zones:
                    pygame.draw.rect(window, DANGEROUS_COLOR, (zone[0] * GRID_SIZE, zone[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)  # Draw red grid
                pygame.display.flip()

    # Set the goal for the level
    goal_x, goal_y = GRID_COLS - 1, GRID_ROWS - 1
    level_data["goal"] = [goal_x, goal_y]

    # Set the dangerous zones for the level
    level_data["is_dangerous"] = True
    level_data["dangerous_zones"] = dangerous_zones

    return level_data

if __name__ == "__main__":
    window.fill(BLACK)
    draw_grid()
    pygame.display.flip()

    print("Create your level by placing dangerous zones with mouse clicks.")
    print("Press Enter to finish creating the level and save it.")

    level_data = create_level()
    save_level(level_data)

    pygame.quit()
