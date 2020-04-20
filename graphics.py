import pygame
import numpy as np
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
        0 : pygame.Color(255, 0, 0),
        1 : pygame.Color(0, 255, 0),
        2 : pygame.Color(0, 0, 255)
        }

    def render_world(self, world):
        self.display_surf.fill(Color(0,0,0,0))
        font = pygame.font.SysFont('Tahoma', 10, True, False)
        symbols = [
            'x', 'o', 's']
        symbols = [p.behaviour.name[0] for p in world.populations]

        for j, p in enumerate(world.populations):
            indices = np.argwhere(p.states)

            for i in range(len(indices)):
                current_color = self.sprites[indices[i][0]]
                renders = [
                    font.render(symb, True, current_color)
                    for symb in symbols]                            
                self.display_surf.blit(
                    renders[j % len(renders)],
                    [int(x) for x in p.positions[:,indices[i][1]]])
        pygame.display.flip()
