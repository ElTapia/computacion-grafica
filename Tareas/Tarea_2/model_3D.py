
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

# Create Shapes
###########################################################################
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

# Model scene graph
###########################################################################

    headNode = sg.SceneGraphNode("head")
    headNode.transform = tr.matmul([tr.translate(0, -0.3, 9.4), tr.rotationX(np.pi/2), tr.uniformScale(1.4)])
    headNode.childs = [gpuHead]

    z_arms = -2.6
    rightArmNode = sg.SceneGraphNode("right arm")
    rightArmNode.transform = tr.matmul([tr.translate(-0.1, -0.1, z_arms), tr.rotationX(np.pi/2),  tr.rotationY(np.pi/2), tr.scale(1, 1, -1)])
    rightArmNode.childs = [gpuArmHand]

    #TODO: Insertar curva theta aca
    rotateRightArmNode = sg.SceneGraphNode("rotate right arm")
    rotateRightArmNode.transform = tr.matmul([tr.rotationY(0), tr.rotationX(0)])
    rotateRightArmNode.childs = [rightArmNode]

    leftArmNode = sg.SceneGraphNode("left arm")
    leftArmNode.transform = tr.matmul([tr.translate(-0.1, -0.1, z_arms), tr.rotationX(np.pi/2), tr.rotationY(np.pi/2)])
    leftArmNode.childs = [gpuArmHand]

    #TODO: Insertar curva theta aca
    rotateLeftArmNode = sg.SceneGraphNode("rotate left arm")
    rotateLeftArmNode.transform = tr.matmul([tr.rotationY(0), tr.rotationX(0)])
    rotateLeftArmNode.childs = [leftArmNode]

    x_forearms = 2.2
    rightForearmNode = sg.SceneGraphNode("right forearm")
    rightForearmNode.transform = tr.matmul([tr.rotationX(np.pi/2), tr.uniformScale(0.8)])
    rightForearmNode.childs = [gpuForearm]

    completeRightArmNode = sg.SceneGraphNode("complete right arm")
    completeRightArmNode.transform = tr.matmul([tr.translate(0, 0, -2.4)])
    completeRightArmNode.childs = [rightForearmNode, rotateRightArmNode]

    #TODO: Insertar curva theta aca
    rotateCompleteRightArmNode = sg.SceneGraphNode("rotate complete right arm")
    rotateCompleteRightArmNode.transform = tr.matmul([tr.translate(-x_forearms, 0, 2.2), tr.rotationX(-np.pi/2), tr.rotationY(np.pi/2)])
    rotateCompleteRightArmNode.childs = [completeRightArmNode]

    leftForearmNode = sg.SceneGraphNode("left forearm")
    leftForearmNode.transform = tr.matmul([tr.rotationX(np.pi/2), tr.uniformScale(0.8)])
    leftForearmNode.childs = [gpuForearm]

    completeLeftArmNode = sg.SceneGraphNode("complete left arm")
    completeLeftArmNode.transform = tr.matmul([tr.translate(0, 0, -2.4)])
    completeLeftArmNode.childs = [leftForearmNode, rotateLeftArmNode]

    #TODO: Insertar curva theta aca
    rotateCompleteLeftArmNode = sg.SceneGraphNode("rotate complete left arm")
    rotateCompleteLeftArmNode.transform = tr.matmul([tr.translate(x_forearms, 0, 2.2), tr.rotationX(-np.pi/2), tr.rotationY(-np.pi/2)])
    rotateCompleteLeftArmNode.childs = [completeLeftArmNode]

    bodyNode = sg.SceneGraphNode("body")
    bodyNode.transform = tr.matmul([tr.translate(0, 0, 2), tr.rotationX(np.pi/2)])
    bodyNode.childs = [gpuBody]

    footNode = sg.SceneGraphNode("foot")
    footNode.transform = tr.matmul([tr.translate(0.05, -0.4, -4.3), tr.scale(1, 0.8, 1), tr.rotationX(np.pi/2)])
    footNode.childs = [gpuFoot]

    thighNode = sg.SceneGraphNode("thigh")
    thighNode.transform = tr.matmul([tr.rotationY(-0.02), tr.translate(0, 0, -3.2), tr.rotationX(np.pi/2)])
    thighNode.childs = [gpuThigh]

    #TODO: Insertar curva theta aca
    rotateLeftFootNode = sg.SceneGraphNode("rotate left foot")
    rotateLeftFootNode.transform = tr.matmul([tr.translate(0, 0, -3.4), tr.rotationY(np.pi/8)])
    rotateLeftFootNode.childs = [footNode]

    x_leg = 0.8
    z_leg = 7.5

    leftThighNode = sg.SceneGraphNode("left thigh")
    leftThighNode.childs = [thighNode]

    completeLeftLegNode = sg.SceneGraphNode("complete left leg")
    completeLeftLegNode.childs = [leftThighNode, rotateLeftFootNode]

    #TODO: Insertar curva theta aca
    rotateCompleteLeftLegNode = sg.SceneGraphNode("rotate complete left leg")
    rotateCompleteLeftLegNode.transform = tr.matmul([tr.translate(x_leg, 0, z_leg), tr.rotationY(-np.pi/8)])
    rotateCompleteLeftLegNode.childs = [completeLeftLegNode]

    #TODO: Insertar curva theta aca
    rotateRightFootNode = sg.SceneGraphNode("rotate right foot")
    rotateRightFootNode.transform = tr.matmul([tr.translate(0, 0, -3.4), tr.rotationY(-np.pi/8)])
    rotateRightFootNode.childs = [footNode]

    rightThighNode = sg.SceneGraphNode("right thigh")
    rightThighNode.childs = [thighNode]

    completeRightLegNode = sg.SceneGraphNode("complete right leg")
    completeRightLegNode.childs = [rightThighNode, rotateRightFootNode]

    #TODO: Insertar curva theta aca
    rotateCompleteRightLegNode = sg.SceneGraphNode("rotate complete right leg")
    rotateCompleteRightLegNode.transform = tr.matmul([tr.translate(-x_leg, 0, z_leg), tr.rotationY(np.pi/8)])
    rotateCompleteRightLegNode.childs = [completeRightLegNode]

    armsNode = sg.SceneGraphNode("arms")
    armsNode.transform = tr.matmul([tr.translate(0, 0, 4.8)])
    armsNode.childs = [rotateCompleteLeftArmNode, rotateCompleteRightArmNode]

    upperBodyNode = sg.SceneGraphNode("upper body")
    upperBodyNode.transform = tr.matmul([tr.translate(0, 0, 6)])
    upperBodyNode.childs = [headNode, bodyNode, armsNode]

    legsNode = sg.SceneGraphNode("legs")
    legsNode.childs = [rotateCompleteLeftLegNode, rotateCompleteRightLegNode]

    modelNode = sg.SceneGraphNode("model")
    modelNode.childs = [upperBodyNode, legsNode]

    return modelNode
