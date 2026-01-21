
from pygame import Surface
import pygame




class Scene:
    def __init__(self, state) -> None:
        self.state = state
    

    def handle_event(self, event:pygame.event.Event):
        pass

    def init(self):
        pass

    def load(self):
        pass

    def restart_scene(self):
        pass

    def update(self, delta_time:float):
        pass

    def draw(self, window:Surface):
        pass
