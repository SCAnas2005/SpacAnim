
import random
import pygame

from src.maths import vec2

class Particule:
    def __init__(self, pos:vec2, velocity:vec2, life:float, size:float, color:pygame.Color) -> None:
        self.pos = pos
        self.velocity = velocity
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size
    
    def update(self, delta_time:float):
        self.pos += self.velocity * delta_time
        self.life -= delta_time

    def draw(self, window:pygame.Surface):
        if self.life <= 0: return
        current_size = self.size * (self.life / self.max_life)
        pygame.draw.circle(window, self.color, self.pos.toTuple(), int(current_size))

class ParticuleSystem:
    def __init__(self) -> None:
        self.particules:list[Particule] = []

    def emit(self, pos:vec2, direction:vec2, count:int = 1):
        for _ in range(count):
            spread_angle = random.uniform(-0.5, 0.5) # angle en radian
            vx = direction.x * 1#random.uniform(-0.5, 0.5)
            vy = direction.y * 1#random.uniform(-0.5, 0.5)

            speed = random.uniform(100, 300)
            vel = vec2(vx, vy).normalize() * speed
            p = Particule(
                pos=pos,
                velocity=vel*-1,
                life=random.uniform(0.2, 0.6),
                size=random.uniform(3, 8),
                color=pygame.Color(255, random.randint(100,200), 0)
            )
            self.particules.append(p)

    
    def update(self, delta_time:float):
        self.particules = [p for p in self.particules if p.life > 0]
        for p in self.particules:
            p.update(delta_time)

    def draw(self, window:pygame.Surface):
        for p in self.particules:
            p.draw(window)
        



