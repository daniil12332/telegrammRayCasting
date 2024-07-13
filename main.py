import math
import time
from math import cos, sin
from PIL import Image, ImageDraw

import pygame

from settings import *

fps = 30
time_delta = 1./fps

img = Image.open(TEXTURE)
img = img.convert("RGB")
d = img.getdata()

imageRGB = []
for i in range(img.size[1]):
    imageRGB.append([])

index = 0
for item in d:
    imageRGB[index].append(item)
    if index == img.size[1]-1:
        index = 0-1
    index += 1

pygame.display.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
surface.fill(WHITE)

rectSizeX = WIDTH // gameWidth
rectSizeY = HEIGHT // gameHeight
playerX = rectSizeX*STARTPLAYERX+rectSizeX//2-rectSizeX
playerY = rectSizeY*STARTPLAYERY+rectSizeY//2-rectSizeY
playerAngle = 0

playerXCoords = STARTPLAYERX
playerYCoords = STARTPLAYERY

SCREENWIDTH = pygame.display.get_window_size()[1]

walls = []
for x in range(gameWidth):
    for y in range(gameHeight):
        if game[y][x] == "w":
            rect1 = (x * rectSizeX, y * rectSizeY, rectSizeX, rectSizeY)
            walls.append(rect1)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerX = int(playerX+PLAYERSPEED*cos(math.radians(playerAngle)))
        playerY = int(playerY+PLAYERSPEED*sin(math.radians(playerAngle)))
    if keys[pygame.K_s]:
        playerX = int(playerX-PLAYERSPEED*cos(math.radians(playerAngle)))
        playerY = int(playerY-PLAYERSPEED*sin(math.radians(playerAngle)))
    if keys[pygame.K_a]:
        playerAngle -= PLAYERANGLESPEED
    if keys[pygame.K_d]:
        playerAngle += PLAYERANGLESPEED
    
    #for i in walls:
    #    pygame.draw.rect(surface, GREEN, i)
    
    playerAngle = math.radians(playerAngle)
    for i in range(SCREENWIDTH//GRAPHUNDETAL):
        lineAngle = playerAngle-FOV/2 + FOV*i/SCREENWIDTH*GRAPHUNDETAL
        for c in range(1000):
            cx = int(playerX+c*cos(lineAngle))
            cy = int(playerY+c*sin(lineAngle))
            for wall in walls:
                if cx > wall[0] and cx < wall[0]+wall[2] and cy > wall[1] and cy < wall[1]+wall[3]:
                    break
            if cx > wall[0] and cx < wall[0] + wall[2] and cy > wall[1] and cy < wall[1] + wall[3]:
                break
        col = int(CWORLD/(c*cos(lineAngle-playerAngle)))
        #pygame.draw.line(surface, BLUE, (i*GRAPHUNDETAL, SCREENWIDTH//2-col), (i*GRAPHUNDETAL, SCREENWIDTH//2+col), GRAPHUNDETAL)
        hitX = (cx-wall[0])/rectSizeX
        hitY = (cy-wall[1])/rectSizeY
        if hitX == 0.01 or hitX == 0.99:
            hit = hitY
        else:
            hit = hitX
        columnRGB = imageRGB[int(hit*img.size[0])]
        for j in range(col*2):
            pix_y = int(j+SCREENWIDTH//2-col)
            #print(pix_y)
            pygame.draw.line(surface, columnRGB[int(img.size[0]*(j/(col*2)))], (i*GRAPHUNDETAL, pix_y), (i*GRAPHUNDETAL, pix_y), GRAPHUNDETAL)
        #pygame.draw.line(surface, RED, (playerX, playerY), (cx, cy))
    playerAngle = math.degrees(playerAngle)
        
        
    #pygame.draw.circle(surface, BLACK, (playerX, playerY), 10)
    
    time.sleep(time_delta)
    pygame.display.flip()
    pygame.draw.rect(surface, WHITE, (0, 0, pygame.display.get_window_size()[0], SCREENWIDTH))
