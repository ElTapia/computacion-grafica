# coding=utf-8
"""Textures and transformations in 3D"""

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
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath
import grafica.ex_curves as cv

__author__ = "Daniel Calderon"
__license__ = "MIT"

############################################################################

def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape


def createColorPyramid(r, g ,b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions         colors
        -0.5, 0.5,  0,  r, g, b,
         0.5, -0.5, 0,  r, g, b,
         0.5, 0.5,  0,  r, g, b,
        -0.5, -0.5, 0,  r, g, b,
         0, 0,  0.5,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         0, 1, 3,
         0, 2, 4,
         2, 4, 1,
         3, 4, 1,
         0, 4, 3]

    return bs.Shape(vertices, indices)

def createColorTriangularPrism(r, g ,b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions         colors
        -0.5, 0.5,  0,  r, g, b,
         0.5, -0.5, 0,  r+0.2, g+0.2, b+0.2,
         0.5, 0.5,  0,  r, g, b,
        -0.5, -0.5, 0,  r+0.2, g+0.2, b+0.2,
         0.5, 0,  -0.5,  r, g, b,
         -0.5, 0,  -0.5,  r+0.2, g+0.2, b+0.2,
         -1, 0,  0,  r, g, b,
         1, 0,  0,  r+0.2, g+0.2, b+0.2]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         0, 1, 3, # base
         0, 5, 3, # lateral 1
         2, 4, 1, # lateral 2
         3, 4, 5,
         3, 4, 1, # cuadrado inclinado 1
         2, 5, 4,
         2, 5, 0, # cuadrado inclinado 2
         0, 6, 3,
         6, 5, 3, # saliente triangular 1
         6, 0, 5,
         1, 2, 7,
         1, 7, 4,
         2, 7, 4] # saliente triangular 2

    return bs.Shape(vertices, indices)

def create_tree(pipeline):
    # Piramide verde
    green_pyramid = createColorPyramid(0, 1, 0)
    gpuGreenPyramid = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGreenPyramid)
    gpuGreenPyramid.fillBuffers(green_pyramid.vertices, green_pyramid.indices, GL_STATIC_DRAW)

    # Cubo cafe
    brown_quad = bs.createColorCube(139/255, 69/255, 19/255)
    gpuBrownQuad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownQuad)
    gpuBrownQuad.fillBuffers(brown_quad.vertices, brown_quad.indices, GL_STATIC_DRAW)

    # Tronco
    tronco = sg.SceneGraphNode("tronco")
    tronco.transform = tr.scale(0.05, 0.05, 0.2)
    tronco.childs += [gpuBrownQuad]

    # Hojas
    hojas = sg.SceneGraphNode("hojas")
    hojas.transform = tr.matmul([tr.translate(0, 0, 0.1), tr.uniformScale(0.25)])
    hojas.childs += [gpuGreenPyramid]

    # Arbol
    tree = sg.SceneGraphNode("arbol")
    tree.transform = tr.identity()
    tree.childs += [tronco, hojas]

    return tree


def create_house(pipeline):
    # Piramide cafe
    brown_pyramid = createColorPyramid(150/255, 100/255, 30/255)
    gpuBrownPyramid = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownPyramid)
    gpuBrownPyramid.fillBuffers(brown_pyramid.vertices, brown_pyramid.indices, GL_STATIC_DRAW)

    # Cubo rojo
    red_cube = bs.createColorCube(1, 0, 0)
    gpuRedCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRedCube)
    gpuRedCube.fillBuffers(red_cube.vertices, red_cube.indices, GL_STATIC_DRAW)

    # Cubo cafe
    brown_cube = bs.createColorCube(166/255, 112/255, 49/255)
    gpuBrownCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownCube)
    gpuBrownCube.fillBuffers(brown_cube.vertices, brown_cube.indices, GL_STATIC_DRAW)

    # Techo
    techo = sg.SceneGraphNode("techo")
    techo.transform = tr.matmul([tr.translate(0, 0, 0.1), tr.scale(0.2, 0.4, 0.2)])
    techo.childs += [gpuBrownPyramid]

    # Base
    base = sg.SceneGraphNode("base")
    base.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.2, 0.4, 0.2)])
    base.childs += [gpuRedCube]

    # Puerta
    puerta = sg.SceneGraphNode("puerta")
    puerta.transform = tr.matmul([tr.translate(0, -0.2, 0), tr.scale(0.05, 0.001, 0.1)])
    puerta.childs += [gpuBrownCube]

    # Casa
    casa = sg.SceneGraphNode("house")
    casa.transform = tr.identity()
    casa.childs += [techo, base, puerta]

    return casa

def create_river(pipeline, w, curve, N):

    curve1 = curve - np.array([w/2, 0, 0])
    curve2 = curve + np.array([w/2, 0, 0])

    vertices = []
    indices = []
    counter = 0 # Contador de vertices, para indicar los indices

    for i in range(len(curve) - 1):
        c_0 = curve1[i] # punto i de la curva
        r_0 = curve2[i] # punto i de la curva trasladada
        c_1 = curve1[i + 1] # punto i + 1 de la curva
        r_1 = curve2[i + 1] # punto i + 1 de la curva trasladada

        vertices += [c_0[0], c_0[1], 0, 0.3, 0.3, 1.0]
        vertices += [r_0[0], r_0[1], 0, 0, 0, 0.7]
        vertices += [c_1[0], c_1[1], 0, 0.3, 0.3, 1.0]
        vertices += [r_1[0], r_1[1], 0, 0, 0, 0.7]
        indices += [counter + 0, counter + 1, counter + 2]
        indices += [counter + 2, counter + 3, counter + 1]
        counter += 4

    riverShape = bs.Shape(vertices, indices)
    gpuRiver = createGPUShape(riverShape, pipeline)

    river = sg.SceneGraphNode("rio")
    river.transform = tr.matmul([tr.translate(0, 0, 0.001)])
    river.childs += [gpuRiver]
    return river

def create_boat(pipeline):
    # Prisma triangular cafe
    brown_prism = createColorTriangularPrism(139/255, 69/255, 19/255)
    gpuBrownPrism = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownPrism)
    gpuBrownPrism.fillBuffers(brown_prism.vertices, brown_prism.indices, GL_DYNAMIC_DRAW)

    white_triangle = bs.createColorTriangle(0.8, 0.8, 0.8)
    gpuWhiteTriangle = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWhiteTriangle)
    gpuWhiteTriangle.fillBuffers(white_triangle.vertices, white_triangle.indices, GL_DYNAMIC_DRAW)

    # Vela
    vela = sg.SceneGraphNode("vela")
    vela.transform = tr.matmul([tr.translate(0, 0, 0.05), tr.rotationZ(np.pi/2),tr.rotationX(np.pi/2), tr.scale(0.15, 0.08, 1)])
    vela.childs += [gpuWhiteTriangle]

    # Base bote
    bote = sg.SceneGraphNode("bote")
    bote.transform = tr.matmul([tr.translate(0, 0, 0.03), tr.rotationZ(np.pi/2), tr.scale(0.1, 0.1, 0.1)])
    bote.childs += [gpuBrownPrism]

    # Movimiento bote
    bote_move = sg.SceneGraphNode("bote move")
    bote_move.transform = tr.matmul([tr.translate(0, 0, 0)])
    bote_move.childs += [bote, vela]

    return bote_move


def create_skybox(pipeline):
    shapeSky = bs.createTextureCube('paisaje.jfif')
    gpuSky = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSky)
    gpuSky.fillBuffers(shapeSky.vertices, shapeSky.indices, GL_STATIC_DRAW)
    gpuSky.texture = es.textureSimpleSetup(
        getAssetPath("paisaje2.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    skybox = sg.SceneGraphNode("skybox")
    skybox.transform = tr.matmul([tr.translate(0, 0, 0.3), tr.uniformScale(2)])
    skybox.childs += [gpuSky]

    return skybox

def create_floor(pipeline):
    shapeFloor = bs.createTextureQuad(8, 8)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("grass.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.matmul([tr.translate(0, 0, 0),tr.scale(2, 2, 1)])
    floor.childs += [gpuFloor]

    return floor

def create_decorations(pipeline, curve, N):
    tree1 = create_tree(pipeline)
    tree1.transform = tr.translate(0.5, 0, 0)

    tree2 = create_tree(pipeline)
    tree2.transform = tr.translate(-0.5, 0, 0)

    tree3 = create_tree(pipeline)
    tree3.transform = tr.translate(0, -0.5, 0)

    tree4 = create_tree(pipeline)
    tree4.transform = tr.translate(-0.2, 0.5, 0)

    tree5 = create_tree(pipeline)
    tree5.transform = tr.translate(0.2, 0.5, 0)

    house = create_house(pipeline)
    house.transform = tr.translate(0, 0.5, 0)

    river = create_river(pipeline, 0.25, curve, N)

    boat = create_boat(pipeline)

    decorations = sg.SceneGraphNode("decorations")
    decorations.transform = tr.identity()
    decorations.childs += [tree1, tree2, tree3, tree4, tree5, house, river, boat]    

    return decorations

############################################################################

N = 100
P0 = np.array([[4, 4, 0]]).T
P1 = np.array([[-0.35, 1, 0]]).T
P2 = np.array([[0, -1, 0]]).T
P3 = np.array([[-4.5, -4.5, 0]]).T
GMcr = cv.catmullRomMatrix(P0, P1, P2, P3)
curve = cv.evalCurve(GMcr, N)

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
###########################################################
        self.theta = np.pi
        self.eye = [0, 0, 0.1]
        self.at = [0, 1, 0.1]
        self.up = [0, 0, 1]
        self.boat_index = 0
###########################################################


# global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    
###########################################################

    elif key == glfw.KEY_W:
        controller.eye += (controller.at - controller.eye) * 0.05
        controller.at += (controller.at - controller.eye) * 0.05

    elif key == glfw.KEY_S:
        controller.eye -= (controller.at - controller.eye) * 0.05
        controller.at -= (controller.at - controller.eye) * 0.05

    elif key == glfw.KEY_D:
        controller.theta -= np.pi*0.05
    elif key == glfw.KEY_A:
        controller.theta += np.pi*0.05

    elif key == glfw.KEY_H:
        controller.boat_index += 1

###########################################################
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
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)


    window = glfw.create_window(width, height, "Ejercicio 6: Rio y bote", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

###########################################################################################
    # Creating shapes on GPU memory

    decorations = create_decorations(colorShaderProgram, curve, N)
    skybox = create_skybox(textureShaderProgram)
    floor = create_floor(textureShaderProgram)

###########################################################################################

    # View and projection
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

###########################################################################

        at_x = controller.eye[0] + np.cos(controller.theta)
        at_y = controller.eye[1] + np.sin(controller.theta)
        controller.at = np.array([at_x, at_y, controller.at[2]])

        view = tr.lookAt(controller.eye, controller.at, controller.up)

###########################################################################

        if controller.boat_index < N:
            sg.findNode(decorations, "bote move").transform = tr.matmul([tr.translate(curve[controller.boat_index][0], curve[controller.boat_index][1], 0)])

        if controller.boat_index == N:
            controller.boat_index = 0

###########################################################################

        # Drawing (no texture)
        glUseProgram(colorShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        sg.drawSceneGraphNode(decorations, colorShaderProgram, "model")

        # Drawing dice (with texture, another shader program)
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        sg.drawSceneGraphNode(skybox, textureShaderProgram, "model")
        sg.drawSceneGraphNode(floor, textureShaderProgram, "model")       

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
