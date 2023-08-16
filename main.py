import pygame
import random

pygame.init()
pygame.mixer.init() # add this line
# Red Green Blue
white = (255, 255, 255)
black = (0, 50, 0)
red = (255, 0, 0)
green = (0, 0, 0)
music = pygame.mixer.music.load('creepy sound.mp3')

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
size_y = 180
xgreen = dis_x / 2
ygreen = dis_y / 2
obstacles = [(50, 100), (700,300), (550, 750), (200,100), (250,600), (300, 100), (450, 100), (850, 700)]
bg = pygame.image.load("minecraft background.jpg")
bg = pygame.transform.scale(bg, (dis_x, dis_y))  # Scale the image if needed

player_image = pygame.image.load('unnamed.png')  # Load the player image
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

def ywall(y):
    if y>dis_y:
        y = 0
    elif y<0:
        y = dis_y
    return y

clock = pygame.time.Clock()
def chase(xgreen, ygreen, xghost, yghost, speed):
    if xghost - xgreen>0:
        xgreen = xgreen + speed
    else:
        xgreen = xgreen - speed
    if yghost - ygreen>0:
        ygreen = ygreen + speed
    else:
        ygreen = ygreen - speed
    return xgreen, ygreen

def movement(event, xghost_change, yghost_change):

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
    return xghost_change, yghost_change

while not game_over:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        xghost_change, yghost_change = movement(event, xghost_change, yghost_change)
        
    xghost = xghost + xghost_change
    yghost = yghost + yghost_change


    dis.fill(black)
    xgreen, ygreen = chase(xgreen, ygreen, xghost, yghost, 10)  
    xghost = xwall(xghost)

    yghost = ywall(yghost)
    dis.blit(bg, (0, 0))
    dis.blit(player_image, (xghost, yghost))
    dis.blit(black_ghost_image, (xgreen, ygreen))

    pygame.display.update()

    clock.tick(10)

pygame.quit()
quit()