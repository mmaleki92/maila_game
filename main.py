import pygame
import random
pygame.init()

# Red Green Blue
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
dis = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Maila's Game")

game_over = False

x1 = 300
y1 = 300

x1_change = 0        
y1_change = 0

clock = pygame.time.Clock()
x2, y2 = 50, 0 
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -10
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = 10
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -10
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = 10
                x1_change = 0

    x1 = x1 + x1_change
    y1 = y1 + y1_change
    if x1>800 or x1<0 or y1>600 or y1<0:
        break


    dis.fill(white)
    y2 = y2 + 5

    random.randint(0, 800)
    for x2 in range(0, 800, 200):
        pygame.draw.rect(dis, red, [x2, y2, 40, 40])

        if x2-40<x1<x2+40 and y2-40<y1<y2+40 :
            game_over = True
    if y2 > 600:
        y2 = 0
        
    pygame.draw.rect(dis, black, [x1, y1, 40, 40])

    pygame.display.update()

    clock.tick(30)

pygame.quit()
quit()