# coding=utf-8
"""Textures and transformations in 2D"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys, os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica.gpu_shape import GPUShape, SIZE_IN_BYTES
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
from PIL import Image

__author__ = "Daniel Calderon"
__license__ = "MIT"


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True

###################################################################################################
        # Agregamos dos nuevas variables a nuestro controlador
        self.actual_sprite = 1
        self.actual_key = 0
        self.x = 0
###################################################################################################


# global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    #if action != glfw.PRESS:
    #    return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

#############################################################################################
    # Agregamos dos nuevas teclas para interactuar
    elif key == glfw.KEY_RIGHT:
        controller.x += 0.05
        controller.actual_sprite = (controller.actual_sprite + 1)%10
        controller.actual_key = 0
    
    elif key == glfw.KEY_LEFT:
        controller.x -= 0.05
        controller.actual_sprite = (controller.actual_sprite - 1)%10
        controller.actual_key = 1
#############################################################################################

    else:
        print('Unknown key')


if __name__ == "__main__":
    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE,       glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(width, height, "Ejercicio 4: Caballero bajo la lluvia", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.SimpleTextureTransformShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

######################################################################################################

    # Creating shapes on GPU memory

    # Creamos una lista para guardar todas las gpu shapes necesarias
    gpus = []


    #* Definimos donde se encuentran las texturas
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    spritesDirectory = os.path.join(thisFolderPath, "Sprites")
    spritePath = os.path.join(spritesDirectory, "sprites.png")
    rainPath = os.path.join(spritesDirectory, "lluvia.png")
    backgroundPath = os.path.join(spritesDirectory, "fondo.jpeg")

    texture = es.textureSimpleSetup(
            spritePath, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

    #* Creamos una gpushape por cada frame de textura
    for i in range(10):
        gpuKnight = GPUShape().initBuffers()
        pipeline.setupVAO(gpuKnight)

        shapeKnight = bs.createTextureQuad(i/10,(i + 1)/10,0,1)

        gpuKnight.texture = texture

        gpuKnight.fillBuffers(shapeKnight.vertices, shapeKnight.indices, GL_STATIC_DRAW)

        gpus.append(gpuKnight)

    #* Creamos gpushape para la lluvia
    shapeRain = bs.createTextureBackground(3, 3, 10, 10)
    gpuRain = GPUShape().initBuffers()
    pipeline.setupVAO(gpuRain)

    gpuRain.texture = es.textureSimpleSetup(
        rainPath, GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    gpuRain.fillBuffers(shapeRain.vertices, shapeRain.indices, GL_STATIC_DRAW)


    #* Creamos gpushape para el fondo
    shapeBackground = bs.createTextureBackground(5, 2, 1, 1)
    gpuBackground = GPUShape().initBuffers()
    pipeline.setupVAO(gpuBackground)

    gpuBackground.texture = es.textureSimpleSetup(
        backgroundPath, GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    gpuBackground.fillBuffers(shapeBackground.vertices, shapeBackground.indices, GL_STATIC_DRAW)


#######################################################################################################    

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing the shapes
        
###############################################################
        # * Movimiento fondo

        t = glfw.get_time()

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(-((controller.x)*0.3)*0.5, 0, 0),
            tr.translate(0, 0, 0),
            tr.uniformScale(0.5)
        ]))

        pipeline.drawCall(gpuBackground)

################################################################
        # * Movimiento lluvia

        t = glfw.get_time()

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(-(controller.x%2.4)*0.8, -(t%6), 0),
            tr.translate(0, 3, 0),
            tr.uniformScale(0.5)
        ]))

        pipeline.drawCall(gpuRain)

        # * Repite caida lluvia
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(-(controller.x%2.4)*0.8, -((t+3)%6), 0),
            tr.translate(0, 3, 0),
            tr.uniformScale(0.5)
        ]))

        pipeline.drawCall(gpuRain)

        # * Repite lluvia mientras avanza

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(-((controller.x)%2.4)*0.8, -(t%6), 0),
            tr.translate(3, 3, 0),
            tr.uniformScale(0.5)
        ]))

        pipeline.drawCall(gpuRain)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(-((controller.x)%2.4)*0.8, -((t+3)%6), 0),
            tr.translate(3, 3, 0),
            tr.uniformScale(0.5)
        ]))

        pipeline.drawCall(gpuRain)
##############################################################################################################################

        # Le entregamos al vertex shader la matriz de transformaci??n
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.rotationY(controller.actual_key * np.pi),
            tr.translate(0, -0.7, 0),
            tr.uniformScale(0.5)
        ]))
#############################################

        # Dibujamos la figura
        pipeline.drawCall(gpus[controller.actual_sprite])

##############################################################################################################################

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuKnight.clear()
    gpuRain.clear()
    gpuBackground.clear()
    glfw.terminate()
