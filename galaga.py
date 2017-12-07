# -*- coding: utf-8 -*-
"""
Description: Spin-off of the arcade game Galaga. The goal is to not let any
enemy ships past your ship.

@author: Nareg A. Megan

"""

#import pygame and system
import pygame, os
from pygame.locals import *
from random import randint
from timeit import default_timer

print("program started")

#set window position
x = 500
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#setup pygame
pygame.init()

start = default_timer()

window_width = 520
window_height = 672

score = 0

class ScrollingBackground():
    def __init__(self, imagePath):
        self.width = window_width
        self.height = window_height
        self.display = pygame.display.set_mode((self.width,self.height))
        self.bgIm1 = pygame.image.load(imagePath).convert()
        self.bgIm2 = pygame.image.load(imagePath).convert()
        self.yPos1 = 0
        self.yPos2 = -(self.height)

    def update(self):
        if(self.yPos1 == self.height):
            self.yPos1 = -(self.height)
        else:
            self.yPos1 = self.yPos1 + 2

        if(self.yPos2 == self.height):
            self.yPos2 = -(self.height)
        else:
            self.yPos2 = self.yPos2 + 2

    def render(self):
        self.display.blit(self.bgIm1, (0,self.yPos1))
        self.display.blit(self.bgIm2, (0,self.yPos2))


class Ship():
    def __init__(self, imagePath, display):
        self.display = display
        self.shipIm = pygame.image.load(imagePath).convert()
        self.xPos = background.width/2
        self.yPos = 530
        self.key_right = False
        self.key_left = False

    def checkStatus(self):
        #ship movement boolean check
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_RIGHT):
                self.key_right = True
            elif(event.key == pygame.K_LEFT):
                self.key_left = True
        elif(event.type == pygame.KEYUP):
            if(event.key == pygame.K_RIGHT):
                self.key_right = False
            elif(event.key == pygame.K_LEFT):
                self.key_left = False

    def update(self):
        if(self.key_right):
            if(self.xPos == background.width - 60):
                self.xPos = self.xPos
            else:
                self.xPos = self.xPos + 5
        elif(self.key_left):
            if(self.xPos == 0):
                self.xPos = self.xPos
            else:
                self.xPos = self.xPos - 5

    def render(self):
        self.display.blit(self.shipIm, (self.xPos, self.yPos))


class Laser():
    def __init__(self, imagePath, display):
        self.laser = pygame.image.load(imagePath).convert()
        self.yPos = ship.yPos
        self.xPos = ship.xPos + 30
        self.display = display

    def update(self):
        if(self.yPos <= -60):
            return False
        else:
            self.yPos = self.yPos - 12

    def render(self):
        self.display.blit(self.laser, (self.xPos, self.yPos))


class Enemy1():
    def __init__(self, imagePath, display):
        self.display = display
        self.enemyIm = pygame.image.load(imagePath).convert()
        self.xPos = randint(0,background.width-60)
        self.yPos = -30
        self.destroyed = False
        self.safe = False

    def checkStatus(self, laser):
        if(laser.xPos >= self.xPos and laser.xPos <= (self.xPos+60) and laser.yPos <= (self.yPos+30)):
            self.destroyed = True
        if(self.yPos >= background.height+60):
            self.safe = True

    def update(self):
        if not(self.destroyed):
            self.yPos = self.yPos + 5

    def render(self):
        self.display.blit(self.enemyIm, (self.xPos, self.yPos))


class Enemy2():
    def __init__(self, imagePath, display):
        self.display = display
        self.enemyIm = pygame.image.load(imagePath).convert()
        self.xPos = randint(0,background.width)
        self.yPos = -30
        self.destroyed = False
        self.health = 2

    def checkStatus(self, laser):
        if(laser.xPos >= self.xPos and laser.xPos <= (self.xPos+60) and laser.yPos == (self.yPos+30)):
            self.health = self.health - 1
            if(self.health == 0):
                self.destroyed = True

    def update(self):
        if not(self.destroyed):
            self.yPos = self.yPos + 3

    def render(self):
        self.display.blit(self.enemyIm, (self.xPos, self.yPos))


class wave1():
    def __init__(self):
        self.enemies = []
        self.creationCount = 0

    def addEnemy(self, time):
        if(time%4 == 0 and time >= 4):
            self.enemies.append(Enemy1('images\enemy1.png',background.display))

    def update(self, laser):
        if(len(self.enemies) > 0):
            for enemy in self.enemies:
                for lasr in laser:
                    enemy.checkStatus(lasr)
                if(enemy.destroyed == True):
                    self.enemies.remove(enemy)
                elif(enemy.safe == True):
                    self.enemies.remove(enemy)
                    #TODO decrement score
                else:
                    enemy.update()
                    enemy.render()

basicFont = pygame.font.SysFont(None, 48)

#setup game objects
background = ScrollingBackground('images\space.jpg')
ship = Ship('images\ship.png',background.display)

laserArray = []

prevTime = 0

wave1 = wave1()

#clock setup
clock = pygame.time.Clock()
totalTime = 0

score = 0
gameOver = False

#game crashed?
crashed = False
#main game loop (loops for each frame per second)
while not crashed:
    clock.tick(60)
    background.update()
    background.render()
    totalTime = totalTime + clock.get_time()
    currentTime = round(totalTime/1000, 0)

    text = basicFont.render('Hello World!', True, (255, 0, 0), (255, 255, 255))

    #list each event in frame
    for event in pygame.event.get():
        #quit game
        if(event.type == pygame.QUIT):
            crashed = True
        #check ship event status
        ship.checkStatus()
        #check if laser is fired and add it to laser array
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_SPACE):
                laserArray.append(Laser('images\laser.jpg', background.display))

    #update laserArray
    for lasr in laserArray:
        if(lasr.update() == False):
            laserArray.remove(lasr)
        lasr.update()
        lasr.render()

    if(currentTime < 30 and currentTime != prevTime):
        wave1.addEnemy(currentTime)
    if(currentTime < 30):
        wave1.update(laserArray)

    #check if enemy has made it passed player
    for enemy in wave1.enemies:
        print("enemy")
        if(enemy.safe == True):
            print("enemy is safe!")
            gameOver = True
            break
        if(enemy.destroyed == True):
            score = score + 10
    if(gameOver == True):
        break

    #TODO display score

    #update ship according to status
    ship.update()
    #render ship
    ship.render()
    #draw background
    pygame.display.update()
    prevTime = currentTime

#once game is over
if(gameOver == True):
    print(score)
    #TODO display ending screen and score

pygame.quit()
#quit()
