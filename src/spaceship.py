
from pygame import Surface
import pygame

import math 
from src.bullet import BulletManager
from src.maths import vec2,clamp
from src.gameconfig import *
from src.animated_sprite import *
from src.particule import ParticuleSystem
from src.camera import Camera

class Spaceship:
    def __init__(self) -> None:
        self.image = pygame.image.load("assets/spaceships/main/main_ship-1.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        screen_size = GameConfig.get_screen_size()
        self.pos = vec2((screen_size[0]-self.width)/2, screen_size[1]-300)

        self.max_speed = 1500
        self.mov_dir = vec2(0, 0)

        self.acceleration = 500.0
        self.decceleration = 200.0

        self.speed = 0.0
        self.velocity = vec2.zero()


        self.origin = vec2(0,0) # Pivot du point de rotation du vaisseau
        self.angle_decalage = 90 # L'angle 0 pointe vers la droite, donc j'ajoute 90 pour pointer vers le haut
        self.angle = 0 # Pointe vers le haut
        self.rotation_speed = 150
        self.forward_dir = vec2(math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
        self.right_dir = vec2(-self.forward_dir.y, self.forward_dir.x) # calcule la normal du vecteur forward (en gros c'est faire le perpendiculaire)


        self.is_accelerating = False



        self.animated_sprite = AnimatedSprite()
        self.create_animation()
        self.animated_sprite.play("idle")

        self.particuleSystem = ParticuleSystem()

        self.explosion_sound = pygame.mixer.Sound("assets/spaceships/main/sounds/explosion.mp3")
        self.engine_idle_sound = pygame.mixer.Sound("assets/spaceships/main/sounds/idle.wav")
        self.engine_thrust_sound = pygame.mixer.Sound("assets/spaceships/main/sounds/thrust_engine.mp3")
        self.engine_thrust_sound.set_volume(0.5)


        self.engine_idle_channel = pygame.mixer.Channel(0)
        self.engine_thrust_channel = pygame.mixer.Channel(1)
        self.explosion_channel = pygame.mixer.Channel(2)

        self.engine_idle_channel.play(self.engine_idle_sound, loops=-1)

        self.is_dead = False
        self.explosion = False


        self.bullet_manager = BulletManager()
        self.prev_keys = pygame.key.get_pressed()

    def reinit(self):
        self.is_dead = False
        self.explosion = False
        self.bullet_manager = BulletManager()

        self.pos = vec2(1000,1000)

        self.is_accelerating = False
        self.angle = 0 # regarde vers le haut
        self.forward_dir = vec2(math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
        self.right_dir = vec2(-self.forward_dir.y, self.forward_dir.x) 

        self.animated_sprite.play("idle")

    def create_animation(self):
        name = "idle"
        self.animated_sprite.add_from_sheet(
            name=name, 
            sheet=pygame.image.load("assets/spaceships/main/spritesheet_spaceship.png"), 
            start_x=0, start_y=0, width=48, height=58,
            fps=3, 
            count=3, 
            loop=True
        )

        name = "right"
        self.animated_sprite.add_from_sheet(
            name=name, 
            sheet=pygame.image.load("assets/spaceships/main/spritesheet_spaceship.png"), 
            start_x=0, start_y=58*2, width=48, height=58,
            fps=3, 
            count=3, 
            loop=True
        )

        name = "left"
        self.animated_sprite.add_from_sheet(
            name=name, 
            sheet=pygame.image.load("assets/spaceships/main/spritesheet_spaceship.png"), 
            start_x=0, start_y=58 *4, width=48, height=58,
            fps=3, 
            count=3, 
            loop=True
        )


        name = "explosion"
        self.animated_sprite.add_from_sheet(
            name=name,
            sheet=pygame.image.load("assets/spaceships/main/explosion.png"),
            start_x=0, start_y=0,
            width=256, height=256,
            count=10,
            fps=10
        )

    def set_pos(self, new_pos:vec2):
        self.pos = new_pos

    def accelerate(self, delta_time:float):
        # self.speed += self.acceleration * delta_time
        push_force = self.forward_dir * self.acceleration * delta_time
        self.velocity += push_force

    def deccelerate(self, delta_time:float):
        current_speed = self.velocity.magnitude()
            
        if current_speed > 0:
            drop = self.decceleration * delta_time
            
            new_speed = max(0, current_speed - drop)
            
            if current_speed > 0: # Sécurité division par zéro
                self.velocity = self.velocity.normalize() * new_speed

    def destroy(self):
        self.engine_idle_channel.stop()
        self.engine_thrust_channel.stop()
        self.explosion = True


    def get_hitbox(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def check_collision(self, colliders:list):
        hitbox = self.get_hitbox()
        for collider in colliders:
            hitbox_collider = collider.get_hitbox()
            if (hitbox.colliderect(hitbox_collider)):
                self.destroy()
                collider.destroy()


    def update(self, delta_time:float, cam:Camera):
        pygame.event.pump()

        keys = pygame.key.get_pressed()

        keys = pygame.key.get_pressed()
        if (not self.is_dead and not self.explosion):
            self.is_accelerating = False
            if (keys[pygame.K_z]):
                self.is_accelerating = True
                self.accelerate(delta_time)
                if (not self.engine_thrust_channel.get_busy()):
                    self.engine_thrust_channel.play(self.engine_thrust_sound, loops=-1)
                pos = vec2(self.pos.x + self.width/2, self.pos.y + self.height)
                self.particuleSystem.emit(pos=pos, direction=self.forward_dir, count=2)
            else:
                self.is_accelerating = False
                if self.engine_thrust_channel.get_busy():
                    self.engine_thrust_channel.stop()
                self.deccelerate(delta_time)

            if (keys[pygame.K_RIGHT]):
                self.angle -= self.rotation_speed * delta_time
            if (keys[pygame.K_LEFT]):
                self.angle += self.rotation_speed * delta_time

            if (keys[pygame.K_d]):
                self.velocity += self.right_dir * self.acceleration * delta_time
                if (self.animated_sprite.current_animation_name != "right"):
                    self.animated_sprite.play("right")
            elif (keys[pygame.K_q]):
                self.velocity -= self.right_dir * self.acceleration * delta_time
                if (self.animated_sprite.current_animation_name != "left"):
                    self.animated_sprite.play("left")
            else:
                if (self.animated_sprite.current_animation_name != "idle"):
                    self.animated_sprite.play("idle")

            angle_radians = math.radians(-self.angle - self.angle_decalage)
            self.forward_dir = vec2(math.cos(angle_radians), math.sin(angle_radians))
            self.right_dir = vec2(-self.forward_dir.y, self.forward_dir.x)

            if (self.velocity.magnitude() > self.max_speed):
                self.velocity = self.velocity.normalize() * self.max_speed
            
            
            self.pos += self.velocity * delta_time
            self.pos += GameConfig.GRAVITY * delta_time

            self.speed = self.velocity.magnitude()
            self.particuleSystem.update(delta_time)

            if (keys[pygame.K_SPACE] and not self.prev_keys[pygame.K_SPACE]):
                self.bullet_manager.add(
                    pos=vec2(self.pos.x+self.width/2, self.pos.y + self.height/2),
                    dir=self.forward_dir,
                    scale=0.2
                )

            self.animated_sprite.set_parameters_for_current_animation(rotation_angle=self.angle)
            self.animated_sprite.update(delta_time)
                
        elif self.explosion:
            if (self.animated_sprite.current_animation_name != "explosion"):
                self.animated_sprite.get("explosion").loop = False
                self.animated_sprite.play("explosion")
                self.explosion_channel.play(self.explosion_sound)
            if (self.animated_sprite.current_animation.is_finished):
                self.is_dead = True

            self.animated_sprite.set_parameters_for_current_animation(rotation_angle=self.angle)
            self.animated_sprite.update(delta_time)
        
        elif self.is_dead:
            pass
    
        self.bullet_manager.update(delta_time, cam=cam)
        self.prev_keys = pygame.key.get_pressed()


    def draw(self, window:Surface, cam:Camera = None): # type: ignore
        if (self.is_dead): return
        if (cam != None):
            screen_pos = self.pos - cam.pos
        else:
            screen_pos = self.pos
        center_pos = vec2(
            screen_pos.x + self.width / 2,
            screen_pos.y + self.height/2
        )
        self.bullet_manager.draw(window, cam)
        self.animated_sprite.draw(window, center_pos)
        # self.particuleSystem.draw(window)
        pygame.draw.rect(window, "white", pygame.Rect(screen_pos.x, screen_pos.y, self.width, self.height), 1)

        line_start = center_pos
        line_end = center_pos + (self.forward_dir * 100)
        pygame.draw.line(window, (255,0,0), line_start.toTuple(), line_end.toTuple(), 1)

        line_start = center_pos
        line_end = center_pos + (self.right_dir * 100)
        pygame.draw.line(window, (0,255,0), line_start.toTuple(), line_end.toTuple(), 1)