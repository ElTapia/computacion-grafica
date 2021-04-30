""" Clases y objetos correspondiente al modelo"""

import glfw
import numpy as np
import grafica.transformations as tr
import grafica.scene_graph as sg

#TODO: Definir player para hinata
#TODO: Definir modelo para zombie
#TODO: Definir modelo para humano

class Player():
    # Clase que contiene al modelo del player
    def __init__(self, size):
        self.pos = [0.58, -0.75] # Posicion hinata
        self.vel = [1,1] # Velocidad de desplazamiento
        self.model = None # Referencia al grafo de escena asociado
        self.controller = None # Referencia del controlador, para acceder a sus variables
        self.size = size # Escala a aplicar al nodo
        self.radio = 0.1 # distancia para realizar los calculos de colision

    def set_model(self, new_model):
        # Se obtiene una referencia a un nodo
        self.model = new_model

    def set_controller(self, new_controller):
        # Se obtiene la referencia al controller
        self.controller = new_controller

    def update(self, delta):
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
    
    def stop(self):
        # Deja quieto al personaje en su posición actual
        self.pos = [0.58, -0.75]

    def collision_store(self, store):

        # Funcion para detectar las colisiones con store
        # si la distancia a la tienda es menor que la suma de los radios ha ocurrido en la colision
        return (self.radio+store.radio)**2 > ((self.pos[0] - store.pos[0])**2 + (self.pos[1]-store.pos[1])**2)

    def collision_zombie(self, zombies):

        # Se recorren los zombies
        for zombie in zombies:
            # si la distancia al zombie es menor que la suma de los radios ha ocurrido en la colision
            return (self.radio+zombie.radio)**2 > ((self.pos[0] - zombie.pos[0])**2 + (self.pos[1]-zombie.pos[1])**2)
    
    def collision_human(self, humans):

        for human in humans:
            # si la distancia al humano es menor que la suma de los radios ha ocurrido en la colision
            return (self.radio+human.radio)**2 > ((self.pos[0] - human.pos[0])**2 + (self.pos[1]-human.pos[1])**2)
        
class Zombie():
    # Clase para contener las caracteristicas de un objeto que representa un zombie 
    def __init__(self, posx, posy, size):
        self.pos = [posx, posy]
        self.radio = 0.05
        self.size = size
        self.model = None
    
    def set_model(self, new_model):
        self.model = new_model

    def update(self):
        # Se posiciona el nodo referenciado
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])


class Human():
    # Clase para contener las caracteristicas de un objeto que representa un zombie 
    def __init__(self, posx, posy, size):
        self.pos = [posx, posy]
        self.radio = 0.05
        self.size = size
        self.model = None
    
    def set_model(self, new_model):
        self.model = new_model

    def update(self):
        # Se posiciona el nodo referenciado
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])


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

