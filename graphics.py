import pygame
from pygame.locals import *

class Graphics:
    def __init__(self):
        self.sprites = None
        self.display_surf = None
        self.size = None

    def initialize(self, size):
        self.size = size
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.sprites = {
        'S' : pygame.Color(255, 0, 0),
        'I' : pygame.Color(0, 255, 0),
        'R' : pygame.Color(0, 0, 255)
        }

    def render_world(self, world):
        self.display_surf.fill(Color(0,0,0,0))
        for a in world.actors:
            current_color = self.sprites[a.state]
            pygame.draw.circle(self.display_surf, current_color, [int(x) for x in a.position], 5)

        pygame.display.flip()