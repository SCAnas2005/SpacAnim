import random
import pygame
from src.animated_sprite import AnimatedSprite
from src.camera import Camera
from src.gameconfig import GameConfig
from src.maths import vec2


class Meteor:
    def __init__(self, pos:vec2, dir:vec2, image:pygame.Surface, scale:float=1.0, offset_hitbox:pygame.Rect=pygame.Rect(0,0,0,0)) -> None:
        self.image = image
        self.pos = pos
        self.dir = dir
        self.scale = scale

        self.speed = random.uniform(200, 800)
        self.velocity = self.dir.normalize() * self.speed

        self.animated_sprite = AnimatedSprite()
        self.animated_sprite.add("idle")
        self.animated_sprite.add("explosion")

        self.offset_hitbox = offset_hitbox

        self.animated_sprite.add_frame("idle", frame=self.image)
        self.animated_sprite.add_from_sheet(
            name="explosion", 
            sheet=pygame.image.load("assets/meteors/explosion.png"),
            start_x=0, start_y=0,
            width=96,height=96,
            count=6, fps=10,
            loop=False
        )

        self.animated_sprite.set_parameters_for_animation("idle", scale=scale)
        self.animated_sprite.set_parameters_for_animation("explosion", scale=scale)

        self.is_destroy = False
        self.is_dead = False

        self.animated_sprite.play("idle")
    
    def get_hitbox(self) -> pygame.Rect:
        # 1. Calculer la position du coin Haut-Gauche de l'IMAGE (car self.pos est le centre)
        # On prend en compte le scale actuel
        image_width = self.image.get_width() * self.scale
        image_height = self.image.get_height() * self.scale
        
        image_top_left_x = self.pos.x - (image_width / 2)
        image_top_left_y = self.pos.y - (image_height / 2)

        # 2. Appliquer l'offset de la hitbox (en prenant en compte le scale aussi !)
        return pygame.Rect(
            image_top_left_x + (self.offset_hitbox.x * self.scale), 
            image_top_left_y + (self.offset_hitbox.y * self.scale), 
            self.offset_hitbox.width * self.scale, 
            self.offset_hitbox.height * self.scale
        )      

    def destroy(self):
        self.is_destroy = True 

    def update(self, delta_time:float):
        self.animated_sprite.update(delta_time)
        if (not self.is_dead and not self.is_destroy):
            self.pos += self.velocity * delta_time
        elif (self.is_destroy):
            if (self.animated_sprite.current_animation_name != "explosion"):
                self.animated_sprite.play("explosion")
            elif (self.animated_sprite.current_animation.is_finished):
                self.is_dead = True

    def draw_hitbox(self, window:pygame.Surface, cam: Camera):
        hitbox = self.get_hitbox()
        hitbox.x -= int(cam.pos.x)
        hitbox.y -= int(cam.pos.y)
        pygame.draw.rect(window, (255,255,255), hitbox, 1)

    def draw(self, window:pygame.Surface, cam:Camera):
        screen_pos = self.pos - cam.pos
        # original_image = self.image
        # final_image = original_image
        # if (self.scale != 1.0): 
        #     s = (self.image.get_width() * self.scale, self.image.get_height() * self.scale)
        #     final_image = pygame.transform.scale(original_image, s)

        # window.blit(final_image, screen_pos.toTuple())
        self.animated_sprite.draw(window, screen_pos)
        self.draw_hitbox(window, cam)



class MeteorManager:
    def __init__(self) -> None:
        self.meteors:list[Meteor] = []
        self.spawn_timer = 0.0
        self.spawn_delay = 2.0

        self.meteor_image = pygame.image.load("assets/meteors/base_meteor.png")
        self.explosion_sound = pygame.mixer.Sound("assets/spaceships/main/sounds/explosion.mp3")
        self.explosion_channel = pygame.mixer.Channel(3)

    def spawn_outsite_camera(self, cam:Camera, target:vec2, player_velocity:vec2):
        margin = 100
        screen_w = GameConfig.get_screen_size()[0]
        screen_h = GameConfig.get_screen_size()[1]
        
        choices = ["top", "bottom", "left", "right"]
        if player_velocity.x > 50:    # Je vais à Droite
            choices.extend(["right"] * 6) # 6x plus de chances d'apparaitre à droite
        elif player_velocity.x < -50: # Je vais à Gauche
            choices.extend(["left"] * 6)
            
        if player_velocity.y > 50:    # Je descends
            choices.extend(["bottom"] * 6)
        elif player_velocity.y < -50: # Je monte
            choices.extend(["top"] * 6)

        side = random.choice(choices)
        start_pos = vec2.zero()

        if side == "top":
            start_pos.x = random.uniform(cam.pos.x, cam.pos.x + screen_w)
            start_pos.y = cam.pos.y - margin
        elif side == "bottom":
            start_pos.x = random.uniform(cam.pos.x, cam.pos.x + screen_w)
            start_pos.y = cam.pos.y + screen_h + margin

        elif side == "right":
            start_pos.x = cam.pos.x + screen_w + margin
            start_pos.y = random.uniform(cam.pos.y, cam.pos.y + screen_h)
        elif side == "left":
            start_pos.x = cam.pos.x - margin
            start_pos.y = random.uniform(cam.pos.y, cam.pos.y + screen_h)


        scale = random.uniform(1.0, 2.0)
        futur_target = target + (player_velocity * 1.5)
        new_meteor = Meteor(
            pos=start_pos, 
            dir=(futur_target-start_pos), 
            image=self.meteor_image, 
            scale=scale,
            offset_hitbox=pygame.Rect(28.5, 31, 39, 34),
        )
        self.meteors.append(new_meteor)


    def update(self, delta_time:float, cam:Camera, target:vec2, player_velocity:vec2):

        self.spawn_timer -= delta_time
        if (self.spawn_timer <= 0):
            self.spawn_outsite_camera(cam=cam, target=target, player_velocity=player_velocity)
            self.spawn_timer = self.spawn_delay

        for meteor in self.meteors:
            meteor.update(delta_time)
            hitbox = meteor.get_hitbox()
            for m in self.meteors:
                if m == meteor: continue
                if hitbox.colliderect(m.get_hitbox()):
                    m.destroy()
                    meteor.destroy()
            if (meteor.is_destroy):
                if (not self.explosion_channel.get_busy()):
                    self.explosion_channel.play(self.explosion_sound)
        
        self.meteors = [m for m in self.meteors if not m.is_dead and (m.pos-target).magnitude() < 3000]

    def draw(self, window:pygame.Surface, cam:Camera):
        for meteor in self.meteors:
            meteor.draw(window, cam)
