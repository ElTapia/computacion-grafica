import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import random
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.performance_monitor as pm
import shapes_3D as s3d
import grafica.scene_graph as sg


# Convenience function to ease initialization
def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_DYNAMIC_DRAW)
    return gpuShape


class Circle:

    def __init__(self, pipeline, position, velocity, r, g, b, CIRCLE_DISCRETIZATION, RADIUS):
        shape = s3d.createColorNormalSphere(CIRCLE_DISCRETIZATION, r, g, b)

        # addapting the size of the circle's vertices to have a circle
        # with the desired radius

        #bs.scaleVertices(shape, 6, (scaleFactor, scaleFactor, scaleFactor))
        self.pipeline = pipeline
        self.gpuShape = createGPUShape(self.pipeline, shape)
        self.position = position
        self.radius   = RADIUS
        self.velocity = velocity

    def action(self, gravityAceleration, deltaTime):
        # Euler integration
        self.velocity += deltaTime * gravityAceleration
        self.position += self.velocity * deltaTime

    def draw(self, transformName):
        scaleFactor = 2 * self.radius
        glUniformMatrix4fv(glGetUniformLocation(self.pipeline.shaderProgram, transformName), 1, GL_TRUE,
            tr.matmul([tr.translate(self.position[0], self.position[1], 0.0), tr.uniformScale(scaleFactor)])
        )
        self.pipeline.drawCall(self.gpuShape)


# Clase para manejar una camara que se mueve en coordenadas polares
class PolarCamera:
    def __init__(self):
        self.center = np.array([0.0, 0.0, -0.5]) # centro de movimiento de la camara y donde mira la camara
        self.theta = 0                           # coordenada theta, angulo de la camara
        self.rho = 5                             # coordenada rho, distancia al centro de la camara
        self.eye = np.array([0.0, 0.0, 0.0])     # posicion de la camara
        self.height = 2.0                        # altura fija de la camara
        self.up = np.array([0, 0, 1])            # vector up
        self.viewMatrix = None                   # Matriz de vista
    
    # Añadir ángulo a la coordenada theta
    def set_theta(self, delta):
        self.theta = (self.theta + delta) % (np.pi * 2)

    # Añadir distancia a la coordenada rho, sin dejar que sea menor o igual a 0
    def set_rho(self, delta):
        if ((self.rho + delta) > 0.1):
            self.rho += delta

    def get_eye(self):
        return self.eye

    # Actualizar la matriz de vista
    def update_view(self):
        # Se calcula la posición de la camara con coordenadas poleras relativas al centro
        self.eye[0] = self.rho * np.sin(self.theta) + self.center[0]
        self.eye[1] = self.rho * np.cos(self.theta) + self.center[1]
        self.eye[2] = self.height + self.center[2]

        # Se genera la matriz de vista
        viewMatrix = tr.lookAt(
            self.eye,
            self.center,
            self.up
        )
        return viewMatrix


def create_scene(pipeline, width, height, radius):
    green_cube = bs.createColorCube(0.1, 0.7, 0.3)
    gpu_cube = createGPUShape(pipeline, green_cube)

    green_cube_node = sg.SceneGraphNode("cubo verde")
    green_cube_node.childs += [gpu_cube]

    scaled_cube = sg.SceneGraphNode("cubo escalado")
    scaled_cube.transform = tr.matmul([tr.translate(0, 0, -radius-0.25), tr.scale(width, height, 0.5)])
    scaled_cube.childs += [green_cube_node]

    scene = sg.SceneGraphNode("Escena")
    scene.childs += [scaled_cube]

    return scene