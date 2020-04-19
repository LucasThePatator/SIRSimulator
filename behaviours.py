import numpy as np

class Behaviour:
    def __init__(self):
        self.actor = None
        self.world = None
        self.last_update_time = None

    def initialize(self, actor, world, time):
        self.actor = actor
        self.world = world
        self.last_update_time = time

    def step(self, time):
        pass

    def colision_detection(self):
        if self.actor.position[0] < self.world.area[0]:
            self.actor.position[0] = 0

        if self.actor.position[1] < self.world.area[1]:
            self.actor.position[1] = 0

        if self.actor.position[0] >= self.world.area[2]:
            self.actor.position[0] = self.world.area[2] - 1

        if self.actor.position[1] >= self.world.area[3]:
            self.actor.position[1] = self.world.area[3] - 1
        
class RandomBehaviour(Behaviour):
    def __init__(self):
        super(RandomBehaviour, self).__init__()
        self.speed = self.x_speed, self.y_speed = 0,0
        self.max_speed = 50
        self.acceleration = self.max_speed * 20

        radius = self.max_speed * np.random.random_sample()
        angle = 2*np.pi * np.random.random_sample()
        x, y = radius * np.cos(angle), radius * np.sin(angle)
        self.x_speed = x
        self.y_speed = y

    def bounce(self):
        if self.actor.position[0] < self.world.area[0]:
            self.x_speed *= -1

        if self.actor.position[1] < self.world.area[1]:
            self.y_speed *= -1

        if self.actor.position[0] >= self.world.area[2]:
            self.x_speed *= -1

        if self.actor.position[1] >= self.world.area[3]:
            self.y_speed *= -1

    def step(self, time):
        delta = time - self.last_update_time
        rands = np.random.random(2)
        radius = self.acceleration * delta * rands[0] * 0.001
        angle = 2 * np.pi * rands[1]
        x, y = radius * np.cos(angle), radius * np.sin(angle)
        self.x_speed += x
        self.y_speed += y

        self.x_speed = np.clip(self.x_speed, -self.max_speed, self.max_speed)
        self.y_speed = np.clip(self.y_speed, -self.max_speed, self.max_speed)

        self.actor.position[0] += self.x_speed * delta * 0.001
        self.actor.position[1] += self.y_speed * delta * 0.001

        self.bounce()
        self.colision_detection()
        self.last_update_time = time
