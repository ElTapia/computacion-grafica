
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import grafica.basic_shapes as bs
import grafica.transformations as tr
import grafica.scene_graph as sg
import grafica.easy_shaders as es
from grafica.assets_path import getAssetPath
from obj_reader import *


# Convenience function to ease initialization
def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_DYNAMIC_DRAW)
    return gpuShape


# Create every model part from obj files
def create3DModel(pipeline):

    # Create head obj and shape
    headShape = readOBJ(getAssetPath('head.obj'), (0.4, 0.3, 0.2))
    gpuHead = createGPUShape(pipeline, headShape)

    # Create right arm and hand obj and shape
    armHandShape = readOBJ(getAssetPath('brazo_y_mano.obj'), (0.9, 0.8, 0.7))
    gpuArmHand = createGPUShape(pipeline, armHandShape)

    # Create right forearm and hand obj and shape
    forearmShape = readOBJ(getAssetPath('antebrazo.obj'), (1, 1, 1))
    gpuForearm = createGPUShape(pipeline, forearmShape)

    # Create right foot and hand obj and shape
    footShape = readOBJ(getAssetPath('pie.obj'), (0.1, 0.1, 0.1))
    gpuFoot = createGPUShape(pipeline, footShape)

    # Create right thigh and hand obj and shape
    thighShape = readOBJ(getAssetPath('muslo.obj'), (0.3, 0.3, 0.8))
    gpuThigh = createGPUShape(pipeline, thighShape)

    # Create body obj and shape
    bodyShape = readOBJ(getAssetPath('torso.obj'), (0.8, 0.2, 0.2))
    gpuBody = createGPUShape(pipeline, bodyShape)


    headNode = sg.SceneGraphNode("head")
    headNode.transform = tr.matmul([tr.translate(0, -0.3, 9.4), tr.rotationX(np.pi/2), tr.uniformScale(1.4)])
    headNode.childs = [gpuHead]

    x_arms = 3.6
    z_arms = -2.6
    leftArmNode = sg.SceneGraphNode("left arm")
    leftArmNode.transform = tr.matmul([tr.translate(0, 0, z_arms), tr.rotationX(np.pi/2),  tr.rotationY(np.pi/2), tr.scale(1, 1, -1)])
    leftArmNode.childs = [gpuArmHand]

    #TODO: Insertar curva theta aca
    rotateLeftArmNode = sg.SceneGraphNode("rotate left arm")
    rotateLeftArmNode.transform = tr.matmul([tr.translate(-x_arms, 0, 0), tr.rotationY(np.pi/8), tr.rotationX(0)])
    rotateLeftArmNode.childs = [leftArmNode]

    rightArmNode = sg.SceneGraphNode("right arm")
    rightArmNode.transform = tr.matmul([tr.translate(0, 0, z_arms), tr.rotationX(np.pi/2), tr.rotationY(np.pi/2)])
    rightArmNode.childs = [gpuArmHand]

    #TODO: Insertar curva theta aca
    rotateRightArmNode = sg.SceneGraphNode("rotate right arm")
    rotateRightArmNode.transform = tr.matmul([tr.translate(x_arms, 0, 0), tr.rotationY(-np.pi/8), tr.rotationX(0)])
    rotateRightArmNode.childs = [rightArmNode]

    x_forearms = 3.5
    leftForearmNode = sg.SceneGraphNode("left forearm")
    leftForearmNode.transform = tr.matmul([tr.rotationX(np.pi/2), tr.uniformScale(0.8)])
    leftForearmNode.childs = [gpuForearm]

    #TODO: Insertar curva theta aca
    rotateLeftForearmNode = sg.SceneGraphNode("rotate left forearm")
    rotateLeftForearmNode.transform = tr.matmul([tr.translate(-x_forearms, 0, 0), tr.rotationY(np.pi/5)])
    rotateLeftForearmNode.childs = [leftForearmNode]

    rightForearmNode = sg.SceneGraphNode("right forearm")
    rightForearmNode.transform = tr.matmul([tr.rotationX(np.pi/2), tr.uniformScale(0.8)])
    rightForearmNode.childs = [gpuForearm]

    #TODO: Insertar curva theta aca
    rotateRightForearmNode = sg.SceneGraphNode("rotate right forearm")
    rotateRightForearmNode.transform = tr.matmul([tr.translate(x_forearms, 0, 0), tr.rotationY(-np.pi/5)])
    rotateRightForearmNode.childs = [rightForearmNode]

    bodyNode = sg.SceneGraphNode("body")
    bodyNode.transform = tr.matmul([tr.translate(0, 0, 2), tr.rotationX(np.pi/2)])
    bodyNode.childs = [gpuBody]

    footNode = sg.SceneGraphNode("foot")
    footNode.transform = tr.matmul([tr.translate(0, -0.5, -4.3), tr.scale(1, 0.8, 1), tr.rotationX(np.pi/2)])
    footNode.childs = [gpuFoot]

    #TODO: Insertar curva theta aca
    rotateLeftFootNode = sg.SceneGraphNode("rotate left foot")
    rotateLeftFootNode.transform = tr.matmul([tr.translate(1.8, 0, 4.3), tr.rotationX(0)])
    rotateLeftFootNode.childs = [footNode]

    #TODO: Insertar curva theta aca
    rotateRightFootNode = sg.SceneGraphNode("rotate right foot")
    rotateRightFootNode.transform = tr.matmul([tr.translate(-1.8, 0, 4.3), tr.rotationX(0)])
    rotateRightFootNode.childs = [footNode]

    thighNode = sg.SceneGraphNode("thigh")
    thighNode.transform = tr.matmul([tr.translate(0, 0, -3.2), tr.rotationX(np.pi/2)])
    thighNode.childs = [gpuThigh]

    x_thigh = 0.8
    z_thigh = 7.5
    leftThighNode = sg.SceneGraphNode("left thigh")
    leftThighNode.transform = tr.matmul([tr.rotationY(-np.pi/10)])
    leftThighNode.childs = [thighNode]

    #TODO: Insertar curva theta aca
    rotateLeftThighNode = sg.SceneGraphNode("rotate left thigh")
    rotateLeftThighNode.transform = tr.matmul([tr.translate(x_thigh, 0, z_thigh), tr.rotationX(0)])
    rotateLeftThighNode.childs = [leftThighNode]

    rightThighNode = sg.SceneGraphNode("right thigh")
    rightThighNode.transform = tr.matmul([tr.rotationY(np.pi/10)])
    rightThighNode.childs = [thighNode]

    #TODO: Insertar curva theta aca
    rotateRightThighNode = sg.SceneGraphNode("rotate right thigh")
    rotateRightThighNode.transform = tr.matmul([tr.translate(-x_thigh, 0, z_thigh), tr.rotationX(0)])
    rotateRightThighNode.childs = [rightThighNode]

    forearmsNode = sg.SceneGraphNode("forearms")
    forearmsNode.transform = tr.matmul([tr.translate(0, 0, 4.8)])
    forearmsNode.childs = [rotateLeftForearmNode, rotateRightForearmNode]

    armsNode = sg.SceneGraphNode("arms")
    armsNode.transform = tr.matmul([tr.translate(0, 0, 4.8)])
    armsNode.childs = [rotateLeftArmNode, rotateRightArmNode]

    upperBodyNode = sg.SceneGraphNode("upper body")
    upperBodyNode.transform = tr.matmul([tr.translate(0, 0, 6)])
    upperBodyNode.childs = [headNode, bodyNode, forearmsNode, armsNode]

    thighsNode = sg.SceneGraphNode("thighs")
    thighsNode.childs = [rotateLeftThighNode, rotateRightThighNode]

    feetNode = sg.SceneGraphNode("feet")
    feetNode.childs = [rotateLeftFootNode, rotateRightFootNode]

    modelNode = sg.SceneGraphNode("model")
    modelNode.childs = [upperBodyNode, thighsNode, feetNode]

    return modelNode
