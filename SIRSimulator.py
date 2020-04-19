import pygame
from pygame.locals import *
import colorama
from colorama import Cursor

from graphics import Graphics
from world import World, Disease

class SIRSimulator:
    def __init__(self):
        self.graphics = Graphics()
        self.size = self.width, self.height = 500, 500
        self.running = False
        self.run_simulation = False
        self.clock = pygame.time.Clock()
        self.cursor_steps = 0

        self.world = World()
        self.disease = Disease()

    def on_init(self):
        colorama.init()
        pygame.init()
        self.graphics.initialize(self.size)
        return True

    def initialize_simulation(self):
        time = self.clock.get_time()
        self.world.initialize(100, self.size, time)
        self.disease.initialize(self.world, time)

    def on_loop(self):
        t0 = pygame.time.get_ticks()

        self.world.step(t0)
        t1 = pygame.time.get_ticks()
        print("Time taken by world step " + str(t1 - t0) + "    ")
        self.cursor_steps += 1

        self.disease.step(t0)
        t2 = pygame.time.get_ticks()
        print("Time taken by disease step " + str(t2 - t1) + "    ")
        self.cursor_steps += 1

    def on_render(self):
        self.graphics.render_world(self.world)

    def on_cleanup(self):
        pygame.quit()
        colorama.deinit()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                self.initialize_simulation()
                self.run_simulation = True

    def on_execute(self):
        self.running = self.on_init()

        while(self.running):
            self.cursor_steps = 0
            for event in pygame.event.get():
                self.on_event(event)    
            if (self.run_simulation):
                self.on_loop()
            t0 = pygame.time.get_ticks()
            self.on_render()
            t1 = pygame.time.get_ticks()
            print("Time taken by render step " + str(t1 - t0) + "    ")
            self.cursor_steps += 1
            print("fps : " + str(self.clock.get_fps()) + "    ")
            self.cursor_steps += 1
            print(Cursor.UP(self.cursor_steps + 1))

            self.clock.tick(60)
        self.on_cleanup()

if __name__ == "__main__":
    SIRSim = SIRSimulator()
    SIRSim.on_execute()
