import pygame as pg


class Resource:
    def __init__(self, x=0, y=0):
        self.surface = pg.image.load(".\\Art\\red.png")
        self.rect = self.surface.get_rect(x=x,y=y)
        self.stage = 0   # 0 = Top Tank, 1 = Pipes, 2 = Bottom Tank
    def __str__(self):
        return "resource"