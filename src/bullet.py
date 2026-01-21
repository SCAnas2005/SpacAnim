import math
import pygame
from src.camera import Camera
from src.maths import vec2


class Bullet:
    def __init__(self, pos:vec2, dir:vec2, damage:float, speed:float, image:pygame.Surface, scale:float=1.0) -> None:
        self.pos = pos
        self.dir = dir
        self.damage = damage
        self.speed = speed
        self.image = image
        self.scale = scale
        
        self.is_dead = False

        if self.scale != 1.0:
            new_w = int(self.image.get_width() * self.scale)
            new_h = int(self.image.get_height() * self.scale)
            self.image = pygame.transform.scale(self.image, (new_w, new_h))

    def get_hitbox(self) -> pygame.Rect:
        return pygame.Rect(self.pos.x, self.pos.y, self.image.get_width() * self.scale, self.image.get_height() * self.scale)

    def update(self, delta_time:float):
        if (self.is_dead == True): return
        velocity = self.dir * self.speed * delta_time
        self.pos += velocity

    def draw(self, window:pygame.Surface, cam:Camera):
        screen_pos = self.pos - cam.pos
        original_image = self.image
        final_image = original_image
        window.blit(final_image, screen_pos.toTuple())


class BulletManager:
    def __init__(self) -> None:
        self.bullets:list[Bullet] = []
        self.image = pygame.image.load("assets/spaceships/main/bullets/bullet_blue.png")
        self.sound = pygame.mixer.Sound("assets/spaceships/main/bullets/bullet_blue_sound.mp3")
        self.sound_channel = pygame.mixer.Channel(5)

    def add(self, pos:vec2, dir:vec2, scale:float=1):
        angle_rad = math.atan2(dir.y, dir.x)
        angle_degrees = math.degrees(angle_rad)
        transformed_iamge = pygame.transform.rotate(self.image, -angle_degrees)
        b = Bullet(
            pos=pos,
            dir=dir,
            damage=30.0,
            speed=2000,
            image=transformed_iamge,
            scale=scale
        )
        self.bullets.append(b)
        self.sound_channel.play(self.sound)

    def update(self, delta_time:float, cam:Camera):
        from src.game_scene import GameScene
        # collision avec les meteors
        for b in self.bullets:
            if b.is_dead: continue
            hitbox_bullet = b.get_hitbox()
            for m in GameScene.meteorManager.meteors: # type: ignore
                if m.is_dead or m.is_destroy: continue
                hitbox_meteor = m.get_hitbox()
                if (hitbox_bullet.colliderect(hitbox_meteor)):
                    m.destroy()
                    b.is_dead = True
                    break
        
        for b in self.bullets:
            if (b.is_dead): continue
            b.update(delta_time)
        
        self.bullets = [b for b in self.bullets if not b.is_dead and (b.pos - cam.pos).magnitude() < 2000]

    def draw(self, window:pygame.Surface, cam:Camera):
        for b in self.bullets:
            b.draw(window, cam)