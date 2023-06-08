import pygame as pg
from pygame.locals import *

pg.init()

white = (250, 250, 250)
black = (0, 0, 0)
resolution = (800, 600)
screen = pg.display.set_mode(resolution)

class dotStar(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  
        self.image = pg.Surface((50, 50), pg.SRCALPHA)
        self.radius = 20
        pg.draw.circle(self.image, white, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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
                x, y = event.pos
                star = dotStar(x, y)
                dotStarGP.add(star)  
    screen.fill(black)
    dotStarGP.draw(screen)
    pg.display.update()

pg.quit()
