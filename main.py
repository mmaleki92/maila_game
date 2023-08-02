import pygame
import random

pygame.init()
pygame.mixer.init() # add this line
# Red Green Blue
white = (255, 255, 255)
black = (0, 0, 0)
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

size_x = 100
size_y = 100

obstacles = [(50, 100), (200,300), (300, 600), (200,100), (250,100), (300, 100), (400, 100), (500, 100)]

player_image = pygame.image.load('player.png')  # Load the player image
player_image = pygame.transform.scale(player_image, (size_x, size_y))  # Scale the image if needed


def fire(dis, x1, y1):
    for i in range(10):
        pygame.draw.rect(dis, red, [x1+random.randint(-50, 90), y1+random.randint(-50, 90), 8, 8])

def obstacle(dis):
    for obs in obstacles:
        pygame.draw.rect(dis, green, [obs[0], obs[1], 40, 40])

clock = pygame.time.Clock()
x2, y2 = 50, 0
bullet = False

while not game_over:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -50
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = 50
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -50
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = 50
                x1_change = 0

    x1 = x1 + x1_change
    y1 = y1 + y1_change

    if (x1, y1) in obstacles:
        break
    # if x1>dis_x:
    #     x1=0
    #     size_x = size_x + 50
    # elif x1<0:
    #     size_x=size_x-25
    #     x1=dis_x
    # if y1>dis_y:
    #     size_y=size_y+100
    #     y1=0
    #     y1 = y1 + 5
    # elif y1<0:
    #     y1=dis_y
    #     size_y=size_y-5
        
    dis.fill(white)
      
 #   pygame.draw.rect(dis, black, [x1, y1, size_x, size_y])
    dis.blit(player_image, (x1, y1))

    obstacle(dis)

    if (dis_x - x1)<40 or (dis_y - y1)<40 :
        fire(dis, x1, y1)
        #pygame.mixer.music.play(2)

    pygame.display.update()

    clock.tick(2)

pygame.quit()
quit()