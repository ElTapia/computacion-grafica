"""Funciones para crear distintas figuras y escenas """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.ex_curves as cv
import grafica.scene_graph as sg

def createGPUShape(shape, pipeline):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas

    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape

def createColorTriangle(r, g, b):
    # Funcion para crear un triangulo con un color personalizado

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r+0.05, g+0.05, b+0.05,
         0.0,  0.5, 0.0,  r+0.08, g+0.08, b+0.08]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return bs.Shape(vertices, indices)

def createColorCircle(N, r, g, b):
    # Funcion para crear un circulo con un color personalizado
    # Poligono de N lados 

    # First vertex at the center, white color
    vertices = [0, 0, 0, r, g, b]
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * math.cos(theta), 0.5 * math.sin(theta), 0,

            # color generates varying between 0 and 1
                  r, g, b]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    return bs.Shape(vertices, indices)


def createTree(gpuGreenTriangle, gpuBrownQuad, i):
    # Función que crea un árbol

    # Nodo de copa de un árbol, triangulo verde escalado
    treeTopNode = sg.SceneGraphNode("tree top {}".format(i))
    treeTopNode.transform = tr.matmul([tr.translate(0, 0.3, 0),tr.scale(0.2, 0.3, 1)])
    treeTopNode.childs = [gpuGreenTriangle]

    # Nodo de segunda copa de un árbol, triangulo verde escalado
    treeTop2Node = sg.SceneGraphNode("tree top 2 {}".format(i))
    treeTop2Node.transform = tr.matmul([tr.translate(0, 0.15, 0),tr.scale(0.2, 0.3, 1)])
    treeTop2Node.childs = [gpuGreenTriangle]

    # Nodo que contiene copas de los arboles
    treeTopsNode = sg.SceneGraphNode("tree tops {}".format(i))
    treeTopsNode.childs = [treeTop2Node, treeTopNode]

    # Nodo que contiene movimiento copas de arboles
    shearingTopsNode = sg.SceneGraphNode("tops shearing {}".format(i))
    shearingTopsNode.childs = [treeTopsNode]

    # Nodo de tronco de un árbol, triangulo verde escalado
    treeLogNode = sg.SceneGraphNode("tree log {}".format(i))
    treeLogNode.transform = tr.matmul([tr.scale(0.07, 0.2, 1)])
    treeLogNode.childs = [gpuBrownQuad]

    # Nodo de un arbol, con figuras creadas con anterioridad
    treeNode = sg.SceneGraphNode("tree {}".format(i))
    treeNode.childs = [treeLogNode, shearingTopsNode]
    return treeNode


def createScene(pipeline):
    # Funcion que crea la escena de la pregunta 2

    # Se crean las shapes en GPU
    gpuGreenTriangle = createGPUShape(createColorTriangle(0.125, 0.705, 0.094), pipeline) # Shape del triangulo verde
    gpuGrayQuad = createGPUShape(bs.createColorQuad(0.4, 0.4, 0.4), pipeline) # Shape del quad gris
    gpuWhiteQuad = createGPUShape(bs.createColorQuad(1,1,1), pipeline) # Shape del quad blanco
    gpuBrownQuad = createGPUShape(bs.createColorQuad(0.43,0.31,0.18), pipeline) # Shape del quad café
    gpuGreenQuad = createGPUShape(bs.createColorQuad(0.100, 0.500, 0.090), pipeline) # Shape del quad verde

    # Crea varios arboles y los agrupa
    treesList = []
    for i in range(3):
        newTree = createTree(gpuGreenTriangle, gpuBrownQuad, i)
        newTree.transform = tr.matmul([tr.translate(0, i/2, 0), tr.translate(0.75, -0.32, 0), tr.scale(1, 0.7, 1)])
        treesList.append(newTree)
    
    for i in range(3):
        newTree = createTree(gpuGreenTriangle, gpuBrownQuad, i+3)
        newTree.transform = tr.matmul([tr.translate(0, i/2, 0), tr.translate(-0.75, -0.82, 0), tr.scale(1, 0.7, 1)])
        treesList.append(newTree)

    treesNode = sg.SceneGraphNode("trees")
    treesNode.childs = treesList

    # Nodo de la carretera, quad gris escalado y posicionado
    highwayNode = sg.SceneGraphNode("highway")
    highwayNode.transform = tr.matmul([tr.scale(1.2, 4, 1)])
    highwayNode.childs = [gpuGrayQuad]

    # Nodo del pasto, quad verde escalado y posicionado
    grassNode = sg.SceneGraphNode("grass")
    grassNode.transform = tr.matmul([tr.scale(4, 4, 1)])
    grassNode.childs = [gpuGreenQuad]

    # nodo de la linea de pista, quad blanco escalado y posicionado
    lineNode = sg.SceneGraphNode("line 1")
    lineNode.transform = tr.matmul([tr.translate(0, -0.5, 0), tr.scale(0.02, 0.5, 1)])
    lineNode.childs = [gpuWhiteQuad]

    # nodo de la linea 2 de pista, quad blanco escalado y posicionado
    line2Node = sg.SceneGraphNode("line 2")
    line2Node.transform = tr.matmul([tr.translate(0, 0.5, 0), tr.scale(0.02, 0.5, 1)])
    line2Node.childs = [gpuWhiteQuad]

    # Nodo con las lineas de la pista
    linesNode = sg.SceneGraphNode("lines")
    linesNode.childs = [line2Node, lineNode]

    # nodo derecho de la linea de borde de pista, quad blanco escalado y posicionado
    borderLineNode = sg.SceneGraphNode("border line 1")
    borderLineNode.transform = tr.matmul([tr.translate(0.6, 0, 0), tr.scale(0.02, 4, 1)])
    borderLineNode.childs = [gpuWhiteQuad]

    # nodo izquierdo de la linea de borde de pista, quad blanco escalado y posicionado
    borderLine2Node = sg.SceneGraphNode("border line 2")
    borderLine2Node.transform = tr.matmul([tr.translate(-0.6, 0, 0), tr.scale(0.02, 4, 1)])
    borderLine2Node.childs = [gpuWhiteQuad]

    # nodo con lines de borde
    borderLinesNode = sg.SceneGraphNode("border lines")
    borderLinesNode.childs = [borderLine2Node, borderLineNode]

    # Nodo del background central con todos los nodos anteriores
    backGroundNode = sg.SceneGraphNode("background")
    backGroundNode.childs = [grassNode, highwayNode, linesNode, borderLinesNode, treesNode]

    # Nodo padre de la escena, sol se deja en mundo para poder desplazarlo
    sceneNode = sg.SceneGraphNode("world")
    sceneNode.childs = [backGroundNode]

    return sceneNode



