import pygame as pg
from pygame.locals import *
import tkinter as tk
from tkinter import simpledialog
import os
import random

pg.init()
pg.font.init()

font = pg.font.Font(None, 20)
distanceTxt = ""
dotStarGP = pg.sprite.Group()
distanceLineGP = pg.sprite.Group()
distanceTextGP = pg.sprite.Group()
running = True
marked = []
totalDist = 0
starsFolder = "stars"
starsPath = os.path.join(os.getcwd(), starsFolder)
starsFile = os.listdir(starsPath)


white = (250, 250, 250)
black = (0, 0, 0)
resolution = (800, 600)
screen = pg.display.set_mode(resolution, pg.RESIZABLE)

pg.display.set_caption("Space Marker")
background = pg.image.load("bg1.png")
iconExec = pg.image.load("shipSDOL2.png")
pg.display.set_icon(iconExec)
pg.mixer.music.load("Space_Machine_Power.mp3")
pg.mixer.music.play(-1)

class DotStar(pg.sprite.Sprite):
    def __init__(self, loc, name):
        super().__init__()  
        self.image = pg.image.load(os.path.join(starsPath, random.choice(starsFile)))
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.name = name

    def printNameStar(self, screen):
        text = font.render(self.name, True, white)
        textBox = text.get_rect()
        textBox.centerx = self.rect.centerx  
        textBox.bottom = self.rect.top - 5  
        screen.blit(text, textBox)

def starsDataHistoric():
    try:
        dataHist = open ("dataHist.txt", "r")
    except:
        dataHist = open("dataHist.txt", "w")
        dataHist.close()
        dataHist = open("dataHist.txt", "r")
    data = dataHist.readlines()
    dataHist.close()
    return data

def createDictionary():
    dictionaryName = simpledialog.askstring("Salvar conjunto de estrelas", "Digite o nome do conjunto de estrelas:" )
    starData = {}
    for index, star in enumerate(dotStarGP):
        starData[index] = {
            "loc": star.rect.center,
            "name": star.name
        }
    data = starsDataHistoric()
    data.append(dictionaryName + "\n")
    data.append(str(starData) + "\n")
    dataHist = open("dataHist.txt", "w")
    dataHist.writelines(data)
    dataHist.close()

def loadDictionary(dataHist, dictionaryName):
    try:
        with open(dataHist, "r") as file:
            lines = file.readlines()
            data = {}
            loading = False
            for line in lines:
                if loading:
                    dictionary = eval(line.strip())
                    data[dictionaryName].update(dictionary)
                    loading = False
                elif line.strip() == dictionaryName:
                    loading = True
                    data[dictionaryName] = {}
            return data.get(dictionaryName, {})
    except IOError:
        loadError = "Erro ao carregar o arquivo"
        loadErrorTXT = font.render(loadError, True, white)
        LoadErrorRect = sumText.get_rect()
        LoadErrorRectLoc = (400, 300)
        screen.blit(loadErrorTXT, LoadErrorRectLoc)

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
            if saveQuit == "s" or "S" or "sim" or "Sim":
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

    screen.fill(black)
    screen.blit(background,(0,0))
    dotStarGP.draw(screen)
    distanceLineGP.draw(screen)
    distanceTextGP.draw(screen)

    calculateDistace()
    

    for star in dotStarGP:
        star.printNameStar(screen)

    summary = "F10 - Salvar // F11 - Carregar Save // F12 - Limpar tela // LCTRL + Z - Apaga o último ponto"
    sumText = font.render(summary, True, white)
    sumRect = sumText.get_rect()
    sumRectLoc = (10, 10)
    screen.blit(sumText, sumRectLoc)

    pg.display.update()


pg.quit()