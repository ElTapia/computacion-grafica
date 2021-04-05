# coding=utf-8
"""Ejercicio 3: Planeta tierra orbitando alrededor del sol y luna alrededor de la tierra

Extra: La tierra y la luna también tienen movimiento de rotación.
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import planet_shape as ps
import easy_shaders_Windows as es
import transformations as tr
import math

__author__ = "Daniel Calderon"
__license__ = "MIT"


# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    else:
        print('Unknown key')


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Ejercicio 3: Movimiento órbitas Tierra y luna", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Creating shapes on GPU memory
    # * Crea shape de la tierra
    shapeTierra = ps.createPlanet(100, [0, 0, 1])
    gpuTierra = es.GPUShape().initBuffers()
    gpuTierra.fillBuffers(shapeTierra.vertices, shapeTierra.indices, GL_STATIC_DRAW)

    # * Crea shape del sol
    shapeSol = ps.createPlanet(100, [1, 1, 0])
    gpuSol = es.GPUShape().initBuffers()
    gpuSol.fillBuffers(shapeSol.vertices, shapeSol.indices, GL_STATIC_DRAW)

    # * Crea shape de la luna
    shapeLuna = ps.createPlanet(100, [0.5, 0.5, 0.5])
    gpuLuna = es.GPUShape().initBuffers()
    gpuLuna.fillBuffers(shapeLuna.vertices, shapeLuna.indices, GL_STATIC_DRAW)

    glBindVertexArray(gpuSol.vao)

    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)
    pipeline.setupVAO(gpuTierra)
    pipeline.setupVAO(gpuSol)
    pipeline.setupVAO(gpuLuna)


    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Using the time as the theta parameter
        theta = glfw.get_time()

        # * Movimiento tierra
        tierraTransform = tr.matmul([
            tr.rotationZ(-theta),
            tr.translate(math.sin(theta/10)*0.7, math.cos(theta/10)*0.7, 0),
            tr.uniformScale(0.3)
        ])

        # updating the transform attribute
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tierraTransform)
        # drawing function
        pipeline.drawCall(gpuTierra)

        # * Posición sol
        solTransform = tr.matmul([
            tr.translate(0, 0, 0),
            tr.uniformScale(0.5)
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, solTransform)
        pipeline.drawCall(gpuSol)

        #  * Movimiento luna
        lunaTransform = tr.matmul([
            tr.translate(math.sin(theta*1.1)*0.7, math.cos(theta*1.1)*0.7, 0),
            tr.rotationZ(-theta),
            tr.translate(math.sin(theta*2)*0.3, math.cos(theta*2)*0.3, 0),
            tr.uniformScale(0.1)
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, lunaTransform)
        pipeline.drawCall(gpuLuna)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuTierra.clear()
    gpuSol.clear()
    gpuLuna.clear()
    
    glfw.terminate()