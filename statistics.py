import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np



class Statistics:
    def __init__(self):
        self.x_values = []
        self.nb_susceptible = []
        self.nb_infected = []
        self.nb_recovered = []
        self.animation = None

    def initialize(self):
        self.x_values = []
        self.nb_susceptible = []
        self.nb_infected = []
        self.nb_recovered = []
        plt.ion()
        plt.tight_layout()
        plt.show()

    def step(self, time, world):
        self.x_values.append(time)
        self.nb_susceptible.append(np.sum(world.populations[0].states[0]))
        self.nb_infected.append(np.sum(world.populations[0].states[1]))
        self.nb_recovered.append(np.sum(world.populations[0].states[2]))

        self.plot()

    def plot(self):
        plt.cla()
        plt.plot(self.x_values, self.nb_susceptible)
        plt.plot(self.x_values, self.nb_infected)
        plt.plot(self.x_values, self.nb_recovered)
        plt.draw()
        plt.pause(0.0001)

