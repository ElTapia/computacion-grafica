""" Models classes and objects"""

import glfw
import numpy as np
import grafica.transformations as tr
import grafica.scene_graph as sg
from shapes import *
import math


class Player():

    # Class that contains player model
    def __init__(self, size):
        self.pos = [0., -0.75] # Hinata's position
        self.vel = [0.4,0.4] # Speed
        self.model = None # Scene graph reference
        self.controller = None # Controller reference
        self.size = size # Size of the model
        self.radio = 0.1 # Ratio of collision
        self.is_infected = False # If Hinata is infected by a human

    def set_model(self, new_model):
        # Model node reference
        self.model = new_model

    def set_controller(self, new_controller):
        # Controller reference
        self.controller = new_controller

    def update(self, delta, stop=False):
        # Update Hinata´s position

        # [D] keyword is pressed, hinata moves to right
        if self.controller.is_d_pressed and self.pos[0] < 0.6:
            self.pos[0] += self.vel[0] * delta

        # [A] keyword is pressed, hinata moves to left
        if self.controller.is_a_pressed and self.pos[0] > -0.6:
            self.pos[0] -= self.vel[0] * delta

        # [W] keyword is pressed and is on screen, moves upwards
        if self.controller.is_w_pressed and self.pos[1] < 1:
            self.pos[1] += self.vel[1] * delta

        # [S] keyword is pressed and is on screen, moves downwards
        if self.controller.is_s_pressed and self.pos[1] > -1:
            self.pos[1] -= self.vel[1] * delta

        # Transformation due to actual position
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

        # Stop the controller
        if stop:
            self.controller.stop = True


    def collision_store(self, store):

        # Function that detects collision with the store
        # Distance from the store is less than sum or ratios => collision
        return (self.radio+store.radio)**2 > ((self.pos[0] - store.pos[0])**2 + (self.pos[1]-store.pos[1])**2)

    def collision_zombie(self, zombie):

        # Function that detects collision with a zombie
        # Distance from zombie is less than sum or ratios => collision
        return (self.radio+zombie.radio)**2 > ((self.pos[0] - zombie.pos[0])**2 + (self.pos[1]-zombie.pos[1])**2)
    
    def collision_human(self, human):

        # Function that detects collision with a human
        # Distance from human is less than sum or ratios => collision
        return (self.radio+human.radio)**2 > ((self.pos[0] - human.pos[0])**2 + (self.pos[1]-human.pos[1])**2)

    def infected(self, human):

        # If player touch an infected human => is infected
        if self.collision_human(human) and human.is_infected:
            self.is_infected = True
    
    def prob_become_zombie(self, p, lose=False):

        # Probabilities to become a zombie while player is infected
        if self.is_infected:
            return np.random.binomial(1, p)==1
        else:
            return False

def entity_movement(entity):
    # General function for entities (zombies or humans) move
    def pos_y():
        # Function to y coordinate
            return -np.sign(entity.y_ini)*entity.vel[1]*entity.t + entity.y_ini
        
    def pos_x():
        # Function to x coordinate
        return entity.direction*entity.vel[0]*np.sin(entity.t) + entity.x_ini

    # Stop the entities movement
    if entity.stop:
        entity.model.transform = tr.matmul([tr.translate(entity.pos[0], entity.pos[1], 0), tr.scale(entity.size, entity.size, 1)])

    else:
        # Update self time from entity and positions while is on screen
        entity.t += 0.001
        entity.pos[0] = pos_x()

        if entity.pos[0] > 0.55:
            entity.pos[0]=0.55
            entity.pos[1] = pos_y()
            entity.model.transform = tr.matmul([tr.translate(entity.pos[0], entity.pos[1], 0), tr.scale(entity.size, entity.size, 1)])

        elif entity.pos[0] < -0.55:
            entity.pos[0]=-0.55
            entity.pos[1] = pos_y()
            entity.model.transform = tr.matmul([tr.translate(entity.pos[0], entity.pos[1], 0), tr.scale(entity.size, entity.size, 1)])

        else:
            entity.pos[0] = pos_x()
            entity.pos[1] = pos_y()
            entity.model.transform = tr.matmul([tr.translate(entity.pos[0], entity.pos[1], 0), tr.scale(entity.size, entity.size, 1)])

class Zombie():
    # Class that contains zombies features
    def __init__(self, x_ini, y_ini, size):
        self.t = 0 # Self time controller for movement
        self.x_ini = x_ini # Init x coordinate position
        self.y_ini = y_ini # Init y coordinate position
        self.pos = [x_ini, y_ini] # Position on screen
        self.vel = np.random.uniform(0.4, 0.6, 2) # Random generated speed 
        self.direction = np.random.choice([-1, 1], 1) # Direction could be upwards or downwards
        self.radio = 0.03 # Ratio of collition
        self.size = size # Size of the model
        self.model = None # Scene graph reference
        self.stop = False # Entity could stop

    def set_model(self, new_model):
        # Model node reference
        self.model = new_model

    def update(self):
        # Update zombie position
        entity_movement(self)


class Human():
    # Class that contains humans features
    def __init__(self, x_ini, y_ini, size, p):
        self.t = 0 # Self time controller for movement
        self.x_ini = x_ini # Init x coordinate position
        self.y_ini = y_ini # Init y coordinate position
        self.pos = [x_ini, y_ini] # Position on screen
        self.vel = np.random.uniform(0.4, 0.6, 2) # Random generated speed 
        self.direction = np.random.choice([-1, 1], 1) # Direction could be upwards or downwards
        self.radio = 0.05 # Ratio of collition
        self.size = size # Size of the model
        self.model = None # Scene graph reference
        self.stop = False # Entity could stop
        self.is_infected = True # Human could be infected
        if np.random.binomial(1, p)==0:
            # Infection is random with probability p
            self.is_infected = False

    def set_model(self, new_model):
        # Model node reference
        self.model = new_model

    def update(self):
        # Update human position
        entity_movement(self)

    def collision_zombie(self, zombie):
        # Function that detects collision with a zombie
        # Distance from zombie is less than sum or ratios => collision
        return (self.radio+zombie.radio)**2 > ((self.pos[0] - zombie.pos[0])**2 + (self.pos[1]-zombie.pos[1])**2)

    def collision_human(self, human):
        # Function that detects collision with other human
        # Distance from human is less than sum or ratios => collision
        return (self.radio+human.radio)**2 > ((self.pos[0] - human.pos[0])**2 + (self.pos[1]-human.pos[1])**2)

    def infected(self, human):
        # Detect if a human touch and infected human
        if self.collision_human(human) and human.is_infected:
            # Update infection state
            self.is_infected = True

    def touch_zombie(self, zombie):
        # Detect if a human touch and infected human
        if self.collision_human(zombie):
            # Update infection state
            self.is_infected = True

class Store():
    # Class that contains store features
    def __init__(self, posx, posy, size):
        self.pos = [posx, posy]  # Position on screen
        self.radio = 0.13 # Ratio of collition
        self.size = size # Size of the model
        self.model = None # Scene graph reference

    def set_model(self, new_model):
        # Model node reference
        self.model = new_model

    def update(self):
        # Update store position
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1), tr.rotationZ(math.pi/2)])
