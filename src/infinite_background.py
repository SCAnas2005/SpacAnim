import pygame


class InfiniteBackground:
    def __init__(self, screen_size):
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        
        # Charge ton image (garde-la assez grande, ex: 1024x1024 ou plus)
        self.image = pygame.image.load("assets/space.png").convert()
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def update(self, delta_time):
        # PLUS RIEN ICI !
        # On n'utilise plus de vitesse automatique ou de temps.
        pass

    def draw(self, window, camera):
        # 1. Calcul du décalage (Parallax)
        # On veut que le fond bouge MOINS VITE que la caméra pour donner de la profondeur.
        # 0.5 = Le fond est 2x plus loin (bouge à 50% de la vitesse)
        # 0.1 = Le fond est très loin (bouge à 10%)
        parallax_factor = 0.5 
        
        # L'opérateur % (modulo) fait en sorte que x reste toujours entre 0 et la largeur de l'image
        # C'est ça qui crée la boucle infinie
        rel_x = -(camera.pos.x * parallax_factor) % self.width
        rel_y = -(camera.pos.y * parallax_factor) % self.height

        # 2. Dessin (Tuiles)
        # On doit dessiner l'image 4 fois pour couvrir tous les coins quand on bouge en diagonale
        
        # Image principale
        window.blit(self.image, (rel_x, rel_y))
        
        # Image répétée à gauche
        if rel_x > 0:
            window.blit(self.image, (rel_x - self.width, rel_y))
            
        # Image répétée au dessus
        if rel_y > 0:
            window.blit(self.image, (rel_x, rel_y - self.height))
            
        # Image répétée en diagonale (coin haut-gauche)
        if rel_x > 0 and rel_y > 0:
            window.blit(self.image, (rel_x - self.width, rel_y - self.height))