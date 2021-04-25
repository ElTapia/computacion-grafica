""" Clases y objetos correspondiente al modelo"""

import glfw
import numpy as np
import grafica.transformations as tr
import grafica.scene_graph as sg

class Player():
    # Clase que contiene al modelo del player / auro
    def __init__(self, size):
        self.pos = [-2, 0, 2, -0.65] # Posicion escenarios
        self.vel = [1,0.8] # Velocidad de desplazamiento
        self.model = None # Referencia al grafo de escena asociado
        self.controller = None # Referencia del controlador, para acceder a sus variables
        self.size = size # Escala a aplicar al nodo 
        self.radio = 0.1 # distancia para realiozar los calculos de colision

    def set_model(self, new_model):
        # Se obtiene una referencia a dos nodo
        self.model = new_model

    def set_controller(self, new_controller):
        # Se obtiene la referencia al controller
        self.controller = new_controller

    def update(self, delta):
        # Se actualiza la posicion del auto y fondo

        # Si detecta la tecla [D] presionada fondo se mueve hacia la izquierda
        #if self.controller.is_d_pressed:
        #    self.pos[0] -= self.vel[0] * delta
        #    self.pos[1] -= self.vel[0] * delta
        #    self.pos[2] -= self.vel[0] * delta
        # Si detecta la tecla [A] presionada fondo se mueve hacia la derecha
        #if self.controller.is_a_pressed:
        #    self.pos[0] += self.vel[0] * delta
        #    self.pos[1] += self.vel[0] * delta
        #    self.pos[2] += self.vel[0] * delta
        # Si detecta la tecla [W] presionada y no se ha salido de la pista se mueve hacia arriba
        if self.controller.is_w_pressed and self.pos[3] < -0.45:
            self.pos[3] += self.vel[1] * delta
        # Si detecta la tecla [S] presionada y no se ha salido de la pista se mueve hacia abajo
        if self.controller.is_s_pressed and self.pos[3] > -0.8:
            self.pos[3] -= self.vel[1] * delta

        # Se le aplica la transformacion de traslado segun la posicion actual
        car = sg.findNode(self.model, "car")
        backgrounds = sg.findNode(self.model, "backgrounds")

        leftBackground = sg.findNode(backgrounds, "left background")
        centerBackground = sg.findNode(backgrounds, "center background")
        rightBackground = sg.findNode(backgrounds, "right background")

        pos_inicial = 3.5

        if self.pos[0] < -3:
            self.pos[0] = pos_inicial

        if self.pos[1] < -3:
            self.pos[1] = pos_inicial

        if self.pos[2] < -3:
            self.pos[2] = pos_inicial

        car.transform = tr.matmul([tr.translate(-0.5, self.pos[3], 0), tr.scale(self.size*0.3, self.size*0.3, 1)])
        leftBackground.transform = tr.matmul([tr.translate(self.pos[0], 0, 0), tr.scale(self.size, self.size, 1)])
        centerBackground.transform = tr.matmul([tr.translate(self.pos[1], 0, 0), tr.scale(self.size, self.size, 1)])
        rightBackground.transform = tr.matmul([tr.translate(self.pos[2], 0, 0), tr.scale(self.size, self.size, 1)])

    def collision(self, cargas):
        # Funcion para detectar las colisiones con las cargas

        # Se recorren las cargas 
        for carga in cargas:
            # si la distancia a la carga es menor que la suma de los radios ha ocurrido en la colision
            if (self.radio+carga.radio)**2 > ((-0.5 - carga.pos[0])**2 + (self.pos[3]-carga.pos[1])**2):
                print("CHOQUE")
                return
        
class Carga():
    # Clase para contener las caracteristicas de un objeto que representa una carga 
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

    
