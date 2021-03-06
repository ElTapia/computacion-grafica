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


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    # Activa cel shading
    elif key == glfw.KEY_TAB:
        controller.celShading = not controller.celShading

    # Activa slow motions
    elif key == glfw.KEY_1:
        controller.slowMotion = not controller.slowMotion

    # Activa camara automatica
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

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Defining shader program
    celShadingPipeline = ls.MultipleCelShadingShaderProgram()
    phongPipeline = ls.MultiplePhongShaderProgram()
    textPhongPipeline = ls.MultipleTexturePhongShaderProgram()
    texCelShadingPipeline = ls.MultipleTextureCelShadingShaderProgram()

    # Creating shapes on GPU memory
    model_3D = create3DModel(phongPipeline, textPhongPipeline)
    skybox = createSceneSkybox(textPhongPipeline)
    floor = createFloor(textPhongPipeline)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    t0 = glfw.get_time()

    # Par??metros para reducir fps en slow motion
    lastFrameTime = glfw.get_time()
    fpsLimit = 1.0 / 25.0

    # We will use the global controller as communication with the callback function
    controller = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Par??metros para spotlight
    spotDirection1 = [2.5, -50, -30]
    spotDirection2 = [2.5, 50, -30]
    spotDirection3 = [-8, 0, -4]
    spotDirection4 = [2.3, 0, -9]

    spotConcentration = 1.231
    shininess = 500

    # Luz ambiental
    La = [0, 0, 0]

    # Factores de reflexion en materiales
    Ka = [0.3, 0.3, 0.3]
    Kd = [0.8, 0.8, 0.8]
    Ks = [0.5, 0.5, 0.5]


    # inicializa variables
    camera_t = 8

    moveLight_t = 8

    # inicializa modelo controlador de movimiento
    model_movement = ModelMovement()

    # Inicializa curva para luces
    light_movement = lightMovement()
    light_movement.set_points()

    # Inicializa curva para camara
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

        # Tiempo para el movimiento de las partes
        t = t1%10

        # activa camara automatica -> avanza sola en su curva
        if controller.autoCam:
            camera_t -= 2.3 * dt

        # Setea colores de luces
        Ld1 = [0.8, 0.1, 0.1]
        Ls1 = [0.8, 0.1, 0.1]

        Ld2 = [0.8, 0.8, 0.8]
        Ls2 = [0.8, 0.8, 0.8]

        Ld3 = [0.1, 0.1, 0.8]
        Ls3 = [0.1, 0.1, 0.8]

        Ld4 = [0.1, 0.1, 0.8]
        Ls4 = [0.1, 0.1, 0.8]

        # Enciende y apaga luces
        if int((2.5*t1)%3) == 0:
            Ld1 = [0, 0, 0]
            Ls1 = [0, 0, 0]

        elif int((2.5*t1)%3) == 1:
            Ld2 = [0, 0, 0]
            Ls2 = [0, 0, 0]

        elif int((2.5*t1)%3) == 2:
            Ld3 = [0, 0, 0]
            Ls3 = [0, 0, 0]

            Ld4 = [0, 0, 0]
            Ls4 = [0, 0, 0]


        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor) + " Dance time: " + str(int(t)) + " segs.")

        # Using GLFW to check for input events
        glfw.poll_events()

        # Activa cel shading
        if controller.celShading:
            pipeline = celShadingPipeline
            tex_pipeline = texCelShadingPipeline
        else:
            pipeline = phongPipeline
            tex_pipeline = textPhongPipeline

        # Actualiza movimiento luces
        moveLight_t += 2* dt
        light_movement.update(moveLight_t%2)

        # Dibuja y agrega movimiento a partes moviles
        model_movement.update(t)

        # Actualiza posicion camara
        cam_movement.update(camera_t%10)

        # Movimientos de cada parte
        # * Cuerpo completo
        body = model_movement.body
        jumpBody = sg.findNode(model_3D, "jump model")
        jumpBody.transform = tr.matmul([tr.translate(0, 0, body.height)])


        # * Cabeza
        head = model_movement.head
        headRotation = sg.findNode(model_3D, "rotate head")
        headRotation.transform = tr.matmul([tr.translate(0, 0, body.height), tr.translate(0, 0, 6), tr.rotationZ(head.rotation)])


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

        # Controla movimiento de camara con teclas y si no esta automatico
        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS) and not controller.autoCam:
            camera_t += 2.3 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS) and not controller.autoCam:
            camera_t -= 2.3 * dt

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

        # Posiciones de la luz siguen curva
        lightposition0 = [light_movement.pos, 67, 50] # Mueve en eje x
        lightposition1 = [light_movement.pos, -67, 50] # Mueve en eje x
        lightposition2 = [25, light_movement.pos, 30] # Mueve en eje y
        lightposition3 = [-36, light_movement.pos, 39] # Mueve en eje y

        # Setting uniforms
        # Pipeline sin texturas
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "spotDirection1"), spotDirection1[0], spotDirection1[1], spotDirection1[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "spotDirection2"), spotDirection2[0], spotDirection2[1], spotDirection2[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "spotDirection3"), spotDirection3[0], spotDirection3[1], spotDirection3[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "spotDirection4"), spotDirection4[0], spotDirection4[1], spotDirection4[2])

        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "spotConcentration"), spotConcentration)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), La[0], La[1], La[2])

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld1"), Ld1[0], Ld1[1], Ld1[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld2"), Ld2[0], Ld2[1], Ld2[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld3"), Ld3[0], Ld3[1], Ld3[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld4"), Ld4[0], Ld4[1], Ld4[2])

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls1"), Ls1[0], Ls1[1], Ls1[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls2"), Ls2[0], Ls2[1], Ls2[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls3"), Ls3[0], Ls3[1], Ls3[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls4"), Ls4[0], Ls4[1], Ls4[2])

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), Ka[0], Ka[1], Ka[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), Kd[0], Kd[1], Kd[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), Ks[0], Ks[1], Ks[2])

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition0"), lightposition0[0], lightposition0[1], lightposition0[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition1"), lightposition1[0], lightposition1[1], lightposition1[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition2"), lightposition2[0], lightposition2[1], lightposition2[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition3"), lightposition3[0], lightposition3[1], lightposition3[2])

        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), shininess)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), cam_movement.pos[0], cam_movement.pos[1], cam_movement.pos[2])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        # Dibuja solo la cabeza -> Unica sin texturas (solo color)
        sg.drawSceneGraphNode(sg.findNode(model_3D, "rotate head"), pipeline, "model")

        # Pipeline de texturas
        glUseProgram(tex_pipeline.shaderProgram)

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "spotDirection1"), spotDirection1[0], spotDirection1[1], spotDirection1[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "spotDirection2"), spotDirection2[0], spotDirection2[1], spotDirection2[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "spotDirection3"), spotDirection3[0], spotDirection3[1], spotDirection3[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "spotDirection4"), spotDirection4[0], spotDirection4[1], spotDirection4[2])

        glUniform1f(glGetUniformLocation(tex_pipeline.shaderProgram, "spotConcentration"), spotConcentration)
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "La"), La[0], La[1], La[2])

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ld1"), Ld1[0], Ld1[1], Ld1[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ld2"), Ld2[0], Ld2[1], Ld2[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ld3"), Ld3[0], Ld3[1], Ld3[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ld4"), Ld4[0], Ld4[1], Ld4[2])

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ls1"), Ls1[0], Ls1[1], Ls1[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ls2"), Ls2[0], Ls2[1], Ls2[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ls3"), Ls3[0], Ls3[1], Ls3[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ls4"), Ls4[0], Ls4[1], Ls4[2])

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ka"), Ka[0], Ka[1], Ka[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Kd"), Kd[0], Kd[1], Kd[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ks"), Ks[0], Ks[1], Ks[2])

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "lightPosition0"), lightposition0[0], lightposition0[1], lightposition0[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "lightPosition1"), lightposition1[0], lightposition1[1], lightposition1[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "lightPosition2"), lightposition2[0], lightposition2[1], lightposition2[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "lightPosition3"), lightposition3[0], lightposition3[1], lightposition3[2])

        glUniform1ui(glGetUniformLocation(tex_pipeline.shaderProgram, "shininess"), shininess)
        glUniform1f(glGetUniformLocation(tex_pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(tex_pipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(tex_pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(tex_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "viewPosition"), cam_movement.pos[0], cam_movement.pos[1], cam_movement.pos[2])
        glUniformMatrix4fv(glGetUniformLocation(tex_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(tex_pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        # Dibuja objetos con texturas
        sg.drawSceneGraphNode(skybox, tex_pipeline, "model")
        sg.drawSceneGraphNode(floor, tex_pipeline, "model")
        sg.drawSceneGraphNode(sg.findNode(model_3D, "jump model"), tex_pipeline, "model")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.

        # Activa slow motion dibujando cada 15 fps
        if controller.slowMotion:
            if (t1 - lastFrameTime) >= fpsLimit:
                glfw.swap_buffers(window)
                lastFrameTime = t1

        else:
            glfw.swap_buffers(window)


    # freeing GPU memory
    model_3D.clear()
    skybox.clear()
    floor.clear()

    glfw.terminate()
