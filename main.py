import pygame as pg
import tkinter as tk
import os
from pygame.locals import *
from tkinter import simpledialog
from tkinter import ttk
from functions import *

pg.init()
pg.font.init()

white = (250, 250, 250)
black = (0, 0, 0)
resolution = (800, 600)
screen = pg.display.set_mode(resolution, pg.RESIZABLE)

background = pg.image.load(os.path.join(bgPath, bgFile[0]))
pg.mixer.music.load(os.path.join(sdPath, sdFile[0]))
pg.mixer.music.play(-1)
iconExec = pg.image.load("shipSDOL.png")
pg.display.set_caption("Space Marker")
pg.display.set_icon(iconExec)

marked = []

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

def configurations():
    global background
    global sound
    
    cfg = tk.Tk()
    cfg.title("Configurações")

    bgLabel = tk.Label(cfg, text="Alterar background:")
    bgLabel.grid(row=0, column=0, padx=10, pady=10)

    bgOptions = ["Background 1", "Background 2", "Background 3", "Background 4", "Escolha do Autor"]
    bgCombobox = ttk.Combobox(cfg, values=bgOptions)
    bgCombobox.grid(row=0, column=1, padx=10, pady=10)

    bgButton = tk.Button(cfg, text="Selecionar", command=lambda: changeBackground(bgCombobox, cfg))
    bgButton.grid(row=0, column=2, padx=10, pady=10)

    musicLabel = tk.Label(cfg, text="Alterar música de fundo:")
    musicLabel.grid(row=1, column=0, padx=10, pady=10)

    musicOptions = ["Sound 1", "Sound 2", "Sound 3", "Sound 4", "Escolha do Autor"]
    musicCombobox = ttk.Combobox(cfg, values=musicOptions)
    musicCombobox.grid(row=1, column=1, padx=10, pady=10)

    musicButton = tk.Button(cfg, text="Selecionar", command=lambda: changeMusic(musicCombobox))
    musicButton.grid(row=1, column=2, padx=10, pady=10)

    cfg.mainloop()

def changeBackground(combobox, cfg):
    global background

    selectedBg = combobox.get()

    if selectedBg == "Background 1":
        background = pg.image.load(os.path.join(bgPath, bgFile[0]))
    elif selectedBg == "Background 2":
        background = pg.image.load(os.path.join(bgPath, bgFile[1]))
    elif selectedBg == "Background 3":
        background = pg.image.load(os.path.join(bgPath, bgFile[2]))
    elif selectedBg == "Background 4":
        background = pg.image.load(os.path.join(bgPath, bgFile[3]))
    elif selectedBg == "Escolha do Autor":
        background = pg.image.load(os.path.join(bgPath, bgFile[4]))
    screen.blit(background, (0, 0))
    pg.display.flip()

def changeMusic(combobox):
    global sound

    selectedSound = combobox.get()
    if selectedSound == "Sound 1":
        sound = os.path.join(sdPath, sdFile[0])
    elif selectedSound == "Sound 2":
        sound = os.path.join(sdPath, sdFile[1])
    elif selectedSound == "Sound 3":
        sound = os.path.join(sdPath, sdFile[2])
    elif selectedSound == "Sound 4":
        sound = os.path.join(sdPath, sdFile[3])
    elif selectedSound == "Escolha do Autor":
        sound = os.path.join(sdPath, sdFile[4])
    
    pg.mixer.music.stop()
    pg.mixer.music.load(sound)
    pg.mixer.music.play(-1)  

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
            saveQuit = simpledialog.askstring("Salvar", "Deseja salvar antes de sair? r: s ou n")
            if saveQuit and saveQuit.lower() == "s":
                createDictionary()
            running = False
        
        elif event.type == pg.VIDEORESIZE:
            resolution = (event.w, event.h)
            screen = pg.display.set_mode(resolution, pg.RESIZABLE)

        elif event.type == pg.KEYUP and event.key == pg.K_F10:
            createDictionary()

        elif event.type == pg.KEYUP and event.key == pg.K_F11:
            dataHist = "dataHist.txt"
            dictionaryName = simpledialog.askstring("Carregar conjunto de estrelas", "Digite o nome do conjunto de estrelas:")
            
            if dictionaryName is None or dictionaryName.strip() == "":
                messagebox.showinfo("Erro ao carregar conjunto", "Nome inválido.")
            else:
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

        elif event.type == pg.KEYDOWN and event.key == pg.K_QUOTE:
            configurations()

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
                    if nameStar is not None:
                        if nameStar.strip() == "":
                            nameStar = "Desconhecido"
                        star = DotStar(loc, nameStar)
                        dotStarGP.add(star)  
                        marked.append(loc)
                except tk.TclError:
                    pass

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