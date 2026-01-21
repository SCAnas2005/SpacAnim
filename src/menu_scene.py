
from pygame import Surface
import pygame
from pygame.event import Event

from src.scene import Scene
from src.gameconfig import GameConfig
from src.maths import vec2
from src.game_state import GameState


class MenuScene(Scene):
    def __init__(self) -> None:
        super().__init__(GameState.MENU)
        self.screen_size = GameConfig.get_screen_size()
        self.font_title = pygame.font.Font(None, 60)
        self.title = self.font_title.render("SpacAnim", False, (255,255,255))

        self.font_play = pygame.font.Font(None, 40)
        self.play_label = self.font_play.render("Appuyer sur [Espace] pour jouer", False, (255,255,255))

        self.prev_keys = pygame.key.get_pressed()
        self.can_press_space = True


        self.controls_strings_list = [
            "Acceleration : Z",
            "Déplacément horizontale : Q,D",
            "Tirer : Espace",
            "Rotation du vaisseau : <-, ->",
            "Téléportation au point (500,500) : T"
        ]

        self.controls_label = []

        for c in self.controls_strings_list:
            control = self.font_play.render(c, False, (255,255,255))
            self.controls_label.append(control)
    
    def handle_event(self, event: Event):
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_SPACE and self.can_press_space:
                from src.game import Game
                def f():
                    self.can_press_space = True
                    from src.scene_manager import SceneManager
                    SceneManager.set_scene(scene=GameState.GAMEPLAY)
                Game.timer_manager.add_timer(delay=1.0, callback=f)             
                self.can_press_space = False

    def update(self, delta_time:float):
        super().update(delta_time)

    def draw_controls(self, window:Surface):
        screen_width = window.get_width()
        screen_height = window.get_height()
        
        line_spacing = 10
        
        total_text_height = sum(label.get_height() for label in self.controls_label) + (line_spacing * (len(self.controls_label) - 1))
        
        start_y = screen_height - total_text_height - 50
        
        current_y = start_y

        for label in self.controls_label:
            pos_x = 30
            
            window.blit(label, (pos_x, current_y))
            
            current_y += label.get_height() + line_spacing

    def draw(self, window:Surface):
        window.fill((0,0,0))
        window.blit(self.title, vec2((self.screen_size[0] - self.title.get_width())/2, 200).toTuple())
        window.blit(self.play_label, vec2((self.screen_size[0]-self.play_label.get_width())/2, 250+self.title.get_height()).toTuple())
        self.draw_controls(window)
        pygame.display.flip()