from math import (
    sin,
    cos,
    radians
)

import telebot
from PIL import Image

import render
from settings import *

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

imgMap = Image.open(MAP)
imgMap = imgMap.convert("RGB")
d = imgMap.getdata()
new_image = []
for item in d:
    new_image.append((255, 255, 255))
imgMap.putdata(new_image)
imgMap.save(MAP)

img = Image.open(IMAGE)
img = img.convert("RGB")
d = img.getdata()
new_image = []
for item in d:
    new_image.append((255, 255, 255))
img.putdata(new_image)
img.save(IMAGE)

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
playerAngle = STARTPLAYERANGLE

walls = []
for x in range(gameWidth):
    for y in range(gameHeight):
        if game[y][x] == "w":
            rect1 = (x * rectSizeX, y * rectSizeY, rectSizeX, rectSizeY)
            walls.append(rect1)

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=["show"])
def showGame(message):
    global playerX
    global playerY
    global playerAngle
    bot.send_message(message.chat.id, "hello")
    render.render(img, playerAngle, playerX, playerY, SCREENWIDTH, IMAGE, walls, imageRGB=imageRGB)
    bot.send_photo(message.chat.id, open(IMAGE, 'rb'))
    
@bot.message_handler(commands=["map"])
def map(message):
    global playerAngle
    render.renderMap(imgMap, playerAngle, playerX, playerY, MAP, walls)
    bot.send_photo(message.chat.id, open(MAP, 'rb'))
    
@bot.message_handler(commands=["forward"])
def forward(message):
    global playerX
    global playerY
    global playerAngle
    try:
        render.animationsForward(playerAngle, playerX, playerY, PLAYERANGLESPEED, rectSizeX, rectSizeY, ANIMATION, SCREENWIDTH, walls, imageRGB=imageRGB)
        playerX = int(playerX + rectSizeX * cos(radians(playerAngle)))
        playerY = int(playerY+rectSizeY*sin(radians(playerAngle)))
        bot.send_video(message.chat.id, open(ANIMATION, 'rb'), None)
    except ZeroDivisionError:
        bot.send_message(message.chat.id, "wall")
    render.render(img, playerAngle, playerX, playerY, SCREENWIDTH, IMAGE, walls, imageRGB=imageRGB)
    bot.send_photo(message.chat.id, open(IMAGE, 'rb'))
    
@bot.message_handler(commands=["lookRight"])
def lookRight(message):
    global playerX
    global playerY
    global playerAngle
    render.animationsRotate(playerAngle, playerX, playerY, 90, PLAYERANGLESPEED, ANIMATION, SCREENWIDTH, walls, imageRGB=imageRGB)
    playerAngle += 90
    render.render(img, playerAngle, playerX, playerY, SCREENWIDTH, IMAGE, walls, imageRGB=imageRGB)
    bot.send_video(message.chat.id, open(ANIMATION, 'rb'))
    bot.send_photo(message.chat.id, open(IMAGE, 'rb'))
    
@bot.message_handler(commands=["lookLeft"])
def lookLeft(message):
    global playerX
    global playerY
    global playerAngle
    render.animationsRotate(playerAngle, playerX, playerY, -90, -PLAYERANGLESPEED, ANIMATION, SCREENWIDTH, walls, imageRGB=imageRGB)
    playerAngle -= 90
    render.render(img, playerAngle, playerX, playerY, SCREENWIDTH, IMAGE, walls, imageRGB=imageRGB)
    bot.send_video(message.chat.id, open(ANIMATION, 'rb'))
    bot.send_photo(message.chat.id, open(IMAGE, 'rb'))
    
bot.polling()
