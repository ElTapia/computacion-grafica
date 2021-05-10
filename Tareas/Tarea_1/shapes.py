"""Funciones para crear distintas figuras y escenas """

import numpy as np
import math
from OpenGL.GL import *
import grafica.shaders as es
import grafica.transformations as tr
import grafica.scene_graph as sg

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, textureFileName=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = textureFileName


def createGPUShape(shape, pipeline, usage=GL_STATIC_DRAW):
    # Initialize GPUShape
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, usage)
    return gpuShape


def createTextureGPUShape(shape, pipeline, path, usage):
    # Initialize GPUShape with textures

    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, usage)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape


def createColorTriangle(r, g, b):
    # Create triangle with personalized color

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r+0.05, g+0.05, b+0.05,
         0.0,  0.5, 0.0,  r+0.08, g+0.08, b+0.08]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return Shape(vertices, indices)

def createColorQuad(r, g, b):
    # Create quad with personalized color

    # Defining locations and colors for each vertex of the shape    
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r+0.1, g+0.1, b+0.1,
         0.5,  0.5, 0.0,  r+0.2, g+0.2, b+0.2,
        -0.5,  0.5, 0.0,  r+0.23, g+0.23, b+0.23]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)


def createTextureQuad(nx, ny):
    # Create triangle with texture

    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions        texture
        -0.5, -0.5, 0.0,  0, ny,
         0.5, -0.5, 0.0, nx, ny,
         0.5,  0.5, 0.0, nx, 0,
        -0.5,  0.5, 0.0,  0, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)


def createColorTreeTop(N, r, g, b):
    # Create top of a tree
    # circle with center outside

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

    return Shape(vertices, indices)


def createTree(gpuGreenTop, gpuBrownQuad, i):
    # Creates a tree
    top_scale = 0.2
    top_translate = 0.2

    # Top of the tree node, deformed circle scalated
    treeTopNode = sg.SceneGraphNode("tree top {}".format(i))
    treeTopNode.transform = tr.matmul([tr.translate(0, top_translate, 0),tr.scale(top_scale, top_scale, 1)])
    treeTopNode.childs = [gpuGreenTop]

    # Top of the tree node, deformed circle scalated
    treeTop2Node = sg.SceneGraphNode("tree top 2 {}".format(i))
    treeTop2Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(math.pi/4),tr.scale(top_scale, top_scale, 1)])
    treeTop2Node.childs = [gpuGreenTop]

    # Top of the tree node, deformed circle scalated
    treeTop3Node = sg.SceneGraphNode("tree top 3 {}".format(i))
    treeTop3Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(math.pi/2),tr.scale(top_scale, top_scale, 1)])
    treeTop3Node.childs = [gpuGreenTop]

    # Top of the tree node, deformed circle scalated
    treeTop4Node = sg.SceneGraphNode("tree top 4 {}".format(i))
    treeTop4Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(3*math.pi/4),tr.scale(top_scale, top_scale, 1)])
    treeTop4Node.childs = [gpuGreenTop]

    # Top of the tree node, deformed circle scalated
    treeTop5Node = sg.SceneGraphNode("tree top 5 {}".format(i))
    treeTop5Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(-math.pi),tr.scale(top_scale, top_scale, 1)])
    treeTop5Node.childs = [gpuGreenTop]

    # Top of the tree node, deformed circle scalated
    treeTop6Node = sg.SceneGraphNode("tree top 5 {}".format(i))
    treeTop6Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(-math.pi/4),tr.scale(top_scale, top_scale, 1)])
    treeTop6Node.childs = [gpuGreenTop]

    # Top of the tree node, deformed circle scalated
    treeTop7Node = sg.SceneGraphNode("tree top 5 {}".format(i))
    treeTop7Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(-math.pi/2),tr.scale(top_scale, top_scale, 1)])
    treeTop7Node.childs = [gpuGreenTop]

    # Top of the tree node, deformed circle scalated
    treeTop8Node = sg.SceneGraphNode("tree top 5 {}".format(i))
    treeTop8Node.transform = tr.matmul([tr.translate(0, top_translate, 0), tr.rotationZ(-3*math.pi/4),tr.scale(top_scale, top_scale, 1)])
    treeTop8Node.childs = [gpuGreenTop]

    # Node that contains the movement of the tops
    shearingTopsNode = sg.SceneGraphNode("tops shearing {}".format(i))
    shearingTopsNode.childs = [treeTopNode, treeTop2Node, treeTop3Node, treeTop4Node, treeTop5Node, treeTop6Node, treeTop7Node, treeTop8Node]

    # Log tree node, brown quad scalated
    treeLogNode = sg.SceneGraphNode("tree log {}".format(i))
    treeLogNode.transform = tr.matmul([tr.scale(0.07, 0.2, 1)])
    treeLogNode.childs = [gpuBrownQuad]

    # Tree node with the figures created
    treeNode = sg.SceneGraphNode("tree {}".format(i))
    treeNode.childs = [treeLogNode, shearingTopsNode]
    return treeNode


def createScene(pipeline):
    # Creates the background

    # Create shapes in GPU
    gpuGreenTop = createGPUShape(createColorTreeTop(15, 0.125, 0.705, 0.094), pipeline, GL_DYNAMIC_DRAW) # Green top shape
    gpuGrayQuad = createGPUShape(createColorQuad(0.4, 0.4, 0.4), pipeline) # Gray quad shape
    gpuWhiteQuad = createGPUShape(createColorQuad(1,1,1), pipeline) # White quad shape
    gpuBrownQuad = createGPUShape(createColorQuad(0.43,0.31,0.18), pipeline) # Brown quad shape
    gpuGreenQuad = createGPUShape(createColorQuad(0.100, 0.500, 0.090), pipeline) # Green quad shape

    # Create some trees and group them
    treesList = []
    for i in range(4):
        newTree = createTree(gpuGreenTop, gpuBrownQuad, i)
        newTree.transform = tr.matmul([tr.translate(0, i/2, 0), tr.translate(0.82, -0.82, 0), tr.scale(1, 0.7, 1)])
        treesList.append(newTree)
    
    for i in range(3):
        newTree = createTree(gpuGreenTop, gpuBrownQuad, i+4)
        newTree.transform = tr.matmul([tr.translate(0, i/2, 0), tr.translate(-0.82, -0.82, 0), tr.scale(1, 0.7, 1)])
        treesList.append(newTree)

    treesNode = sg.SceneGraphNode("trees")
    treesNode.childs = treesList

    # Highway node
    highwayNode = sg.SceneGraphNode("highway")
    highwayNode.transform = tr.matmul([tr.scale(1.2, 4, 1)])
    highwayNode.childs = [gpuGrayQuad]

    # Grass Node
    grassNode = sg.SceneGraphNode("grass")
    grassNode.transform = tr.matmul([tr.scale(4, 4, 1)])
    grassNode.childs = [gpuGreenQuad]

    # Highway's line Node
    lineNode = sg.SceneGraphNode("line 1")
    lineNode.transform = tr.matmul([tr.translate(0, -0.5, 0), tr.scale(0.02, 0.5, 1)])
    lineNode.childs = [gpuWhiteQuad]

    # Highway's line 2 Node
    line2Node = sg.SceneGraphNode("line 2")
    line2Node.transform = tr.matmul([tr.translate(0, 0.5, 0), tr.scale(0.02, 0.5, 1)])
    line2Node.childs = [gpuWhiteQuad]

    # Node with highway's lines
    linesNode = sg.SceneGraphNode("lines")
    linesNode.childs = [line2Node, lineNode]

    # Right bordes line node
    borderLineNode = sg.SceneGraphNode("border line 1")
    borderLineNode.transform = tr.matmul([tr.translate(0.6, 0, 0), tr.scale(0.02, 4, 1)])
    borderLineNode.childs = [gpuWhiteQuad]

    # Left bordes line node
    borderLine2Node = sg.SceneGraphNode("border line 2")
    borderLine2Node.transform = tr.matmul([tr.translate(-0.6, 0, 0), tr.scale(0.02, 4, 1)])
    borderLine2Node.childs = [gpuWhiteQuad]

    # Border lines node
    borderLinesNode = sg.SceneGraphNode("border lines")
    borderLinesNode.childs = [borderLine2Node, borderLineNode]

    # Central background node with all the created nodes
    backGroundNode = sg.SceneGraphNode("background")
    backGroundNode.childs = [grassNode, highwayNode, linesNode, borderLinesNode, treesNode]

    # Father node of the scene
    sceneNode = sg.SceneGraphNode("world")
    sceneNode.childs = [backGroundNode]

    return sceneNode



