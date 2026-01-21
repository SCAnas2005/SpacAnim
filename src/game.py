import pygame
from src.scene_manager import SceneManager
from src.maths import vec2
from src.gameconfig import * 
from src.meteor import *

from src.timer import TimerManager

class Game:
    window: pygame.Surface = None # type: ignore

    def __init__(self) -> None:
        self.init()
        Game.clock = pygame.time.Clock()
        Game.window = pygame.display.set_mode(GameConfig.get_screen_size())
        Game.font = pygame.font.Font(None, 32)
        Game.timer_manager = TimerManager()

        SceneManager.init()

        pygame.display.set_caption("SpacAnime")
        Game.running = True

    def init(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

    def update(self, delta_time:float):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.running = False
            SceneManager.get_current_scene().handle_event(event)
        SceneManager.get_current_scene().update(delta_time)
        self.timer_manager.update(delta_time)

    def draw(self, window:pygame.Surface):
        window.fill((0,0,0))
        self.draw_fps_label(window)
        SceneManager.get_current_scene().draw(window)
        pygame.display.flip()

    def draw_fps_label(self, window:pygame.Surface):
        fps_label = self.font.render(f"FPS:{int(Game.clock.get_fps())}", False, (255,255,255))
        pos = vec2(GameConfig.get_screen_size()[0]-fps_label.get_size()[0]-10, 0)
        window.blit(fps_label, pos.toTuple())

    def run(self):
        print("Running game")
        while Game.running:
            delta_time = self.clock.tick(GameConfig.FPS)/1000 
            self.update(delta_time)
            self.draw(Game.window) # Utilisation de Game.window