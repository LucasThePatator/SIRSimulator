import pygame
import numpy as np
import math
from pygame.locals import *

class Graphics:
    def __init__(self):
        self.sprites = None
        self.display_surf = None
        self.size = None
        self.augment_x = None
        self.augment_y = None

    def initialize(self, size):
        augment_factor = 0.5
        self.augment_x = 20
        self.augment_y = 20

        self.basesize = size
        self.size = (size[0] + self.augment_x,
                     size[1] + self.augment_y)
        self.display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.sprites = {
        0 : pygame.Color(255, 0, 0),
        1 : pygame.Color(0, 255, 0),
        2 : pygame.Color(0, 0, 255)
        }

    def render_world(self, world):
        self.display_surf.fill(Color(0,0,0,0))
        font = pygame.font.SysFont('Tahoma', 10, True, False)
        symbols = [p.behaviour.name[0] for p in world.populations]

        for j, p in enumerate(world.populations):
            indices = np.argwhere(p.states)

            for i in range(len(indices)):
                offset_max = np.array([self.augment_x / 2, self.augment_y / 2])
                scale_factor = ((
                    np.array(self.basesize) + offset_max)
                                / np.array(self.basesize))
                scale_factor = scale_factor.reshape((2, 1))
                all_positions = (p.positions[:,indices[i][1]]
                                 * scale_factor[:, 0])
                current_color = self.sprites[indices[i][0]]
                renders = [
                    font.render(symb, True, current_color)
                    for symb in symbols]                            
                self.display_surf.blit(
                    renders[j % len(renders)],
                    [int(x) for x in all_positions])
        pygame.display.flip()
