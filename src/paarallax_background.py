
from pygame import Surface
import pygame
from src.maths import *

class ParallaxBackground:
    def __init__(self, background:str, stars: str = None) -> None: # type: ignore
        self.image = pygame.image.load(background)
        self.stars =  pygame.image.load(stars) if stars != None  else None

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.p1 = vec2.zero()
        self.p2 = vec2(0.0, self.height)

        self.scroll_speed = 250.0

    def update(self, delta_time:float):
        self.p1.y -= self.scroll_speed * delta_time # type: ignore
        self.p2.y -= self.scroll_speed * delta_time

        if (self.p1.y +self.height < 0): # type: ignore
            self.p1.y = self.p2.y + self.height

        if (self.p2.y + self.height < 0):
            self.p2.y = self.p1.y + self.height 

    def draw(self, window:Surface):
        window.blit(self.image, self.p1.toTuple()) # type: ignore
        window.blit(self.image, self.p2.toTuple())

        if (self.stars != None):
            window.blit(self.stars, self.p1.toTuple())
            window.blit(self.stars, self.p2.toTuple())