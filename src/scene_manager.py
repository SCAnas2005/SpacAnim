
from src.scene import Scene
from src.game_scene import GameScene
from src.menu_scene import MenuScene
from src.game_state import GameState


class SceneManager:
    scenes: dict[GameState, Scene]
    current_scene_name: GameState

    @staticmethod
    def init() -> None:
        SceneManager.scenes = {
            GameState.MENU:MenuScene(), 
            GameState.GAMEPLAY:GameScene()
        }
        SceneManager.current_scene_name = GameState.MENU

    @staticmethod
    def get_current_scene() -> Scene:
        return SceneManager.scenes[SceneManager.current_scene_name]

    @staticmethod
    def set_scene(scene:GameState):
        if SceneManager.current_scene_name not in SceneManager.scenes.keys(): return
        SceneManager.current_scene_name = scene
        SceneManager.get_current_scene().restart_scene()