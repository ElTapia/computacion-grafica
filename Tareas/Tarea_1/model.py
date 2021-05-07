""" Models classes and objects"""

import glfw
import numpy as np
import grafica.transformations as tr
import grafica.scene_graph as sg
from shapes import *
import math


class Player():
    # Clase que contiene al modelo del player
    def __init__(self, size):
        self.pos = [0.58, -0.75] # Posicion hinata
        self.vel = [0.4,0.4] # Velocidad de desplazamiento
        self.model = None # Referencia al grafo de escena asociado
        self.controller = None # Referencia del controlador, para acceder a sus variables
        self.size = size # Escala a aplicar al nodo
        self.radio = 0.1 # distancia para realizar los calculos de colision
        self.is_infected = False

    def set_model(self, new_model):
        # Se obtiene una referencia a un nodo
        self.model = new_model

    def set_controller(self, new_controller):
        # Se obtiene la referencia al controller
        self.controller = new_controller

    def update(self, delta, stop=False):
        # Se actualiza la posicion de hinata

        # Si detecta la tecla [D] presionada hinata se mueve hacia la derecha
        if self.controller.is_d_pressed and self.pos[0] < 0.6:
            self.pos[0] += self.vel[0] * delta

        # Si detecta la tecla [A] presionada hinata se mueve hacia la izquierda
        if self.controller.is_a_pressed and self.pos[0] > -0.6:
            self.pos[0] -= self.vel[0] * delta

        # Si detecta la tecla [W] presionada y no se ha salido de la pantalla, se mueve hacia arriba
        if self.controller.is_w_pressed and self.pos[1] < 1:
            self.pos[1] += self.vel[1] * delta

        # Si detecta la tecla [S] presionada y no se ha salido de la pantalla, se mueve hacia abajo
        if self.controller.is_s_pressed and self.pos[1] > -1:
            self.pos[1] -= self.vel[1] * delta

        # Se le aplica la transformacion de traslado segun la posicion actual
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

        if stop:
            self.controller.stop = True


    def collision_store(self, store):

        # Funcion para detectar las colisiones con store
        # si la distancia a la tienda es menor que la suma de los radios ha ocurrido en la colision
        return (self.radio+store.radio)**2 > ((self.pos[0] - store.pos[0])**2 + (self.pos[1]-store.pos[1])**2)

    def collision_zombie(self, zombie):

        # si la distancia al zombie es menor que la suma de los radios ha ocurrido en la colision
        return (self.radio+zombie.radio)**2 > ((self.pos[0] - zombie.pos[0])**2 + (self.pos[1]-zombie.pos[1])**2)
    
    def collision_human(self, human):
        # si la distancia al humano es menor que la suma de los radios ha ocurrido en la colision
        return (self.radio+human.radio)**2 > ((self.pos[0] - human.pos[0])**2 + (self.pos[1]-human.pos[1])**2)

    def infected(self, human):
        if self.collision_human(human) and human.is_infected:
            self.is_infected = True
    
    def prob_become_zombie(self, p, lose=False):
        if self.is_infected:
            return np.random.binomial(1, p)==0
        else:
            return False

class Zombie():
    # Clase para contener las caracteristicas de un objeto que representa un zombie 
    def __init__(self, x_ini, y_ini, size):
        self.t = 0
        self.x_ini = x_ini # x de partida
        self.y_ini = y_ini # y de partida
        self.pos = [x_ini, y_ini]
        self.vel = np.random.uniform(0.1, 0.8, 2)
        self.direction = np.random.choice([-1, 1], 1)
        self.radio = 0.03
        self.size = size
        self.model = None
        self.stop=False
    
    def set_model(self, new_model):
        self.model = new_model

    def update(self):
        def pos_y():
            return -np.sign(self.y_ini)*self.vel[1]*self.t + self.y_ini
        
        def pos_x():
            return self.direction*self.vel[0]*np.sin(self.t) + self.x_ini

        # Se posiciona el nodo referenciado
        if self.stop:
            self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

        else:
            self.t += 0.001
            self.pos[0] = pos_x()

            if self.pos[0] > 0.6:
                self.pos[0]=0.6
                self.pos[1] = pos_y()
                self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

            elif self.pos[0] < -0.6:
                self.pos[0]=-0.6
                self.pos[1] = pos_y()
                self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

            else:
                self.pos[0] = pos_x()
                self.pos[1] = pos_y()
                self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])


class Human():
    # Clase para contener las caracteristicas de un objeto que representa un zombie 
    def __init__(self, x_ini, y_ini, size, p, is_zombie=False):
        self.t = 0
        self.x_ini = x_ini
        self.y_ini = y_ini
        self.pos = [x_ini, y_ini]
        self.vel = np.random.uniform(0.4, 0.5, 2)
        self.direction = np.random.choice([-1, 1], 1)
        self.radio = 0.05
        self.size = size
        self.model = None
        self.stop=False
        self.is_infected = True
        if np.random.binomial(1, p)==0:
            self.is_infected = False

    def set_model(self, new_model):
        self.model = new_model

    def update(self):
        def pos_y():
            return -np.sign(self.y_ini)*self.vel[1]*self.t + self.y_ini
    
        def pos_x():
            return self.direction*self.vel[0]*np.sin(self.t) + self.x_ini

        if self.stop:
            self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

        else:
            # Se posiciona el nodo referenciado
            self.t += 0.001
            self.pos[0]=pos_x()

            if self.pos[0] > 0.6:
                self.pos[0]=0.6
                self.pos[1]=pos_y()
                self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

            elif self.pos[0] < -0.6:
                self.pos[0]=-0.6
                self.pos[1]=pos_y()
                self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

            else:
                self.pos[0]=pos_x()
                self.pos[1]=pos_y()
                self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])

    def collision_zombie(self, zombie):

        # si la distancia al zombie es menor que la suma de los radios ha ocurrido en la colision
        return (self.radio+zombie.radio)**2 > ((self.pos[0] - zombie.pos[0])**2 + (self.pos[1]-zombie.pos[1])**2)

    def collision_human(self, human):
        # si la distancia al zombie es menor que la suma de los radios ha ocurrido en la colision
        return (self.radio+human.radio)**2 > ((self.pos[0] - human.pos[0])**2 + (self.pos[1]-human.pos[1])**2)

    def infected(self, human):
        if self.collision_human(human) and human.is_infected:
            self.is_infected = True

class Store():
    # Clase para contener las caracteristicas de un objeto que representa un zombie 
    def __init__(self, posx, posy, size):
        self.pos = [posx, posy]
        self.radio = 0.1
        self.size = size
        self.model = None
    
    def set_model(self, new_model):
        self.model = new_model

    def update(self):
        # Se posiciona el nodo referenciado
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])
