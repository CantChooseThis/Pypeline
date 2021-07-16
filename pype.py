import pygame as pg
import random as r
from liquid import Liquid
# from enum import Enum
#
# class Dir(Enum)

class Pype:
    def __init__(self, x=0, y=0):
        choices = ["corner", "plus", "straight", "t"]
        img = r.choice(choices)
        self.name = img
        if img == "corner":
            self.open = [False, True, True, False] # North, South, East, West
        elif img == "plus":
            self.open = [True, True, True, True]
        elif img == "t":
            self.open = [False, True, True, True]
        else:
            self.open = [False, False, True, True]
        img = pg.image.load(".\\Art\\"+img+"_piece.png")
        self.surface = img
        self.rect = img.get_rect(x=x, y=y)
        self.surface.set_colorkey((0, 255, 0))
        self.n = [None, None, None, None]
        self.filled = False
        self.liquid = Liquid(x, y)
        self.filledby = [False, False, False, False]
        self.source = False

    def __str__(self):
        return "Pype"

    def rotate(self, amount):
        self.surface = pg.transform.rotate(self.surface, amount)
        self.rect = self.surface.get_rect(x=self.rect.x, y=self.rect.y)
        if amount == 90:
            self.open = [self.open[2], self.open[3], self.open[1], self.open[0]]
        if amount == -90:
            self.open = [self.open[3], self.open[2], self.open[0], self.open[1]]

    def connected(self, other, edge):
        if edge == 0: # North = 0, South = 1, East = 2, West = 3
            return self.open[edge] and other.open[1]
        elif edge == 1:
            return self.open[edge] and other.open[0]
        elif edge == 2:
            return self.open[edge] and other.open[3]
        elif edge == 3:
            return self.open[edge] and other.open[2]
