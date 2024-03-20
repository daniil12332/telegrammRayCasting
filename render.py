from math import (
    cos,
    sin,
    radians,
    degrees
)

from PIL import Image, ImageDraw

from settings import *


def renderMap(img, playerAngle, playerX, playerY, MAP, walls):
    draw = ImageDraw.Draw(img)
    draw.rectangle(xy=(0, 0, img.size[0], img.size[1]),
                   fill=WHITE,
                   outline=WHITE,
                   width=1)
    for i in walls:
        draw.rectangle(xy=(i[0], i[1], i[0] + i[2], i[1] + i[3]),
                       fill=BLACK,
                       outline=BLUE,
                       width=1)
    for c in range(45):
        cx1 = int(playerX + c * cos(radians(playerAngle - 30)))
        cy1 = int(playerY + c * sin(radians(playerAngle - 30)))
    for c in range(45):
        cx2 = int(playerX + c * cos(radians(playerAngle + 30)))
        cy2 = int(playerY + c * sin(radians(playerAngle + 30)))
    draw.line(xy=(playerX, playerY, cx1, cy1),
              fill=DARKGREEN, width=1)
    draw.line(xy=(playerX, playerY, cx2, cy2),
              fill=DARKGREEN, width=1)
    draw.ellipse(xy=(playerX - 10, playerY - 10, playerX + 10, playerY + 10),
                 fill=DARKGREEN,
                 outline=WHITE)
    
    img.save(MAP)


def render(img, playerAngle, playerX, playerY, SCREENWIDTH, IMAGE, walls):
    draw = ImageDraw.Draw(img)
    draw.rectangle(xy=(0, 0, img.size[0], img.size[1]),
                   fill=WHITE,
                   outline=WHITE,
                   width=1)
    playerAngle = radians(playerAngle)
    for i in range(SCREENWIDTH // GRAPHUNDETAL):
        lineAngle = playerAngle - FOV / 2 + FOV * i / SCREENWIDTH * GRAPHUNDETAL
        for c in range(1000):
            cx = int(playerX + c * cos(lineAngle))
            cy = int(playerY + c * sin(lineAngle))
            for wall in walls:
                if cx > wall[0] and cx < wall[0] + wall[2] and cy > wall[1] and cy < wall[1] + wall[3]:
                    break
            if cx > wall[0] and cx < wall[0] + wall[2] and cy > wall[1] and cy < wall[1] + wall[3]:
                break
        col = CWORLD / (c * cos(lineAngle - playerAngle))
        for h in range(GRAPHUNDETAL):
            draw.rectangle(xy=(i*GRAPHUNDETAL+h, SCREENWIDTH // 2 - col, i*GRAPHUNDETAL+h, SCREENWIDTH // 2 + col),
                           fill=BLACK,
                           outline=BLUE,
                           width=1)
    playerAngle = degrees(playerAngle)
    img.save(IMAGE)


def animationsForward(playerAngle, startplayerX, startplayerY, speed, rectSizeX, rectSizeY, FILE, SCREENWIDTH, walls):
    animation = []
    playerX = startplayerX
    playerY = startplayerY
    if playerAngle % 180 == 0:
        rectSize = rectSizeX
    else:
        rectSize = rectSizeY
    for i in range(0, rectSize, speed):
        playerX = int(playerX + speed * cos(radians(playerAngle)))
        playerY = int(playerY + speed * sin(radians(playerAngle)))
        animImg = Image.open(FILE)
        animImg = animImg.convert("RGB")
        render(animImg, playerAngle, playerX, playerY, SCREENWIDTH, FILE, walls)
        animation.append(animImg)
    for i in range(0, rectSize, speed * 2):
        playerX = int(playerX - speed * 2 * cos(radians(playerAngle)))
        playerY = int(playerY - speed * 2 * sin(radians(playerAngle)))
        animImg = Image.open(FILE)
        animImg = animImg.convert("RGB")
        render(animImg, playerAngle, playerX, playerY, SCREENWIDTH, FILE, walls)
        animation.append(animImg)
    
    animation[0].save(
        FILE, save_all=True, append_images=animation[1:], duration=100
    )


def animationsRotate(playerAngle, playerX, playerY, rotateAngle, rotateSpeed, FILE, SCREENWIDTH, walls):
    animation = []
    for i in range(0, rotateAngle, rotateSpeed):
        playerAngle += rotateSpeed
        animImg = Image.open(FILE)
        animImg = animImg.convert("RGB")
        render(animImg, playerAngle, playerX, playerY, SCREENWIDTH, FILE, walls)
        animation.append(animImg)
    for i in range(0, rotateAngle, rotateSpeed * 3):
        playerAngle -= rotateSpeed * 3
        animImg = Image.open(FILE)
        animImg = animImg.convert("RGB")
        render(animImg, playerAngle, playerX, playerY, SCREENWIDTH, FILE, walls)
        animation.append(animImg)
    
    animation[0].save(
        FILE, save_all=True, append_images=animation[1:], duration=100
    )