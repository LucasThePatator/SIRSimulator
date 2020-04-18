import behaviours
import numpy as np

class Disease:
    def __init__(self):
        self.contagion_probability = 0.2
        self.contagion_distance = 20
        self.recovery_time = 20*1000
        self.world = None

    def initialize(self, world):
        self.world = world

    def step(self, time):
        nb_actors = len(self.world.actors)
        rands = np.random.random(nb_actors*(nb_actors+1))

        for a in self.world.actors:  
             if a.state == 'I' and a.change_state_time + self.recovery_time < time:
                 a.state = 'R'
                 a.change_state_time = time

        for i in range(nb_actors - 1):
            for j in range(i+1, nb_actors):
                self.interact(self.world.actors[i], self.world.actors[j], rands[i + nb_actors*j], time)

    def interact(self, actor1, actor2, random_number, time):
        if (actor1.state == 'S' and actor2.state == 'I') or (actor1.state == 'I' and actor2.state == 'S') :
            if random_number < self.contagion_probability:
                if np.linalg.norm(np.array(actor1.position)-np.array(actor2.position)) < self.contagion_distance:   
                    if(actor1.state == 'S'):
                        actor1.change_state_time = time
                        actor1.state = 'I'

                    if(actor2.state == 'S'):
                        actor2.change_state_time = time
                        actor2.state = 'I'
                    


class World :
    def __init__(self):
        self.actors = []
        self.disease = []
        self.meter_in_pixel = 1
        self.area = None

    def initialize(self, nb_actors, world_size, time):
        self.area = [0, 0, world_size[0], world_size[1]] #left, top, width, height

        self.actors = []
        for i in range(nb_actors):
            position = [np.random.randint(world_size[0]), np.random.randint(world_size[1])]
            self.actors.append(Actor(position, 'S', behaviours.RandomBehaviour(), self, i))
            self.actors[-1].initialize(time)

        self.actors.append(Actor(position, 'I', behaviours.RandomBehaviour(), self, i))
        self.actors[-1].initialize(time)

    def step(self, time):
        for a in self.actors:
            a.step(time)

class Actor :
    def __init__(self, initial_position, initial_state, behaviour, world, ID):
        self.world = world
        self.position = initial_position
        self.state = initial_state
        self.behaviour = behaviour
        self.ID = ID
        self.change_state_time = None

    def initialize(self, time):
        self.change_state_time = time
        self.behaviour.initialize(self, self.world)

    def step(self, time):
        self.behaviour.step(time)

