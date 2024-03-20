import math
import time
from math import cos, sin

import pygame

from settings import *

fps = 5
time_delta = 1./fps

pygame.display.init()
surface = pygame.display.set_mode((600, 600))
surface.fill(WHITE)

rectSizeX = (pygame.display.get_window_size()[0]) // gameWidth
rectSizeY = (pygame.display.get_window_size()[1]) // gameHeight
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
        playerX = int(playerX+rectSizeX*cos(math.radians(playerAngle)))
        playerY = int(playerY+rectSizeY*sin(math.radians(playerAngle)))
    if keys[pygame.K_s]:
        playerX = int(playerX-PLAYERSPEED*cos(math.radians(playerAngle)))
        playerY = int(playerY-PLAYERSPEED*sin(math.radians(playerAngle)))
    if keys[pygame.K_a]:
        playerAngle -= 90
    if keys[pygame.K_d]:
        playerAngle += 90
    
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
        col = CWORLD/(c*cos(lineAngle-playerAngle))
        pygame.draw.line(surface, BLUE, (i*GRAPHUNDETAL, SCREENWIDTH//2-col), (i*GRAPHUNDETAL, SCREENWIDTH//2+col), GRAPHUNDETAL)
        #pygame.draw.line(surface, RED, (playerX, playerY), (cx, cy))
    playerAngle = math.degrees(playerAngle)
        
        
    #pygame.draw.circle(surface, BLACK, (playerX, playerY), 10)
    
    time.sleep(time_delta)
    pygame.display.flip()
    pygame.draw.rect(surface, WHITE, (0, 0, pygame.display.get_window_size()[0], SCREENWIDTH))