# coding=utf-8
"""Tarea 2b: Bailando con cel shading"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
import grafica.ex_curves as cv
from grafica.assets_path import getAssetPath
from obj_reader import *
from model_3D import *
from model_curves import *

__author__ = "Daniel Calderon"
__license__ = "MIT"


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# We will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1000
    height = 1000
    title = "Reading a *.obj file"

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Defining shader programs
    pipeline = ls.SimplePhongShaderProgram()
    mvpPipeline = es.SimpleTextureModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    model_3D = create3DModel(pipeline)
    skybox = createSceneSkybox(mvpPipeline)
    floor = createFloor(mvpPipeline)

    t0 = glfw.get_time()

    # inicializa variables
    camera_theta = -3*np.pi/4
    camZ = 10
    moveLightTheta = -3*np.pi/4
    moveLightZ = 8

    # inicializa modelo controlador de movimiento
    model_movement = ModelMovement()

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        t = t1%4.5

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor) + str(int(t)))

        # Using GLFW to check for input events
        glfw.poll_events()

        # Agrega movimiento a partes moviles
        model_movement.update(t)

        # * Cuerpo completo
        body = model_movement.body
        model_3D.transform = tr.matmul([tr.translate(0, 0, body.height)])

        # * mano y antebrazo derecho
        rightArm = model_movement.rightArm
        rightArmRotation = sg.findNode(model_3D, "rotate right arm")
        rightArmRotation.transform = tr.matmul([tr.rotationX(rightArm.theta_x) ,tr.rotationY(rightArm.theta_y), tr.rotationZ(rightArm.theta_z)])


        # * brazo completo derecho
        completeRightArm = model_movement.completeRightArm
        completeRightArmRotation = sg.findNode(model_3D, "rotate complete right arm")
        completeRightArmRotation.transform = tr.matmul([tr.rotationX(completeRightArm.theta_x), tr.rotationY(completeRightArm.theta_y), 
                                                        tr.rotationZ(completeRightArm.theta_z)])


        # * mano y antebrazo izquierdo
        leftArm = model_movement.leftArm
        leftArmRotation = sg.findNode(model_3D, "rotate left arm")
        leftArmRotation.transform = tr.matmul([tr.rotationX(leftArm.theta_x), tr.rotationY(leftArm.theta_y), tr.rotationZ(leftArm.theta_z)])


        # * brazo completo izquierdo
        completeLeftArm = model_movement.completeLeftArm
        completeLeftArmRotation = sg.findNode(model_3D, "rotate complete left arm")
        completeLeftArmRotation.transform = tr.matmul([tr.rotationX(completeLeftArm.theta_x), tr.rotationY(completeLeftArm.theta_y),
                                                       tr.rotationZ(completeLeftArm.theta_z)])

        # * pierna y pie derecho
        rightFoot = model_movement.rightFoot
        rightLegRotation = sg.findNode(model_3D, "rotate right foot")
        rightLegRotation.transform = tr.matmul([tr.rotationX(rightFoot.theta_x), tr.rotationY(rightFoot.theta_y), tr.rotationZ(rightFoot.theta_z)])

        # * pierna completa derecha
        rightLeg = model_movement.rightLeg
        completeRightLegRotation = sg.findNode(model_3D, "rotate complete right leg")
        completeRightLegRotation.transform = tr.matmul([tr.rotationY(rightLeg.theta_y), tr.rotationX(rightLeg.theta_x), tr.rotationZ(rightLeg.theta_z)])

        # * pierna y pie izquierdo
        leftFoot = model_movement.leftFoot
        leftLegRotation = sg.findNode(model_3D, "rotate left foot")
        leftLegRotation.transform = tr.matmul([tr.rotationY(leftFoot.theta_y), tr.rotationX(leftFoot.theta_x), tr.rotationZ(leftFoot.theta_z)])

        # * pierna completa izquierda
        leftLeg = model_movement.leftLeg
        completeLeftLegRotation = sg.findNode(model_3D, "rotate complete left leg")
        completeLeftLegRotation.transform = tr.matmul([tr.rotationY(leftLeg.theta_y), tr.rotationX(leftLeg.theta_x), tr.rotationZ(leftLeg.theta_z)])


        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt

        if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
            camZ += 8* dt

        if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
            camZ -= 8* dt

        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            moveLightTheta += 2* dt

        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            moveLightTheta -= 2* dt

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            moveLightZ += 8 * dt

        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            moveLightZ -= 8 * dt

        # Setting up the view transform
        R = 25
        camX = R * np.sin(camera_theta)
        camY = R * np.cos(camera_theta)

        viewPos = np.array([camX, camY, camZ])
        view = tr.lookAt(
            viewPos,
            np.array([0,0,7]),
            np.array([0,0,1])
        )

        # Setting uniforms that will NOT change on each iteration
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.6, 0.6, 0.6)

        lightposition = [5*np.cos(moveLightTheta), 5*np.sin(moveLightTheta), moveLightZ]
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), lightposition[0], lightposition[1], lightposition[2])
        
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 500)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        # Setting up the projection transform
        projection = tr.perspective(60, float(width)/float(height), 0.1, 300)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        glUseProgram(mvpPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Drawing shapes
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        sg.drawSceneGraphNode(model_3D, pipeline, "model")
        
        glUseProgram(mvpPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(skybox, mvpPipeline, "model")
        sg.drawSceneGraphNode(floor, mvpPipeline, "model")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    model_3D.clear()
    skybox.clear()
    floor.clear()

    glfw.terminate()
