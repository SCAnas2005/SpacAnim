
from pygame import Surface
import pygame

from src.blackhole import BlackHole
from src.scene import Scene
from src.gameconfig import GameConfig
from src.maths import vec2
from src.camera import Camera
from src.game_state import GameState
from src.infinite_background import InfiniteBackground
from src.spaceship import Spaceship 
from src.meteor import MeteorManager


class GameScene(Scene):

    def __init__(self) -> None:
        super().__init__(GameState.GAMEPLAY)
        
        self.space_background = InfiniteBackground("assets/nebula_blue.png")
        GameScene.spaceship = Spaceship()
        
        GameScene.camera = Camera(pos=vec2.zero(), screen_size=vec2(GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        GameScene.camera.look_at(GameScene.spaceship)

        GameScene.meteorManager = MeteorManager()
        GameScene.blackhole = BlackHole(vec2(3000,3000))

        self.font = pygame.font.Font(None, 32)

        self.changing_scene = False

    def restart_scene(self):
        GameScene.meteorManager = MeteorManager()
        self.changing_scene = False
        self.spaceship.reinit()
        self.camera.look_at(self.spaceship)

    def init(self):
        pass

    def load(self):
        pass
    
    def update(self, delta_time:float):
        super().update(delta_time)
        keys = pygame.key.get_pressed()
        
        if (keys[pygame.K_t]):
            mouse_pos = pygame.mouse.get_pos()
            GameScene.spaceship.set_pos(vec2(500, 500))

        GameScene.camera.update()
        self.space_background.update(delta_time)
        
        GameScene.spaceship.update(delta_time, cam=GameScene.camera)
        GameScene.meteorManager.update(delta_time, GameScene.camera, GameScene.spaceship.pos, GameScene.spaceship.velocity)
        GameScene.blackhole.update(delta_time)

        if not GameScene.spaceship.is_dead and not GameScene.spaceship.explosion: 
            GameScene.spaceship.check_collision(GameScene.meteorManager.meteors)
        if (GameScene.spaceship.is_dead and not self.changing_scene):
            self.changing_scene = True
            from src.game import Game
            def f():
                from src.scene_manager import SceneManager
                SceneManager.set_scene(GameState.MENU)
            Game.timer_manager.add_timer(2.0, f)


    def draw(self, window:Surface):
        window.fill((255,255,255))
        self.space_background.draw(window, camera=GameScene.camera)
        
        GameScene.blackhole.draw(window, cam=GameScene.camera)
        GameScene.spaceship.draw(window, cam=GameScene.camera)
        GameScene.meteorManager.draw(window, cam=GameScene.camera)
        
        self.draw_space_ship_info(window)
        
        pygame.display.flip()


    def draw_space_ship_info(self, window:pygame.Surface):
        s = GameScene.spaceship 
        label_list = [
            f"position: {s.pos}",
            f"size: ({s.width}, {s.height})",
            f"angle: {int(s.angle)}",
            f"speed: {int(s.velocity.magnitude())}/{int(s.max_speed)}", # Corrige self.speed qui n'existe plus
            f"velocity: {s.velocity}",
            f"attractive force: {GameConfig.GRAVITY}",
            f"etat: {'destroyed' if s.is_dead or s.explosion else 'ok'}"
        ]
        
        pos = vec2(10, 10)
        for label in label_list:
            render = self.font.render(label, False, (255,255,255))
            window.blit(render, pos.toTuple())
            pos.y += render.get_size()[1] + 5
