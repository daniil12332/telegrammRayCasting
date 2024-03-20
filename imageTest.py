from math import sin, cos

from PIL import Image, ImageDraw

from settings import *

IMAGE="game.jpg"

img = Image.open(IMAGE)
img = img.convert("RGB")
d = img.getdata()
new_image = []
for item in d:
    new_image.append((255, 255, 255))
img.putdata(new_image)
img.save(IMAGE)

draw = ImageDraw.Draw(img)
'''
draw.rectangle(xy=(100, 50, 150, 150),
               fill=(0, 0, 255),
               outline=(255, 255, 255),
               width=5)
'''
SCREENWIDTH = img.size[0]
SCREENHEIGHT = img.size[1]

rectSizeX = (SCREENWIDTH) // gameWidth
rectSizeY = (SCREENHEIGHT) // gameHeight
playerX = rectSizeX*STARTPLAYERX+rectSizeX//2-rectSizeX
playerY = rectSizeY*STARTPLAYERY+rectSizeY//2-rectSizeY
playerAngle = 1.3000000000000005

walls = []
for x in range(gameWidth):
    for y in range(gameHeight):
        if game[y][x] == "w":
            rect1 = (x * rectSizeX, y * rectSizeY, rectSizeX, rectSizeY)
            walls.append(rect1)

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
    draw.rectangle(xy=(i * GRAPHUNDETAL, SCREENWIDTH // 2 - col, i * GRAPHUNDETAL, SCREENWIDTH // 2 + col),
                   fill=(0, 0, 0),
                   outline=(0, 0, 255),
                   width=1)

img.save(IMAGE)
img.show()