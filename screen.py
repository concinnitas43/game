import pygame
import random
from obj import *
from vec import *

FPS = 30
dt = 1 / 30
N = 10
asteroidtimer = 100
WIDTH, HEIGHT = 480, 640
ACC = 40
TRQ = 30


def dist2(vec1, vec2):
    return (vec1.x - vec2.x)**2 + (vec1.y - vec2.y)**2


class Screen:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.config = {}


class ScreenManager:

    def __init__(self):

        self.screens = []
        self.current = None



