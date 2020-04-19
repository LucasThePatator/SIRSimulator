import numpy as np
from utils import clip

class Behaviour:
    def __init__(self):
        self.population = None
        self.world = None
        self.last_update_time = None

    def initialize(self, population, world, time):
        self.population = population
        self.world = world
        self.last_update_time = time

    def step(self, time):
        pass

    def colision_detection(self):
        left_oob = self.population.positions[0] < self.world.area[0]
        self.population.positions[0] = left_oob*self.world.area[0] + (1 - left_oob)*self.population.positions[0] 

        top_oob = self.population.positions[1] < self.world.area[1]
        self.population.positions[1] = top_oob*self.world.area[1] + (1 - top_oob)*self.population.positions[1] 

        right_oob = self.population.positions[0] >= self.world.area[2]
        self.population.positions[0] = right_oob*self.world.area[2] + (1 - right_oob)*self.population.positions[0] 

        bottom_oob = self.population.positions[1] >= self.world.area[3]
        self.population.positions[1] = bottom_oob*self.world.area[3] + (1 - bottom_oob)*self.population.positions[1] 

class RandomBehaviour(Behaviour):
    def __init__(self):
        super(RandomBehaviour, self).__init__()
        self.speed = []
        self.max_speed = 25
        self.max_acceleration = 500
    def initialize(self, population, world, time):
        super(RandomBehaviour, self).initialize(population, world, time)
        self.speed = np.ones((2,self.population.size))*10
        self.last_update_time = time

    def bounce(self):
        left_bounce = self.population.positions[0] < self.world.area[0]
        self.speed[0] *= 1 - 2 * left_bounce

        top_bounce = self.population.positions[1] < self.world.area[1]
        self.speed[1] *= 1 - 2 * top_bounce

        right_bounce = self.population.positions[0] >= self.world.area[2]
        self.speed[0] *= 1 - 2 * right_bounce

        bottom_bounce = self.population.positions[1] >= self.world.area[3]
        self.speed[1] *= 1 - 2 * bottom_bounce

    def step(self, time):
        delta = time - self.last_update_time
        acceleration_polar_coords = np.array([[self.max_acceleration * delta * 0.001], [2*np.pi]]) * np.random.random_sample((2,self.population.size))
        self.speed += acceleration_polar_coords[0] * [np.cos(acceleration_polar_coords[1]), np.sin(acceleration_polar_coords[1])]

        self.speed = np.clip(self.speed, -self.max_speed, self.max_speed)
        self.population.positions += self.speed * delta * 0.001

        self.bounce()
        self.colision_detection()
        self.last_update_time = time
