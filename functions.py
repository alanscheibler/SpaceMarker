import pygame as pg
from pygame.locals import *
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import os
import random


pg.init()
pg.font.init()

font = pg.font.Font(None, 20)
dotStarGP = pg.sprite.Group()
distanceLineGP = pg.sprite.Group()
distanceTextGP = pg.sprite.Group()
starsFolder = "stars"
starsPath = os.path.join(os.getcwd(), starsFolder)
starsFile = os.listdir(starsPath)

bgFolder = "background"
bgPath = os.path.join(os.getcwd(),bgFolder)
bgFile = os.listdir(bgPath)

sdFolder = "sound"
sdPath = os.path.join(os.getcwd(), sdFolder)
sdFile = os.listdir(sdPath)

running = True
distanceTxt = ""
marked = []
totalDist = 0

white = (250, 250, 250)
black = (0, 0, 0)
resolution = (800, 600)
screen = pg.display.set_mode(resolution, pg.RESIZABLE)

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
        messagebox.showinfo("Erro ao carregar conjunto")

def summaryTxt():
    summary = "F10 - Salvar"
    summary1 = "F11 - Carregar Save"
    summary2 = "F12 - Limpar tela"
    summary3 = "LCTRL + Z - Apaga o último ponto"
    summary4 = " ' - Configurações"
    sumText = font.render(summary, True, white)
    sumText1 = font.render(summary1, True, white)
    sumText2 = font.render(summary2, True, white)
    sumText3 = font.render(summary3, True, white)
    sumText4 = font.render(summary4, True, white)
    sumRect = sumText.get_rect()
    sumRect1 = sumText1.get_rect()
    sumRect2 = sumText2.get_rect()
    sumRect3 = sumText3.get_rect()
    sumRect4 = sumText4.get_rect()
    sumRectLoc = (10, 10)
    sumRectLoc1 = (10, 25)
    sumRectLoc2 = (10, 40)
    sumRectLoc3 = (10, 55)
    sumRectLoc4 = (10, 70)
    screen.blit(sumText, sumRectLoc)
    screen.blit(sumText1, sumRectLoc1)
    screen.blit(sumText2, sumRectLoc2)
    screen.blit(sumText3, sumRectLoc3)
    screen.blit(sumText4, sumRectLoc4)

