import contextlib
with contextlib.redirect_stdout(None): # Remove pygame prints during import
    import pygame
    from pygame.locals import *
import colorama
from colorama import Cursor
import argparse as arg

from graphics import Graphics
from world import World, Disease
from statistics import Statistics

class SIRSimulator:
    def __init__(self, pop_size = 100, world_size = (500, 500)):
        self.graphics = Graphics()
        self.size = self.width, self.height = world_size
        self.running = False
        self.run_simulation = False
        self.clock = pygame.time.Clock()
        self.cursor_steps = 0
        self.stats_period = 500
        self.STAT_EVENT = pygame.USEREVENT+1
        self.compute_stats = False
        self.pop_size = pop_size
        self.world_size = world_size
        self.weight_actors = [1, 1, 1, 1, 1]

        self.world = World(nb_actors = pop_size,
                           weight_actors = self.weight_actors,
                           world_size = self.world_size,
                           time = 0)
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
        self.world= World(nb_actors = self.pop_size,
                          weight_actors = self.weight_actors,
                          world_size = self.size,
                          time = 0)
        self.disease.initialize(self.world, 0)
        if self.compute_stats:
            self.statistics.initialize()
            pygame.time.set_timer(self.STAT_EVENT, self.stats_period)

    def on_loop(self):
        t0 = pygame.time.get_ticks()

        self.simulation_time += self.simulation_time_step_ms
        self.world.step(self.simulation_time)
        t1 = pygame.time.get_ticks()
        #print("Time taken by world step " + str(t1 - t0) + "    ")
        self.cursor_steps += 1

        self.disease.step(self.simulation_time)
        t2 = pygame.time.get_ticks()
        #print("Time taken by disease step " + str(t2 - t1) + "    ")
        self.cursor_steps += 1

    def on_render(self):
        self.graphics.render_world(self.world)

    def on_cleanup(self):
        pygame.quit()
        colorama.deinit()

    def on_event(self, event):
        time = pygame.time.get_ticks()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                self.initialize_simulation()
                self.run_simulation = True

            if event.key == pygame.K_s:
                self.run_simulation = not self.run_simulation

            if event.key == pygame.K_ESCAPE:
                self.running = False

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
            #print("Time taken by render step " + str(t1 - t0) + "    ")
            self.cursor_steps += 1
            #print("fps : " + str(self.clock.get_fps()) + "    ")
            self.cursor_steps += 1
            #print(Cursor.UP(self.cursor_steps + 1))
            self.clock.tick(60)
        self.on_cleanup()

def format_args(args):
    if len(args.world_size) == 0:
        args.world_size = [500, 500]
    elif len(args.world_size) == 1:
        args.world_size = [args.world_size[0], args.world_size[0]]
    else:
        args.world_size = [args.world_size[0], args.world_size[1]]
        
if __name__ == "__main__":
    parser = arg.ArgumentParser(description = '',
                                epilog = '',
                                add_help = True)
    parser.add_argument('--pop_size', dest = 'pop_size', nargs = '?',
                        action = 'store', type = int, required = False,
                        default = 100,
                        help = ('The total number of individuals in the '
                                + 'populations'))
    parser.add_argument('--world_size', dest = 'world_size', nargs = '*',
                        action = 'store', type = int, required = False,
                        default = [500, 500],
                        help = ('The world size'))

    args = parser.parse_args()
    format_args(args)
    SIRSim = SIRSimulator(pop_size = args.pop_size,
                          world_size = tuple(args.world_size))
    SIRSim.on_execute()
