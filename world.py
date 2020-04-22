import math
import scipy.stats as sst
import numpy as np

import behaviours as beh

class Disease:
    def __init__(self):
        self.contagion_probability = 0.5
        self.contagion_distance = 20
        self.contagion_distance_square = self.contagion_distance**2
        self.recovery_time = 10*1000
        self.world = None
        self.last_update_time = None

    def initialize(self, world, time):
        self.world = world
        self.last_update_time = time

    def step(self, time):
        delta = time - self.last_update_time
        current_proba = 1 - pow(1 - self.contagion_probability, delta/1000.0)
        
        for p in self.world.populations:
            to_recovery = np.logical_and(p.states[1], p.change_state_time + self.recovery_time < time)
            p.states[1] = (1 - to_recovery)*p.states[1]
            p.states[2] = np.logical_or(to_recovery, p.states[2])

        self.interact(current_proba, time)
        self.last_update_time = time

    def interact(self, current_proba, time):
        for p in self.world.populations:
            potential_contamination = np.logical_and(p.states[1][:,None], p.states[0])
            diffs = p.positions[:,:,None]  - p.positions[:,None,:]
            distances = diffs ** 2
            distances = distances[0,:,:] + distances[1,:,:]
            potential_contamination = np.logical_and(distances < self.contagion_distance_square, potential_contamination)
            potential_contamination = np.logical_and(potential_contamination, np.random.random_sample((p.size, p.size)) < current_proba)

            contamination = np.sum(potential_contamination, axis=0) >= 1
            p.states[0] -= contamination
            p.states[1] += contamination
            p.change_state_time = contamination*time + (1 - contamination)*p.change_state_time
            
class World :
    def __init__(self, nb_actors = 100, weight_actors = np.array([1, 1]),
                 world_size = (500, 500), time = 0):
        self.area = [0, 0, world_size[0], world_size[1]]        
        self.disease = []
        self.meter_in_pixel = 1
        weight_actors = np.array(weight_actors)

        behaviours_func = [beh.SocialDistancing, beh.DummyPartier,
                           beh.RandomBehaviour, beh.Behaviour,
                           beh.PoolBehaviour]
        names = ['Social Distancing', 'Dummy', 'Random', 'Frozen', 'Pool']
        behaviours_func = [beh.Behaviour, beh.PoolBehaviour,
                           beh.RandomBehaviour, beh.SocialDistancing,
                           beh.DummyPartier]
        names = ['Frozen', 'Pool', 'Random', 'Social distancing', 'Dummy']
        names = dict(zip(behaviours_func, names))
        populations = [Population(world = self, time = 0,
                                  size = math.ceil(nb_actors * w))
                       for w in weight_actors]

        self.populations = []
        for i, population in enumerate(populations):
            beh_init = behaviours_func[i]
            population.set_behaviour(
                behaviour = beh_init(population = population, world = self,
                                    time = 0, name = names[beh_init]))
            if population.size != 0:
                population.states[1, 0] = 1
                self.populations.append(population)

    def step(self, time):
        for p in self.populations:
            p.step(time)

class Population :
    def __init__(self, world, time = 0, size = 1, name = 'DEFAULT'):

        ## Give compatible shapes
        area = np.array(world.area[2:]).reshape((2, 1))
        loc = np.zeros(shape = (1, size))
        self.positions = sst.uniform.rvs(loc = loc, scale = area)
        
        self.world = world
        self.change_state_time = np.array([time for _ in range(size)])
        self.behaviour = beh.Behaviour(population = self, world = world,
                                       time = time)
        self.size = size
        self.name = name

        self.states = np.zeros(shape = (3, self.size))
        self.states[0] = 1


    def set_behaviour(self, behaviour):
        self.behaviour = behaviour

    def step(self, time):
        self.behaviour.step(time)

