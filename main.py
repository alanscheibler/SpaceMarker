import pygame as pg
from pygame.locals import *
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import random

from functions import *

pg.init()
pg.font.init()

white = (250, 250, 250)
black = (0, 0, 0)
resolution = (800, 600)
screen = pg.display.set_mode(resolution, pg.RESIZABLE)
background = pg.image.load("bg1.png")
iconExec = pg.image.load("shipSDOL2.png")
marked = []

pg.display.set_caption("Space Marker")
pg.display.set_icon(iconExec)
pg.mixer.music.load("Space_Machine_Power.mp3")
pg.mixer.music.play(-1)

class DistanceLine(pg.sprite.Sprite):
    def __init__(self, firstPoint, secondPoint):
        super().__init__()
        self.firstPoint = firstPoint
        self.secondPoint = secondPoint
        self.updateLine()

    def updateLine(self):
        self.image = pg.Surface((abs(self.secondPoint[0] - self.firstPoint[0]), abs(self.secondPoint[1] - self.firstPoint[1])), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = min(self.firstPoint[0], self.secondPoint[0]), min(self.firstPoint[1], self.secondPoint[1])
        self.drawnLine()

    def drawnLine(self):
        pg.draw.line(self.image,white,(self.firstPoint[0] - self.rect.x, self.firstPoint[1] - self.rect.y),
            (self.secondPoint[0] - self.rect.x, self.secondPoint[1] - self.rect.y), 2)
            
class DistanceTxt(pg.sprite.Sprite):
    def __init__(self, position, text):
        super().__init__()
        self.image = font.render(text, True, white)
        self.rect = self.image.get_rect(center=position)

def calculateDistace():
        if len(marked) >=2:
            for i in range(len(marked)-1):
                firstPoint = pg.math.Vector2(marked[i])
                secondPoint = pg.math.Vector2(marked[i+1])
                line = DistanceLine(firstPoint, secondPoint)
                distanceLineGP.add(line)

                distance = pg.math.Vector2(secondPoint) - pg.math.Vector2(firstPoint)
                distanceLen = distance.length()
                distanceTxt = DistanceTxt((firstPoint + secondPoint) / 2, "Distancia: {:.2f}".format(distanceLen))
                distanceTextGP.add(distanceTxt)
                
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
            saveQuit = simpledialog.askstring("Salvar", "Deseja salvar antes de sair? r: s ou n")
            if saveQuit == "s" or saveQuit == "S":
                starsDataHistoric()
                createDictionary()
                running = False
            else:
                running = False
        
        elif event.type == pg.VIDEORESIZE:
            resolution = (event.w, event.h)
            screen = pg.display.set_mode(resolution, pg.RESIZABLE)

        elif event.type == pg.KEYUP and event.key == pg.K_F10:
            starsDataHistoric()
            createDictionary()

        elif event.type == pg.KEYUP and event.key == pg.K_F11:
            dataHist = "dataHist.txt"
            dictionaryName = simpledialog.askstring("Carregar conjunto de estrelas", "Digite o nome do conjunto de estrelas:")
            loadedData = loadDictionary(dataHist, dictionaryName)
            dotStarGP.empty()
            distanceLineGP.empty()
            distanceTextGP.empty()
            marked = []  
            
            for index, starData in loadedData.items():
                loc = starData["loc"]
                name = starData["name"]
                star = DotStar(loc, name)
                dotStarGP.add(star)
                marked.append(loc)
                calculateDistace() 

        elif event.type == pg.KEYUP and event.key ==pg.K_F12:
            dotStarGP.empty()
            distanceLineGP.empty()
            distanceTextGP.empty()
            marked = []  

        elif event.type ==pg.KEYDOWN and event.key ==pg.K_z and pg.KMOD_LCTRL:
            if len(marked) >= 1:
                dotStarGP.remove(dotStarGP.sprites()[-1])
                marked.pop()
                distanceLineGP.empty()
                distanceTextGP.empty()
                  
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                try:
                    loc = event.pos
                    nameStar = simpledialog.askstring("Nome", "Digite o nome da estrela: ")
                    try:
                        if nameStar.strip() == "":
                            nameStar = "Desconhecido"
                    except tk.TclError:
                        nameStar = "Desconhecido"
                    star = DotStar(loc, nameStar)
                    dotStarGP.add(star)  
                    marked.append(loc)
                except:
                    nameStar.destroy()

    screen.fill(black)
    screen.blit(background,(0,0))
    dotStarGP.draw(screen)
    distanceLineGP.draw(screen)
    distanceTextGP.draw(screen)

    for star in dotStarGP:
        star.printNameStar(screen)

    calculateDistace()
    summaryTxt()
    pg.display.update()


pg.quit()