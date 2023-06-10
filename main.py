import pygame as pg
from pygame.locals import *

import tkinter as tk
from tkinter import simpledialog

pg.init()
pg.font.init()

font = pg.font.Font(None, 20)

white = (250, 250, 250)
black = (0, 0, 0)
resolution = (800, 600)
screen = pg.display.set_mode(resolution)


class dotStar(pg.sprite.Sprite):
    def __init__(self, loc,name):
        super().__init__()  
        self.image = pg.Surface((50, 50), pg.SRCALPHA)
        self.radius = 20
        pg.draw.circle(self.image, white, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (loc)
        self.name = name

    def printNameStar(self, screen):
        text = font.render(self.name, True, white)
        textBox = text.get_rect()
        textBox.centerx = self.rect.centerx  
        textBox.bottom = self.rect.top - 5  
        screen.blit(text, textBox)

dotStarGP = pg.sprite.Group()

def starsDataHistoric():
    try:
        dataHist = open ("dataHist.txt", "r")
    except:
        dataHist = open("dataHist.txt", "w")
        dataHist.close()
        dataHist = open("dataHist.txt", "r")
    data = dataHist.readlines()
    dataHist.close
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
                if line.strip() == dictionaryName:
                    loading = True
                    data[dictionaryName] = {}
                elif line.strip() == "":
                    loading = False
                elif loading:
                    dictionary = eval(line.strip())
                    data[dictionaryName].update(dictionary)
                    loading = False
            return data.get(dictionaryName, {})
    except IOError:
        loadError = "Erro ao carregar o arquivo"
        loadErrorTXT = font.render(loadError, True, white)
        LoadErrorRect = sumText.get_rect()
        LoadErrorRectLoc = (400, 300)
        screen.blit(loadErrorTXT, LoadErrorRectLoc)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
            saveQuit = simpledialog.askstring("Salvar", "Deseja salvar antes de sair? r: s ou n")
            if saveQuit == "s":
                starsDataHistoric()
                createDictionary()
                running = False
            else:
                running = False

        elif event.type == pg.KEYUP and event.key == pg.K_F10:
            starsDataHistoric()
            createDictionary()

        elif event.type == pg.KEYUP and event.key == pg.K_F11:
            dataHist = "dataHist.txt"
            dictionaryName = simpledialog.askstring("Carregar conjunto de estrelas", "Digite o nome do conjunto de estrelas:")
            loadedData = loadDictionary(dataHist, dictionaryName)
            dotStarGP.empty()  
            
            for index, starData in loadedData.items():
                loc = starData["loc"]
                name = starData["name"]
                star = dotStar(loc, name)
                dotStarGP.add(star)                        

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                loc = event.pos
                nameStar = simpledialog.askstring("Nome", "Digite o nome da estrela: ")
                try:
                    if nameStar.strip() == "":
                        nameStar = nameStar
                except tk.TclError:
                    nameStar = nameStar
                star = dotStar(loc, nameStar)
                dotStarGP.add(star)  
    screen.fill(black)
    dotStarGP.draw(screen)

    for star in dotStarGP:
        star.printNameStar(screen)

    summary = "F10 - Salvar // F11 - Carregar Save // F12 - Excluir Save"
    sumText = font.render(summary, True, white)
    sumRect = sumText.get_rect()
    sumRectLoc = (10, 10)
    screen.blit(sumText, sumRectLoc)

    pg.display.update()


pg.quit()