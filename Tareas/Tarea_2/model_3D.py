
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
    headShape = readOBJ(getAssetPath('head.obj'), (0.6, 0.9, 0.5))
    gpuHead = createGPUShape(pipeline, headShape)

    # Create right arm and hand obj and shape
    armHandShape = readOBJ(getAssetPath('brazo_y_mano.obj'), (0.6, 0.9, 0.5))
    gpuArmHand = createGPUShape(pipeline, armHandShape)

    # Create right forearm and hand obj and shape
    forearmShape = readOBJ(getAssetPath('antebrazo.obj'), (0.6, 0.9, 0.5))
    gpuForearm = createGPUShape(pipeline, forearmShape)

    # Create right foot and hand obj and shape
    footShape = readOBJ(getAssetPath('pie.obj'), (0.6, 0.9, 0.5))
    gpuFoot = createGPUShape(pipeline, footShape)

    # Create right thigh and hand obj and shape
    thighShape = readOBJ(getAssetPath('muslo.obj'), (0.6, 0.9, 0.5))
    gpuThigh = createGPUShape(pipeline, thighShape)

    # Create body obj and shape
    bodyShape = readOBJ(getAssetPath('torso.obj'), (0.6, 0.9, 0.5))
    gpuBody = createGPUShape(pipeline, bodyShape)


    headNode = sg.SceneGraphNode("head")
    headNode.childs = [gpuHead]

    leftArmNode = sg.SceneGraphNode("left arm")
    leftArmNode.transform = tr.matmul([tr.translate(0, 0, 0), tr.rotationX(np.pi/2), tr.rotationY(np.pi)])
    leftArmNode.childs = [gpuArmHand]

    leftForearmNode = sg.SceneGraphNode("left forearm")
    leftForearmNode.childs = [gpuForearm]

    rightArmNode = sg.SceneGraphNode("right arm")
    rightArmNode.childs = [gpuArmHand]

    rightForearmNode = sg.SceneGraphNode("right forearm")
    rightForearmNode.childs = [gpuForearm]

    bodyNode = sg.SceneGraphNode("body")
    bodyNode.childs = [gpuBody]

    leftThighNode = sg.SceneGraphNode("left thigh")
    leftThighNode.childs = [gpuThigh]

    leftFootNode = sg.SceneGraphNode("left foot")
    leftFootNode.childs = [gpuFoot]

    rightThighNode = sg.SceneGraphNode("right thigh")
    rightThighNode.childs = [gpuThigh]

    rightFootNode = sg.SceneGraphNode("right foot")
    rightFootNode.childs = [gpuFoot]

    forearmsNode = sg.SceneGraphNode("forearms")
    forearmsNode.childs = [leftForearmNode, rightForearmNode]

    armsNode = sg.SceneGraphNode("arms")
    armsNode.childs = [leftArmNode, rightArmNode]

    thighsNode = sg.SceneGraphNode("thighs")
    thighsNode.childs = [leftThighNode, rightThighNode]

    feetNode = sg.SceneGraphNode("feet")
    feetNode.childs = [leftFootNode, rightFootNode]

    modelNode = sg.SceneGraphNode("model")
    modelNode.childs = [headNode, forearmsNode, armsNode, bodyNode, thighsNode, feetNode]

    return modelNode
