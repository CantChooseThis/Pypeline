import pygame as pg


class Liquid:
    def __init__(self, x, y):
        img = pg.image.load(".\\Art\\red.png")
        self.surface = img
        self.rect = img.get_rect(x=x, y=y)