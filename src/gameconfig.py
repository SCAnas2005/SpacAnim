
from src.maths import vec2


class GameConfig:
    SCREEN_WIDTH = 1080
    SCREEN_HEIGHT = 720
    
    GRAVITY = vec2(0, 200)

    FPS = 60

    @staticmethod
    def get_screen_size()->tuple:
        return (GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT)
