import pygame
import random

pygame.init()
pygame.mixer.init()  # add this line

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
music = pygame.mixer.music.load('alarm.wav')

dis_x = 1000
dis_y = 600
dis = pygame.display.set_mode((dis_x, dis_y))
pygame.display.set_caption("Maila's Game")

game_over = False

x1 = 300
y1 = 300
x1_change = 0
y1_change = 0

size_x = 40
size_y = 40

obstacles = [(50, 50), (100, 100)]

player_image = pygame.image.load('player.png')  # Load the player image
player_image = pygame.transform.scale(player_image, (size_x, size_y))  # Scale the image if needed

def fire(dis, x1, y1):
    for i in range(10):
        pygame.draw.rect(dis, red, [x1 + random.randint(-50, 90), y1 + random.randint(-50, 90), 8, 8])

def obstacle(dis):
    for obs in obstacles:
        pygame.draw.rect(dis, green, [obs[0], obs[1], 30, 30])


    
clock = pygame.time.Clock()

bullet = False

movement_keys = {
    pygame.K_LEFT: (-10, 0),
    pygame.K_RIGHT: (10, 0),
    pygame.K_UP: (0, -10),
    pygame.K_DOWN: (0, 10)
}

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            # Update the direction when a movement key is pressed
            if event.key in movement_keys:
                x1_change, y1_change = movement_keys[event.key]
        elif event.type == pygame.KEYUP:
            # Stop the movement when a movement key is released
            if event.key in movement_keys:
                x1_change, y1_change = 0, 0

    # Check for collisions with the maze walls and screen boundaries
    if not (x1+x1_change, y1+y1_change) in obstacles:
        x1 += x1_change
        y1 += y1_change


    dis.fill(white)

    # Draw the player image instead of the square
    dis.blit(player_image, (x1, y1))

    obstacle(dis)

    if (dis_x - x1) < 40 or (dis_y - y1) < 40:
        fire(dis, x1, y1)

    pygame.display.update()

    clock.tick(30)

pygame.quit()
quit()
