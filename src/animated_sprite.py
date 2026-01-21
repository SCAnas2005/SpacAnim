from pygame import Rect, Surface
import pygame

from src.maths import vec2

class AnimatedFrames:
    def __init__(self, frame_per_seconds=5) -> None:
        self.frames = []
        self.set_fps(frame_per_seconds)
        self.current_index = 0

        self.is_finished = False
        self.loop = False

        self.rotation_angle:float = None # type: ignore
        self.scale:float = 1.0 
        self.origin = vec2.zero()

    def set_rotation_angle(self, angle:float):
        self.rotation_angle = angle
    
    # <--- NOUVEAU
    def set_scale(self, scale:float):
        self.scale = scale

    def set_origin(self, origin:vec2):
        self.origin = origin

    def set_fps(self, fps:int):
        self.fps = fps
        self.frame_duration = 1000 / self.fps

    def set_loop(self, loop:bool):
        self.loop = loop

    def get_current_frame(self) -> Surface:
        if (self.count() == 0): return None # type: ignore
        return self.frames[self.current_index]

    def count(self) -> int:
        return len(self.frames)
    
    def add_frame(self, frame:Surface):
        self.frames.append(frame)



class AnimatedSprite:
    def __init__(self) -> None:
        self.animations:dict[str, AnimatedFrames] = {}
        self.current_animation:AnimatedFrames = None # type: ignore
        self.current_animation_name:str = None # type: ignore
        self.timer = 0
        self.rotation_angle:float = None # type: ignore
        self.scale:float = 1.0 # <--- NOUVEAU : Scale global par défaut
        self.origin = vec2.zero()


    def get_current_animation(self):
        return self.current_animation

    def get_current_animation_name(self):
        return self.current_animation_name
    
    def get(self, name:str) -> AnimatedFrames: # type: ignore
        if (name in self.animations.keys()):
            return self.animations[name]

    # <--- NOUVEAU : Ajout paramètre scale
    def set_parameters_for_animation(self, name:str, loop=None, fps=None, rotation_angle=None, scale=None, origin=None):
        if name not in self.animations.keys(): return
        anim = self.get(name)
        if (loop != None): anim.set_loop(loop)
        if (fps != None): anim.set_fps(fps)
        if (rotation_angle != None): anim.set_rotation_angle(rotation_angle)
        if (scale != None): anim.set_scale(scale) # <---
        if (origin != None): anim.set_origin(origin)

    # <--- NOUVEAU : Ajout paramètre scale
    def set_parameters_for_current_animation(self, loop=None, fps=None, rotation_angle=None, scale=None, origin=None):
        self.set_parameters_for_animation(self.current_animation_name, loop, fps, rotation_angle, scale, origin)

    def add(self, name:str) -> None:
        self.animations[name] = AnimatedFrames()
        self.animations[name].set_rotation_angle(self.rotation_angle)
        self.animations[name].set_scale(self.scale) # <--- On applique le scale par défaut
        self.animations[name].set_origin(self.origin)

    def add_frame(self, name:str, frame:Surface):
        if (name not in self.animations):
            self.add(name)
        self.get(name).add_frame(frame)

    def add_from_sheet(self, name: str, sheet: Surface, start_x: int, start_y: int, width: int, height: int, count: int, fps: int = 10, loop: bool = True):
        if name not in self.animations:
            self.add(name)
        
        anim = self.get(name)
        anim.set_fps(fps)
        anim.loop = loop

        for i in range(count):
            frame_x = start_x + (i * width)
            frame_y = start_y
            rect = Rect(frame_x, frame_y, width, height)
            
            try:
                frame_surface = sheet.subsurface(rect)
                anim.add_frame(frame_surface)
            except ValueError:
                print(f"Erreur découpe '{name}' frame {i}")

    def play(self, name:str):
        if name in self.animations.keys():
            self.current_animation_name = name
            self.current_animation = self.animations[name]
            self.current_animation.current_index = 0
            self.timer = 0
            self.current_animation.is_finished = False

    def update(self, delta_time:float):
        if (self.current_animation == None): return
        self.timer += delta_time * 1000
        if (self.timer >= self.current_animation.frame_duration):
            self.timer = 0
            self.current_animation.current_index += 1
            if self.current_animation.current_index >= self.current_animation.count():
                if self.current_animation.loop:
                    self.current_animation.current_index = 0
                else:
                    self.current_animation.current_index = self.current_animation.count() - 1
                    self.current_animation.is_finished = True


    # <--- C'EST ICI QUE TOUT SE PASSE
    def draw(self, window:Surface, position:vec2):
        if (self.current_animation != None):
            anim = self.current_animation
            original_image = anim.get_current_frame()
            final_image = original_image

            # 1. D'abord on gère le SCALE (Taille)
            # On ne fait le calcul que si la taille change (optimisation)
            if anim.scale != 1.0:
                new_width = int(original_image.get_width() * anim.scale)
                new_height = int(original_image.get_height() * anim.scale)
                final_image = pygame.transform.scale(original_image, (new_width, new_height))

            # 2. Ensuite on gère la ROTATION
            if anim.rotation_angle != None:
                # Si on a déjà scale, on tourne l'image redimensionnée
                final_image = pygame.transform.rotate(final_image, anim.rotation_angle)
                
                # Le rectangle centré est vital quand on tourne une image
                rect = final_image.get_rect(center=position.toTuple())
                window.blit(final_image, rect)
            
            else:
                # Cas sans rotation mais AVEC potentiellement du scale
                # Si on a scale, il faut quand même centrer l'image sinon elle va se décaler
                if anim.scale != 1.0:
                    rect = final_image.get_rect(center=position.toTuple())
                    window.blit(final_image, rect)
                else:
                    # Cas simple : pas de rotation, pas de scale
                    # Note: Si tu veux que 'position' soit toujours le CENTRE, utilise aussi get_rect ici.
                    # Actuellement ton code d'origine dessinait le coin haut-gauche si pas de rotation.
                    # Pour être cohérent, je te conseille de centrer aussi ici :
                    rect = final_image.get_rect(center=position.toTuple())
                    window.blit(final_image, rect)