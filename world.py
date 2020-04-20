import behaviours as beh
import numpy as np

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
    def __init__(self):
        self.populations = []
        self.disease = []
        self.meter_in_pixel = 1
        self.area = None
        self.last_update_time = None

    def initialize(self, behaviors = [beh.SocialDistancing(),
                                      beh.DummyPartier(),
                                      beh.RandomBehaviour()],
                   nb_actors = 100, world_size = (500, 500), time = 0):
        print(world_size)
        self.area = [0, 0, world_size[0], world_size[1]] #left, top, width, height
        self.populations = []
        for behaviour in behaviors:
            self.populations.append(
                Population(behaviour, self))
            self.populations[-1].initialize(nb_actors, time)
            self.populations[-1].states[0, 0] = 0
            self.populations[-1].states[1, 0] = 1
        self.last_update_time = time

    def step(self, time):
        for p in self.populations:
            p.step(time)

class Population :
    def __init__(self, behaviour, world):
        self.world = world
        self.positions = []
        self.states = []
        self.change_state_time = []
        self.behaviour = behaviour
        self.size = None
        
    def initialize(self, size, time):
        self.size = size
        self.positions = np.random.random_sample((2, size)) * np.array(self.world.area[2:-1])
        self.states = np.zeros((3, self.size))
        self.states[0] = 1
        self.change_state_time = np.array([time for _ in range(size)])
        self.behaviour.initialize(self, self.world, time)

    def step(self, time):
        self.behaviour.step(time)

