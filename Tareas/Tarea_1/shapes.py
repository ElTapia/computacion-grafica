"""Funciones para crear distintas figuras y escenas """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.scene_graph as sg

def createGPUShape(shape, pipeline, usage=GL_STATIC_DRAW):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, usage)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path, usage):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas

    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, usage)
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

def createColorTreeTop(N, r, g, b):
    # Funcion para crear la copa de un arbol
    # Poligono de N lados

    # First vertex at the center, white color
    vertices = [0, 0, 0, r, g, b]
    indices = []

    dtheta =  2*math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.3 * math.cos(theta), 0.3 * math.sin(theta)+0.5, 0,

            # color generates varying between 0 and 1
                  r, g, b]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]


    return bs.Shape(vertices, indices)


def createTree(gpuGreenTop, gpuBrownQuad, i):
    # Función que crea un árbol
    top_scale = 0.2
    top_translate = 0.2
    # Nodo de copa de un árbol, triangulo verde escalado
    treeTopNode = sg.SceneGraphNode("tree top {}".format(i))
    treeTopNode.transform = tr.matmul([tr.translate(0, top_translate, 0),tr.scale(top_scale, top_scale, 1)])
    treeTopNode.childs = [gpuGreenTop]

    # Nodo de copa de un árbol, triangulo verde escalado
    treeTop2Node = sg.SceneGraphNode("tree top 2 {}".format(i))
    treeTop2Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(math.pi/4),tr.scale(top_scale, top_scale, 1)])
    treeTop2Node.childs = [gpuGreenTop]

    # Nodo de copa de un árbol, triangulo verde escalado
    treeTop3Node = sg.SceneGraphNode("tree top 3 {}".format(i))
    treeTop3Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(math.pi/2),tr.scale(top_scale, top_scale, 1)])
    treeTop3Node.childs = [gpuGreenTop]

    # Nodo de copa de un árbol, triangulo verde escalado
    treeTop4Node = sg.SceneGraphNode("tree top 4 {}".format(i))
    treeTop4Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(3*math.pi/4),tr.scale(top_scale, top_scale, 1)])
    treeTop4Node.childs = [gpuGreenTop]

    # Nodo de copa de un árbol, triangulo verde escalado
    treeTop5Node = sg.SceneGraphNode("tree top 5 {}".format(i))
    treeTop5Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(-math.pi),tr.scale(top_scale, top_scale, 1)])
    treeTop5Node.childs = [gpuGreenTop]

    # Nodo de copa de un árbol, triangulo verde escalado
    treeTop6Node = sg.SceneGraphNode("tree top 5 {}".format(i))
    treeTop6Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(-math.pi/4),tr.scale(top_scale, top_scale, 1)])
    treeTop6Node.childs = [gpuGreenTop]

    # Nodo de copa de un árbol, triangulo verde escalado
    treeTop7Node = sg.SceneGraphNode("tree top 5 {}".format(i))
    treeTop7Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(-math.pi/2),tr.scale(top_scale, top_scale, 1)])
    treeTop7Node.childs = [gpuGreenTop]

    # Nodo de copa de un árbol, triangulo verde escalado
    treeTop8Node = sg.SceneGraphNode("tree top 5 {}".format(i))
    treeTop8Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(-3*math.pi/4),tr.scale(top_scale, top_scale, 1)])
    treeTop8Node.childs = [gpuGreenTop]

    # Nodo que contiene movimiento copas de arboles
    shearingTopsNode = sg.SceneGraphNode("tops shearing {}".format(i))
    shearingTopsNode.childs = [treeTopNode, treeTop2Node, treeTop3Node, treeTop4Node, treeTop5Node, treeTop6Node, treeTop7Node, treeTop8Node]

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
    gpuGreenTop = createGPUShape(createColorTreeTop(15, 0.125, 0.705, 0.094), pipeline, GL_DYNAMIC_DRAW) # Shape de la copa verde
    gpuGrayQuad = createGPUShape(bs.createColorQuad(0.4, 0.4, 0.4), pipeline) # Shape del quad gris
    gpuWhiteQuad = createGPUShape(bs.createColorQuad(1,1,1), pipeline) # Shape del quad blanco
    gpuBrownQuad = createGPUShape(bs.createColorQuad(0.43,0.31,0.18), pipeline) # Shape del quad café
    gpuGreenQuad = createGPUShape(bs.createColorQuad(0.100, 0.500, 0.090), pipeline) # Shape del quad verde

    # Crea varios arboles y los agrupa
    treesList = []
    for i in range(3):
        newTree = createTree(gpuGreenTop, gpuBrownQuad, i)
        newTree.transform = tr.matmul([tr.translate(0, i/2, 0), tr.translate(0.75, -0.32, 0), tr.scale(1, 0.7, 1)])
        treesList.append(newTree)
    
    for i in range(3):
        newTree = createTree(gpuGreenTop, gpuBrownQuad, i+3)
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



