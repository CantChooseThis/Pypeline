import pygame as pg


class Resource:
    def __init__(self, x=0, y=0):
        self.surface = pg.image.load(".\\Art\\red.png")
        self.rect = self.surface.get_rect(x=x,y=y)
        self.stage = 0   # 0 = Top Tank, 1 = Pipes, 2 = Bottom Tank

    def col(self):
        return self.rect.x//36

    def row(self):
        return self.rect.y//36

    def __str__(self):
        return "R"