import numpy as np

class Behaviour:
    def __init__(self, population, world, time, name = 'DEFAULT'):
        self.population = population
        self.world = world
        self.speed = np.zeros(population.positions.shape)        
        self.last_update_time = time
        self.name = name        

    def bounce(self):
        left_bounce = self.population.positions[0] < self.world.area[0]
        self.speed[0] *= 1 - 2 * left_bounce

        top_bounce = self.population.positions[1] < self.world.area[1]
        self.speed[1] *= 1 - 2 * top_bounce

        right_bounce = self.population.positions[0] >= self.world.area[2]
        self.speed[0] *= 1 - 2 * right_bounce

        bottom_bounce = self.population.positions[1] >= self.world.area[3]
        self.speed[1] *= 1 - 2 * bottom_bounce    

    def colision_detection(self):
        left_oob = self.population.positions[0] < self.world.area[0]
        self.population.positions[0] = left_oob*self.world.area[0] + (1 - left_oob)*self.population.positions[0] 

        top_oob = self.population.positions[1] < self.world.area[1]
        self.population.positions[1] = top_oob*self.world.area[1] + (1 - top_oob)*self.population.positions[1] 

        right_oob = self.population.positions[0] >= self.world.area[2]
        self.population.positions[0] = right_oob*self.world.area[2] + (1 - right_oob)*self.population.positions[0] 

        bottom_oob = self.population.positions[1] >= self.world.area[3]
        self.population.positions[1] = bottom_oob*self.world.area[3] + (1 - bottom_oob)*self.population.positions[1] 

    def step(self, time):
        delta = time - self.last_update_time
        self.population.positions += self.speed * delta * 0.001        
        self.bounce()
        self.colision_detection()
        self.last_update_time = time

class PoolBehaviour(Behaviour):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_speed = 20
        self.max_acceleration = 40
        acceleration_polar_coords = np.array([[self.max_acceleration], [2*np.pi]]) * np.random.random_sample((2,self.population.size))
        self.speed = acceleration_polar_coords[0] * [np.cos(acceleration_polar_coords[1]), np.sin(acceleration_polar_coords[1])]        
        
        
class RandomBehaviour(Behaviour):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_speed = 20
        self.max_acceleration = 40
        acceleration_polar_coords = np.array([[self.max_acceleration], [2*np.pi]]) * np.random.random_sample((2,self.population.size))
        self.speed = acceleration_polar_coords[0] * [np.cos(acceleration_polar_coords[1]), np.sin(acceleration_polar_coords[1])]

    def step(self, time):
        delta = time - self.last_update_time
        acceleration_polar_coords = np.array([[self.max_acceleration * delta * 0.001], [2*np.pi]]) * np.random.random_sample((2,self.population.size))
        self.speed += acceleration_polar_coords[0] * [np.cos(acceleration_polar_coords[1]), np.sin(acceleration_polar_coords[1])]

        self.speed = np.clip(self.speed, -self.max_speed, self.max_speed)
        super().step(time = time)

class SocialDistancing(Behaviour):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_speed = 20
        self.max_acceleration = 40        
        self.repulsion_distance = 20
        self.repulstion_force = 5
        self.speed_decay = 0.5

    def step(self, time):
        delta = time - self.last_update_time
        diffs = self.world.populations[0].positions[:,:,None]  - self.world.populations[0].positions[:,None,:]
        distance = np.linalg.norm(diffs, axis = 0)

        repulsion_direction = -np.sum(np.clip(self.repulsion_distance - distance, 0, self.repulstion_force) * diffs / (distance + 0.001), axis=1)

        current_decay = pow(self.speed_decay, delta/1000)
        self.speed *= current_decay
        self.speed += repulsion_direction

        self.speed = np.clip(self.speed, -self.max_speed, self.max_speed)
        self.population.positions += self.speed * delta * 0.001

        super().step(time = time)

class DummyPartier(SocialDistancing):
    def __init__(self, attraction_force = 5, attraction_range = 100,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repulsion_distance = attraction_range
        self.repulstion_force = - attraction_force
        self.speed_decay = 0.5
        self.max_acceleration = 20
