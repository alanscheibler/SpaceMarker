import pygame as pg
from pygame.locals import *

import tkinter as tk
from tkinter import simpledialog

pg.init()

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
        self.name = nameStar

    def printNameStar(self, screen):
        font = pg.font.Font(None, 20)
        text = font.render(self.name, True, white)
        textBox = text.get_rect()
        textBox.centerx = self.rect.centerx  
        textBox.bottom = self.rect.top - 5  
        screen.blit(text, textBox)
dotStarGP = pg.sprite.Group()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
            running = False
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                loc = event.pos
                nameStar = simpledialog.askstring("Nome", "Digite o nome da estrela: ")
                try:
                    if nameStar.strip() == "":
                        nameStar = "Desconhecido"
                except tk.TclError:
                    nameStar = "Desconhecido"
                star = dotStar(loc, nameStar)
                dotStarGP.add(star)  
    screen.fill(black)
    dotStarGP.draw(screen)

    for star in dotStarGP:
        star.printNameStar(screen)

    pg.display.update()

pg.quit()
