
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
from grafica.assets_path import *
from obj_reader import *


# Convenience function to ease initialization
def createGPUShape(pipeline, shape, draw = GL_DYNAMIC_DRAW):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, draw)
    return gpuShape


def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape


def createSceneSkybox(pipeline):
    shapeStadium = bs.createTextureNormalsCube('estadio.jpg')
    gpuStadium = createGPUShape(pipeline, shapeStadium, GL_STATIC_DRAW)
    gpuStadium.texture = es.textureSimpleSetup(
        getAssetPath("estadio.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    skybox = sg.SceneGraphNode("skybox")
    skybox.transform = tr.matmul([tr.translate(0, 0, 24.8), tr.scale(1, 2, 1), tr.uniformScale(70)])
    skybox.childs += [gpuStadium]
    return skybox


def createFloor(pipeline):
    shapeFloor = bs.createTextureNormalsQuad(1,1)
    gpuFloor = createGPUShape(pipeline, shapeFloor, GL_STATIC_DRAW)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("cancha.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.matmul([tr.translate(0, 0, -0.38),tr.scale(70, 140, 1), tr.rotationZ(np.pi/2)])
    floor.childs += [gpuFloor]

    return floor


# Create every model part from obj files
def create3DModel(pipeline, tex_pipeline):

# Create Shapes
###########################################################################
    # Create head obj and shape
    headShape = readOBJ(getObjPath('head.obj'),  (0.4, 0.3, 0.2))
    gpuHead = createGPUShape(pipeline, headShape)

    # Create right arm and hand obj and shape
    armHandShape = readTexOBJ(getObjPath('brazo_y_mano.obj'), "piel.png")
    gpuArmHand = createTextureGPUShape(armHandShape, tex_pipeline, getAssetPath("piel.png"))

    # Create right forearm and hand obj and shape
    forearmShape = readTexOBJ(getObjPath('antebrazo.obj'), "camiseta_inv.png")
    gpuForearm = createTextureGPUShape(forearmShape, tex_pipeline, getAssetPath("camiseta_inv.png"))

    # Create right foot and hand obj and shape
    footShape = readTexOBJ(getObjPath('pie.obj'), "camiseta.png")
    gpuFoot = createTextureGPUShape(footShape, tex_pipeline, getAssetPath("camiseta_inv.png"))

    # Create right thigh and hand obj and shape
    thighShape = readTexOBJ(getObjPath('muslo.obj'), "camiseta.png")
    gpuThigh = createTextureGPUShape(thighShape, tex_pipeline, getAssetPath("camiseta_inv.png"))

    # Create body obj and shape
    bodyShape = readTexOBJ(getObjPath('torso.obj'), "camiseta.png")
    gpuBody = createTextureGPUShape(bodyShape, tex_pipeline, getAssetPath("camiseta_inv.png"))


# Model scene graph
###########################################################################

    headNode = sg.SceneGraphNode("head")
    headNode.transform = tr.matmul([tr.translate(0, -0.3, 9.4), tr.rotationX(np.pi/2), tr.uniformScale(1.4)])
    headNode.childs += [gpuHead]

    rotateHeadNode = sg.SceneGraphNode("rotate head")
    rotateHeadNode.transform = tr.matmul([tr.rotationZ(0)])
    rotateHeadNode.childs += [headNode]

    z_arms = -2.6
    rightArmNode = sg.SceneGraphNode("right arm")
    rightArmNode.transform = tr.matmul([tr.translate(-0.1, -0.1, z_arms), tr.rotationX(np.pi/2),  tr.rotationY(np.pi/2), tr.scale(1, 1, -1)])
    rightArmNode.childs += [gpuArmHand]

    # Movimiento del antebrazo derecho
    rotateRightArmNode = sg.SceneGraphNode("rotate right arm")
    rotateRightArmNode.transform = tr.matmul([tr.rotationX(0), tr.rotationY(0), tr.rotationZ(0)])
    rotateRightArmNode.childs += [rightArmNode]

    leftArmNode = sg.SceneGraphNode("left arm")
    leftArmNode.transform = tr.matmul([tr.translate(-0.1, -0.1, z_arms), tr.rotationX(np.pi/2), tr.rotationY(np.pi/2)])
    leftArmNode.childs += [gpuArmHand]

    # Movimiento del antebrazo izquierdo
    rotateLeftArmNode = sg.SceneGraphNode("rotate left arm")
    rotateLeftArmNode.transform = tr.matmul([tr.rotationX(0), tr.rotationY(0),  tr.rotationZ(0)])
    rotateLeftArmNode.childs += [leftArmNode]

    x_forearms = 2.2
    rightForearmNode = sg.SceneGraphNode("right forearm")
    rightForearmNode.transform = tr.matmul([tr.rotationX(np.pi/2), tr.uniformScale(0.8)])
    rightForearmNode.childs += [gpuForearm]

    # Nodo del brazo derecho
    completeRightArmNode = sg.SceneGraphNode("complete right arm")
    completeRightArmNode.transform = tr.matmul([tr.translate(0, 0, -2.4)])
    completeRightArmNode.childs += [rightForearmNode, rotateRightArmNode]

    # Movimiento del brazo derecho
    rotateCompleteRightArmNode = sg.SceneGraphNode("rotate complete right arm")
    rotateCompleteRightArmNode.transform = tr.matmul([tr.rotationX(0), tr.rotationY(0), tr.rotationZ(0)])
    rotateCompleteRightArmNode.childs += [completeRightArmNode]

    translateCompleteRightArmNode = sg.SceneGraphNode("translate complete right arm")
    translateCompleteRightArmNode.transform = tr.matmul([tr.translate(-x_forearms, 0, 2.2)])
    translateCompleteRightArmNode.childs += [rotateCompleteRightArmNode]

    leftForearmNode = sg.SceneGraphNode("left forearm")
    leftForearmNode.transform = tr.matmul([tr.rotationX(np.pi/2), tr.uniformScale(0.8)])
    leftForearmNode.childs += [gpuForearm]

    completeLeftArmNode = sg.SceneGraphNode("complete left arm")
    completeLeftArmNode.transform = tr.matmul([tr.translate(0, 0, -2.4)])
    completeLeftArmNode.childs += [leftForearmNode, rotateLeftArmNode]

    # Movmiento del brazo izquierdo
    rotateCompleteLeftArmNode = sg.SceneGraphNode("rotate complete left arm")
    rotateCompleteLeftArmNode.transform = tr.matmul([tr.rotationX(0), tr.rotationY(0), tr.rotationZ(0)])
    rotateCompleteLeftArmNode.childs += [completeLeftArmNode]

    translateCompleteLeftArmNode = sg.SceneGraphNode("translate complete left arm")
    translateCompleteLeftArmNode.transform = tr.matmul([tr.translate(x_forearms, 0, 2.2)])
    translateCompleteLeftArmNode.childs += [rotateCompleteLeftArmNode]

    bodyNode = sg.SceneGraphNode("body")
    bodyNode.transform = tr.matmul([tr.translate(0, 0, 2), tr.rotationX(np.pi/2)])
    bodyNode.childs += [gpuBody]

    footNode = sg.SceneGraphNode("foot")
    footNode.transform = tr.matmul([tr.translate(0.05, -0.4, -4.3),  tr.rotationX(np.pi/2), tr.scale(1, 1, 0.8)])
    footNode.childs += [gpuFoot]

    thighNode = sg.SceneGraphNode("thigh")
    thighNode.transform = tr.matmul([tr.translate(0, 0, -3.2), tr.rotationX(np.pi/2)])
    thighNode.childs += [gpuThigh]

    # Movimiento del pie izquierdo
    rotateLeftFootNode = sg.SceneGraphNode("rotate left foot")
    rotateLeftFootNode.transform = tr.matmul([tr.rotationX(0), tr.rotationY(0), tr.rotationZ(0)])
    rotateLeftFootNode.childs += [footNode]

    translateLeftFootNode = sg.SceneGraphNode("translate left foot")
    translateLeftFootNode.transform = tr.matmul([tr.translate(0, 0, -3.4)])
    translateLeftFootNode.childs += [rotateLeftFootNode]

    x_leg = 0.8
    z_leg = 7.5

    leftThighNode = sg.SceneGraphNode("left thigh")
    leftThighNode.childs += [thighNode]

    completeLeftLegNode = sg.SceneGraphNode("complete left leg")
    completeLeftLegNode.childs += [leftThighNode, translateLeftFootNode]

    # Movimiento de la pierna izquierda
    rotateCompleteLeftLegNode = sg.SceneGraphNode("rotate complete left leg")
    rotateCompleteLeftLegNode.transform = tr.matmul([tr.rotationY(0), tr.rotationX(0), tr.rotationZ(0)])
    rotateCompleteLeftLegNode.childs += [completeLeftLegNode]

    translateCompleteLeftLegNode = sg.SceneGraphNode("translate complete left leg")
    translateCompleteLeftLegNode.transform = tr.matmul([tr.translate(x_leg, 0, z_leg)])
    translateCompleteLeftLegNode.childs += [rotateCompleteLeftLegNode]

    # Movimiento del pie derecho
    rotateRightFootNode = sg.SceneGraphNode("rotate right foot")
    rotateRightFootNode.transform = tr.matmul([tr.rotationX(0), tr.rotationY(0), tr.rotationZ(0)])
    rotateRightFootNode.childs += [footNode]

    translateRightFootNode = sg.SceneGraphNode("translate right foot")
    translateRightFootNode.transform = tr.matmul([tr.translate(0, 0, -3.4)])
    translateRightFootNode.childs += [rotateRightFootNode]

    rightThighNode = sg.SceneGraphNode("right thigh")
    rightThighNode.childs += [thighNode]

    completeRightLegNode = sg.SceneGraphNode("complete right leg")
    completeRightLegNode.childs += [rightThighNode, translateRightFootNode]

    # Movimiento de la pierna derecha
    rotateCompleteRightLegNode = sg.SceneGraphNode("rotate complete right leg")
    rotateCompleteRightLegNode.transform = tr.matmul([tr.rotationY(0), tr.rotationX(0), tr.rotationZ(0)])
    rotateCompleteRightLegNode.childs += [completeRightLegNode]

    translateCompleteRightLegNode = sg.SceneGraphNode("translate complete right leg")
    translateCompleteRightLegNode.transform = tr.matmul([tr.translate(-x_leg, 0, z_leg)])
    translateCompleteRightLegNode.childs += [rotateCompleteRightLegNode]

    armsNode = sg.SceneGraphNode("arms")
    armsNode.transform = tr.matmul([tr.translate(0, 0, 4.8)])
    armsNode.childs += [translateCompleteLeftArmNode, translateCompleteRightArmNode]

    upperBodyNode = sg.SceneGraphNode("upper body")
    upperBodyNode.transform = tr.matmul([tr.translate(0, 0, 6)])
    upperBodyNode.childs += [bodyNode, armsNode]

    legsNode = sg.SceneGraphNode("legs")
    legsNode.childs += [translateCompleteLeftLegNode, translateCompleteRightLegNode]

    modelNode = sg.SceneGraphNode("model")
    modelNode.childs += [upperBodyNode, legsNode]

    jumpModelNode = sg.SceneGraphNode("jump model")
    jumpModelNode.transform = tr.matmul([tr.translate(0, 0, 0)])
    jumpModelNode.childs += [modelNode]

    completeModel = sg.SceneGraphNode("complete model")
    completeModel.childs += [rotateHeadNode, jumpModelNode]

    return completeModel

