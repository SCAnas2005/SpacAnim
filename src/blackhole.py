import random
from pygame import Surface
import pygame
from src.spaceship import Spaceship
from src.camera import Camera
from src.maths import vec2


class BlackHole:
    def __init__(self, pos:vec2, mass:float = 10000, horizon_radius:float = 1000) -> None:
        self.pos = pos
        self.mass = mass
        self.horizon_radius = horizon_radius
        self.kill_radius = 50


        self.image = pygame.image.load("assets/blackhole/blackhole.png")
        self.angle = 0
        self.rotation_speed = 20
        self.origin = vec2(self.image.get_width()/2, self.image.get_height()/2)

    def update(self, dt:float):
        self.angle += self.rotation_speed * dt
        from src.game_scene import GameScene
        # Applique la gravité aux player
        self.apply_gravity(GameScene.spaceship)

        # Applique la gravité aux meteors
        for m in GameScene.meteorManager.meteors:
            self.apply_gravity(m)

    def draw(self, window:Surface, cam:Camera):
        screen_pos = self.pos - cam.pos
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=screen_pos.toTuple())
        window.blit(rotated_image, rect)


    def apply_gravity(self, target_obj):
        diff = self.pos - target_obj.pos
        distance = diff.magnitude()

        

        if (distance < self.horizon_radius and distance > 5):
            if isinstance(target_obj, Spaceship):
                target_obj.angle += random.uniform(-5,5)
            force_magnitude = self.mass / distance
            gravity_vector = diff.normalize() * force_magnitude

            target_obj.velocity += gravity_vector

            if (distance  < self.kill_radius):
                target_obj.destroy()