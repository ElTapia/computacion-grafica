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
        self.celShading = False
        self.slowMotion = False
        self.autoCam = False


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

    elif key == glfw.KEY_TAB:
        controller.celShading = not controller.celShading
    
    elif key == glfw.KEY_1:
        controller.slowMotion = not controller.slowMotion
    
    elif key == glfw.KEY_2:
        controller.autoCam = not controller.autoCam


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1000
    height = 1000
    title = "Monito vidal cel shading"

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

    # Defining shader program
    celShadingPipeline = ls.MultipleCelShadingShaderProgram()
    phongPipeline = ls.MultiplePhongShaderProgram()
    textPhongPipeline = ls.MultipleTexturePhongShaderProgram()
    texCelShadingPipeline = ls.MultipleTextureCelShadingShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    model_3D = create3DModel(phongPipeline)
    skybox = createSceneSkybox(textPhongPipeline)
    floor = createFloor(textPhongPipeline)

    t0 = glfw.get_time()

    # inicializa variables
    camera_t = 8

    moveLight1Theta = -3*np.pi/4
    moveLight2Theta = 3*np.pi/4
    moveLight3Theta = np.pi/4
    moveLight4Theta = -np.pi/4

    moveLightZ_t = 8

    # inicializa modelo controlador de movimiento
    model_movement = ModelMovement()

    light_movement = lightMovement()
    light_movement.set_points()

    cam_movement = CamMovement()
    cam_movement.set_points()

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        t = t1%4.5
        if controller.slowMotion:
            t = (t1/10)%4.5

        if controller.autoCam:
            camera_t -= 3 * dt

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor) + " Dance time: " + str(int(t)))

        # Using GLFW to check for input events
        glfw.poll_events()

        if controller.celShading:
            pipeline = celShadingPipeline
            tex_pipeline = texCelShadingPipeline
        else:
            pipeline = phongPipeline
            tex_pipeline = textPhongPipeline

        # Actualiza movimiento luces
        moveLight1Theta += 3 * dt
        moveLight2Theta += 3 * dt
        moveLight3Theta += 3 * dt
        moveLight4Theta += 3 * dt

        moveLightZ_t += 3* dt
        light_movement.update(moveLightZ_t%2)

        # Dibuja y agrega movimiento a partes moviles
        model_movement.update(t)

        # Actualiza posicion camara
        cam_movement.update(camera_t%10)

        # * Cuerpo completo
        body = model_movement.body
        jumpBody = sg.findNode(model_3D, "jump model")
        jumpBody.transform = tr.matmul([tr.translate(0, 0, body.height)])

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


        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS) and not controller.autoCam:
            camera_t += 3 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS) and not controller.autoCam:
            camera_t -= 3 * dt

        # Setting up the view transform
        view = tr.lookAt(
            cam_movement.pos,
            np.array([0,0,10]),
            np.array([0,0,1])
        )

        # Setting up the projection transform
        projection = tr.perspective(60, float(width)/float(height), 0.1, 300)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        La = [1.0, 1.0, 1.0]
        Ld = [1.0, 1.0, 1.0]
        Ls = [1.0, 1.0, 1.0]

        Ka = [0.3, 0.3, 0.3]
        Kd = [0.8, 0.8, 0.8]
        Ks = [0.5, 0.5, 0.5]

        # Setting uniforms that will NOT change on each iteration
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), La[0], La[1], La[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), Ld[0], Ld[1], Ld[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), Ls[0], Ls[1], Ls[2])

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), Ka[0], Ka[1], Ka[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), Kd[0], Kd[1], Kd[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), Ks[0], Ks[1], Ks[2])

        lightposition0 = [25*np.cos(moveLight1Theta), 25*np.sin(moveLight1Theta), light_movement.pos_z]
        lightposition1 = [10*np.cos(moveLight2Theta), 10*np.sin(moveLight2Theta), light_movement.pos_z]
        lightposition2 = [25*np.cos(moveLight3Theta), 25*np.sin(moveLight3Theta), light_movement.pos_z]
        lightposition3 = [10*np.cos(moveLight4Theta), 10*np.sin(moveLight4Theta), light_movement.pos_z]

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition0"), lightposition0[0], lightposition0[1], lightposition0[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition1"), lightposition1[0], lightposition1[1], lightposition1[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition2"), lightposition2[0], lightposition2[1], lightposition2[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition3"), lightposition3[0], lightposition3[1], lightposition3[2])
        
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 1000)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), cam_movement.pos[0], cam_movement.pos[1], cam_movement.pos[2])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        sg.drawSceneGraphNode(model_3D, pipeline, "model")

        glUseProgram(tex_pipeline.shaderProgram)

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "La"), La[0], La[1], La[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ld"), Ld[0], Ld[1], Ld[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ls"), Ls[0], Ls[1], Ls[2])

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ka"), Ka[0], Ka[1], Ka[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Kd"), Kd[0], Kd[1], Kd[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ks"), Ks[0], Ks[1], Ks[2])

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "lightPosition0"), lightposition0[0], lightposition0[1], lightposition0[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "lightPosition1"), lightposition1[0], lightposition1[1], lightposition1[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "lightPosition2"), lightposition2[0], lightposition2[1], lightposition2[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "lightPosition3"), lightposition3[0], lightposition3[1], lightposition3[2])

        glUniform1ui(glGetUniformLocation(tex_pipeline.shaderProgram, "shininess"), 1000)
        glUniform1f(glGetUniformLocation(tex_pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(tex_pipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(tex_pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(tex_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "viewPosition"), cam_movement.pos[0], cam_movement.pos[1], cam_movement.pos[2])
        glUniformMatrix4fv(glGetUniformLocation(tex_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(tex_pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        sg.drawSceneGraphNode(skybox, tex_pipeline, "model")
        sg.drawSceneGraphNode(floor, tex_pipeline, "model")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    model_3D.clear()
    skybox.clear()
    floor.clear()

    glfw.terminate()
