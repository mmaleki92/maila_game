import pygame
import random

pygame.init()
pygame.mixer.init() # add this line
# Red Green Blue
white = (255, 255, 255)
black = (0, 50, 0)
red = (255, 0, 0)
green = (0, 255, 0)
pygame.mixer.music.load('creepy sound.mp3')

dis_x = 1200
dis_y = 700
dis = pygame.display.set_mode((dis_x, dis_y))
pygame.display.set_caption("Maila's Game")

game_over = False

xghost = 300
yghost = 300


xghost_change = 0        
yghost_change = 0

size_x = 100
size_y = 100
xgreen = dis_x / 2
ygreen = dis_y / 2
obstacles = [(50, 100), (700,300), (550, 750), (200,100), (250,600), (300, 100), (450, 100), (850, 700)]

player_image = pygame.image.load('player.png')  # Load the player image
player_image = pygame.transform.scale(player_image, (size_x, size_y))  # Scale the image if needed
black_ghost_image = pygame.image.load('black ghost.png')  # Load the player image
black_ghost_image = pygame.transform.scale(black_ghost_image, (size_x, size_y))  # Scale the image if needed

def fire(dis, xghost, yghost):
    for i in range(10):
        pygame.draw.rect(dis, red, [xghost+random.randint(-50, 90), yghost+random.randint(-50, 90), 8, 8])

def obstacle(dis):
    for obs in obstacles:
        pygame.draw.rect(dis, green, [obs[0], obs[1], 40, 40])

def xwall(x):
    if x>dis_x:
        x = 0
    elif x<0:
        x = dis_x
    return x

clock = pygame.time.Clock()
# pygame.mixer.music.play(2)
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xghost_change = -50
                yghost_change = 0
            elif event.key == pygame.K_RIGHT:
                xghost_change = 50
                yghost_change = 0
            elif event.key == pygame.K_UP:
                yghost_change = -50
                xghost_change = 0
            elif event.key == pygame.K_DOWN:
                yghost_change = 50
                xghost_change = 0

    xghost = xghost + xghost_change
    yghost = yghost + yghost_change

    # if (xghost, yghost) in obstacles:
    #     break
    # if xghost>dis_x:
    #     xghost=0
    #     size_x = size_x + 50
    # elif xghost<0:
    #     size_x=size_x-25
    #     xghost=dis_x
    # if yghost>dis_y:
    #     size_y=size_y+100
    #     yghost=0
    #     yghost = yghost + 5
    # elif yghost<0:
    #     yghost=dis_y
    #     size_y=size_y-5

    dis.fill(black)
    if xghost - xgreen>0:
        xgreen = xgreen + 50
    else:
        xgreen = xgreen - 50
    if yghost - ygreen>0:
        ygreen = ygreen + 50
    else:
        ygreen = ygreen - 50
    
    xghost = xwall(xghost)

    if yghost>dis_y:
        yghost = 0
    elif yghost<0:
        yghost = dis_y

    # pygame.draw.rect(dis, green, [xgreen, ygreen, size_x, size_y])
    dis.blit(player_image, (xghost, yghost))
    dis.blit(black_ghost_image, (xgreen, ygreen))
   # obstacle(dis)

    # if (dis_x - xghost)<40 or (dis_y - yghost)<40 :
    #     fire(dis, xghost, yghost)
        #pygame.mixer.music.play(2)

    pygame.display.update()

    clock.tick(10)

pygame.quit()
quit()