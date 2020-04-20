import pygame
from pygame.locals import *
import colorama
from colorama import Cursor

from graphics import Graphics
from world import World, Disease
from statistics import Statistics

class SIRSimulator:
    def __init__(self):
        self.graphics = Graphics()
        self.size = self.width, self.height = 500, 500
        self.running = False
        self.run_simulation = False
        self.clock = pygame.time.Clock()
        self.cursor_steps = 0
        self.stats_period = 500
        self.STAT_EVENT = pygame.USEREVENT+1
        self.compute_stats = False

        self.world = World()
        self.disease = Disease()
        self.statistics = Statistics()

        self.simulation_time_step_ms = 50
        self.simulation_time = 0

    def on_init(self):
        colorama.init()
        pygame.init()
        self.graphics.initialize(self.size)
        return True

    def initialize_simulation(self):
        self.simulation_time = 0
        self.world.initialize(200, self.size, 0)
        self.disease.initialize(self.world, 0)
        if self.compute_stats:
            self.statistics.initialize()
            pygame.time.set_timer(self.STAT_EVENT, self.stats_period)

    def on_loop(self):
        t0 = pygame.time.get_ticks()

        self.simulation_time += self.simulation_time_step_ms
        self.world.step(self.simulation_time)
        t1 = pygame.time.get_ticks()
        print("Time taken by world step " + str(t1 - t0) + "    ")
        self.cursor_steps += 1

        self.disease.step(self.simulation_time)
        t2 = pygame.time.get_ticks()
        print("Time taken by disease step " + str(t2 - t1) + "    ")
        self.cursor_steps += 1

    def on_render(self):
        self.graphics.render_world(self.world)

    def on_cleanup(self):
        pygame.quit()
        colorama.deinit()

    def on_event(self, event):
        time = pygame.time.get_ticks()
        if event.type == pygame.QUIT:
            self.running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                self.initialize_simulation()
                self.run_simulation = True

            if event.key == pygame.K_s:
                self.run_simulation = False

        if event.type == self.STAT_EVENT:
            self.statistics.step(time, self.world)
            

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
