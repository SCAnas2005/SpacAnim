
from src.maths import vec2


class Camera:
    def __init__(self, pos:vec2, screen_size:vec2) -> None:
        self.pos = pos
        self.screen_size = screen_size
        self.target = None # type: ignore
    
    def center_player(self, pos:vec2) -> vec2:
        return vec2(pos.x - (self.screen_size.x/2), pos.y - (self.screen_size.y/2))

    def look_at(self, spaceship):
        self.target = spaceship

    def update(self):
        if self.target == None: return

        self.pos = self.center_player(self.target.pos)
        vector_to_target = self.target.pos - self.pos
        self.pos += vector_to_target * 0.05

