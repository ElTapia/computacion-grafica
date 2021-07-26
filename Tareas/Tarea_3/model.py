import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import random
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.performance_monitor as pm
import shapes_3D as s3d
import grafica.scene_graph as sg
import ode_resolver as edo
import grafica.assets_path as ap

# Convenience function to ease initialization
def createGPUShape(pipeline, shape, draw=GL_DYNAMIC_DRAW):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, draw)
    return gpuShape

# Crea gpu de texturas
def createTextureGPUShape(shape, pipeline, path, draw=GL_DYNAMIC_DRAW):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, draw)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape


class Circle:

    def __init__(self, pipeline, position, velocity, CIRCLE_DISCRETIZATION, RADIUS, texture):
        shape = s3d.createTextureNormalSphere(CIRCLE_DISCRETIZATION)
        shadow_shape = bs.createTextureNormalsPlane("sombra.png")

        # addapting the size of the circle's vertices to have a circle
        # with the desired radius

        self.pipeline = pipeline
        self.gpuShape = createTextureGPUShape(shape, self.pipeline, ap.getAssetPath(texture))
        self.gpuShadowShape = createTextureGPUShape(shadow_shape, self.pipeline, ap.getAssetPath("sombra.png")) #Cambiar sombra

        self.position = position
        self.radius   = RADIUS
        self.velocity = velocity


    def action(self, deltaTime, mu, gravity):

        epsilon = 5e-3
        if np.fabs(self.velocity[0]) < epsilon:
            self.velocity[0] = 0.0
            self.position[0] += 0.0
            pass

        if np.fabs(self.velocity[1]) < epsilon:
            self.velocity[1] = 0
            self.position[1] += 0
            pass

        # Euler integration
        if self.velocity[0] >= 0:
            self.velocity[0] += deltaTime*(-mu)*gravity
            self.position[0] += deltaTime*self.velocity[0]

        # modified Euler integration
        elif self.velocity[0] < 0:
            z = [self.position[0], self.velocity[0]]

            def f(t, z):
                return np.array([z[1], (mu)*gravity])

            z = edo.modified_euler_step(f, deltaTime, 0, z)
            self.velocity[0] = z[1]
            self.position[0] = z[0]

        # RK4 integration
        if self.velocity[1] >= 0:
            z = [self.position[1], self.velocity[1]]

            def f(t, z):
                return np.array([z[1], (-mu)*gravity])

            z = edo.RK4_step(f, deltaTime, 0, z)
            self.velocity[1] = z[1]
            self.position[1] = z[0]

        # improved Euler integration
        elif self.velocity[1] < 0:
            z = [self.position[1], self.velocity[1]]

            def f(t, z):
                return np.array([z[1], (mu)*gravity])

            z = edo.improved_euler_step(f, deltaTime, 0, z)
            self.velocity[1] = z[1]
            self.position[1] = z[0]


    def draw(self, transformName):
        scaleFactor = 2 * self.radius
        glUniformMatrix4fv(glGetUniformLocation(self.pipeline.shaderProgram, transformName), 1, GL_TRUE,
            tr.matmul([tr.translate(self.position[0], self.position[1], 0.0), tr.uniformScale(scaleFactor), tr.rotationZ(np.pi)])
        )
        self.pipeline.drawCall(self.gpuShape)

        glUniformMatrix4fv(glGetUniformLocation(self.pipeline.shaderProgram, transformName), 1, GL_TRUE,
            tr.matmul([tr.translate(self.position[0], self.position[1], -self.radius+0.001-0.5), tr.uniformScale(scaleFactor)])
        )
        self.pipeline.drawCall(self.gpuShadowShape)


def rotate2D(vector, theta):
    """
    Direct application of a 2D rotation
    """
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        cos_theta * vector[0] - sin_theta * vector[1],
        sin_theta * vector[0] + cos_theta * vector[1],
        0
    ], dtype = np.float32)


def collide(circle1, circle2, c):
    """
    If there are a collision between the circles, it modifies the velocity of
    both circles in a way that preserves energy and momentum.
    """
    
    assert isinstance(circle1, Circle)
    assert isinstance(circle2, Circle)

    normal = circle2.position - circle1.position
    normal /= np.linalg.norm(normal)

    circle1MovingToNormal = np.dot(circle2.velocity, normal) > 0.0
    circle2MovingToNormal = np.dot(circle1.velocity, normal) < 0.0

    if not (circle1MovingToNormal and circle2MovingToNormal):

        # obtaining the tangent direction
        tangent = rotate2D(normal, np.pi/2.0)

        # Projecting the velocity vector over the normal and tangent directions
        # for both circles, 1 and 2.
        v1n = np.dot(circle1.velocity, normal) * normal + 0.001
        v1t = np.dot(circle1.velocity, tangent) * tangent

        v2n = np.dot(circle2.velocity, normal) * normal + 0.001
        v2t = np.dot(circle2.velocity, tangent) * tangent

        # swaping the normal components...
        circle1.velocity = (v1n * (1-c) + v2n * (1+c))/2 + v1t
        circle2.velocity = (v2n * (1-c) + v1n * (1+c))/2 + v2t


def areColliding(circle1, circle2):
    assert isinstance(circle1, Circle)
    assert isinstance(circle2, Circle)

    difference = circle2.position - circle1.position
    distance = np.linalg.norm(difference)
    collisionDistance = circle2.radius + circle1.radius
    return distance < collisionDistance

def collideWithHole(circles, circle, point, radius):
    d = np.linalg.norm(circle.position - point)
    if d < circle.radius + radius:
        circles.remove(circle)


def collideWithBorder(circle, border_width, border_height):

    offset = 0.028875
    # Right
    if circle.position[0] + circle.radius > border_width/2-offset:
        circle.velocity[0] = -abs(circle.velocity[0])

    # Left
    if circle.position[0] < -border_width/2+offset + circle.radius:
        circle.velocity[0] = abs(circle.velocity[0])

    # Top
    if circle.position[1] > border_height/2-offset - circle.radius:
        circle.velocity[1] = -abs(circle.velocity[1])

    # Bottom
    if circle.position[1] < -border_height/2+offset + circle.radius:
        circle.velocity[1] = abs(circle.velocity[1])


# Clase para manejar una camara que se mueve en coordenadas polares
class PolarCamera:
    def __init__(self):
        self.center = np.array([0.0, 0.0, -0.5]) # centro de movimiento de la camara y donde mira la camara
        self.theta = 0                           # coordenada theta, angulo de la camara
        self.rho = 1                             # coordenada rho, distancia al centro de la camara
        self.eye = np.array([0.0, 0.0, 0.0])     # posicion de la camara
        self.height = 2.0                        # altura fija de la camara
        self.can_shoot = True                   # Activa camara para lanzar bola blanca
        self.camera_to_up = False                # Posiciona cárama desde arriba
        self.camera_up = 4.0                     # altura cámara en vista desde arriba
        self.up = np.array([0, 0, 1])            # vector up
        self.viewMatrix = None                   # Matriz de vista
    
    # Añadir ángulo a la coordenada theta
    def set_theta(self, delta):
        self.theta = (self.theta + delta) % (np.pi * 2)

    # Añadir distancia a la coordenada rho, sin dejar que sea menor o igual a 0
    def set_rho(self, delta):
        if ((self.rho + delta) > 0.1):
            self.rho += delta

    def get_eye(self):
        return self.eye

    # Actualizar la matriz de vista
    def update_view(self, white_ball_pos):
        # Se calcula la posición de la camara con coordenadas poleras relativas al centro

        self.eye[0] = self.rho * np.sin(self.theta) + self.center[0]
        self.eye[1] = self.rho * np.cos(self.theta) + self.center[1]
        self.eye[2] = self.height + self.center[2]

        if self.camera_to_up:
            self.can_shoot = False
            self.center = np.array([0.0, 0.0, -0.5])
            self.eye[0] = 0
            self.eye[1] = 0.5
            self.eye[2] = self.camera_up + self.center[2]

        if self.can_shoot:
            self.center[0] = white_ball_pos[0]
            self.center[1] = white_ball_pos[1]
            self.center[2] = 0.1
            self.eye[2] = 0.2


        # Se genera la matriz de vista
        viewMatrix = tr.lookAt(
            self.eye,
            self.center,
            self.up
        )
        return viewMatrix


def create_skybox(pipeline):
    shapeSky = bs.createTextureNormalsCube('')
    gpuSky = createTextureGPUShape(shapeSky, pipeline, ap.getAssetPath("sides.png"), GL_STATIC_DRAW)
    
    #################################################################################################
    shapeSecondSky = bs.createTextureNormalsPlane('')
    gpuSecondSky = createTextureGPUShape(shapeSecondSky, pipeline, ap.getAssetPath("frente.png"), GL_STATIC_DRAW)
    ####################################################################################################

    shapeThirdSky = bs.createTextureNormalsPlane('')
    gpuThirdSky = createTextureGPUShape(shapeThirdSky, pipeline, ap.getAssetPath("back.png"), GL_STATIC_DRAW)
    ####################################################################################################

    shapeFourthSky = bs.createTextureNormalsPlane('')
    gpuFourthSky = createTextureGPUShape(shapeFourthSky, pipeline, ap.getAssetPath("floor.png"), GL_STATIC_DRAW)

    ####################################################################################################

    skybox = sg.SceneGraphNode("skybox")
    skybox.transform = tr.matmul([tr.translate(0, 0, 0.3), tr.uniformScale(2)])
    skybox.childs += [gpuSky]

    ##########################################################
    secondSky = sg.SceneGraphNode("second Sky")
    secondSky.transform = tr.matmul([tr.translate(-0.01, 0, 0.42), tr.rotationX(np.pi/2), tr.rotationY(np.pi/2), tr.uniformScale(2)])
    secondSky.childs += [gpuSecondSky]

    ##########################################################
    thirdSky = sg.SceneGraphNode("third Sky")
    thirdSky.transform = tr.matmul([tr.translate(0.01, 0, 0.5), tr.rotationX(np.pi/2), tr.rotationY(-np.pi/2), tr.uniformScale(2)])
    thirdSky.childs += [gpuThirdSky]

    ##########################################################
    fourthSky = sg.SceneGraphNode("fourth Sky")
    fourthSky.transform = tr.matmul([tr.translate(0, 0, -1.5), tr.uniformScale(2)])
    fourthSky.childs += [gpuFourthSky]

    newSkybox = sg.SceneGraphNode("new Skybox")
    newSkybox.transform = tr.matmul([tr.translate(0, 0, 0.5), tr.uniformScale(4)])
    newSkybox.childs += [skybox, secondSky, thirdSky, fourthSky]
    ############################################################

    return newSkybox


def create_scene(color_pipeline, tex_pipeline, width, height, radius):

    brown_cube = bs.createColorNormalsCube(0.4, 0.24, 0.16)
    gpu_brown_cube = createGPUShape(color_pipeline, brown_cube, GL_STATIC_DRAW)

    table_png = bs.createTextureNormalsPlane("mesa.png")
    gpu_table_png = createTextureGPUShape(table_png, tex_pipeline, ap.getAssetPath("mesa.png"))

    table_node = sg.SceneGraphNode("mesa")
    table_node.transform = tr.matmul([tr.translate(0, 0, -radius-0.17), tr.scale(width, height, 0.3)])
    table_node.childs += [gpu_brown_cube]

    borde1_node =  sg.SceneGraphNode("borde 1")
    borde1_node.transform = tr.matmul([tr.translate(0, height/2 + radius + 0.03, -0.15), tr.scale(width, height/20, 0.4)])
    borde1_node.childs += [gpu_brown_cube]

    borde2_node =  sg.SceneGraphNode("borde 2")
    borde2_node.transform = tr.matmul([tr.translate(0, -height/2 - radius - 0.03, -0.15), tr.scale(width, height/20, 0.4)])
    borde2_node.childs += [gpu_brown_cube]

    borde3_node =  sg.SceneGraphNode("borde 3")
    borde3_node.transform = tr.matmul([tr.translate(-width/2 - radius - 0.03, 0, -0.15), tr.scale(height/20, height+0.255, 0.4)])
    borde3_node.childs += [gpu_brown_cube]

    borde4_node =  sg.SceneGraphNode("borde 4")
    borde4_node.transform = tr.matmul([tr.translate(width/2 + radius + 0.03, 0, -0.15), tr.scale(height/20, height+0.255, 0.4)])
    borde4_node.childs += [gpu_brown_cube]

    borders_node = sg.SceneGraphNode("bordes")
    borders_node.childs += [borde1_node, borde2_node, borde3_node, borde4_node]


    table_cover_node = sg.SceneGraphNode("recubrimiento mesa")
    table_cover_node.childs += [gpu_table_png]

    scaled_table_cover = sg.SceneGraphNode("recubrimiento mesa escalada")
    scaled_table_cover.transform = tr.matmul([tr.translate(0, 0, -radius-0.25), tr.scale(width, height, 0.5)])
    scaled_table_cover.childs += [table_cover_node]

    skybox = create_skybox(tex_pipeline)

    tex_scene = sg.SceneGraphNode("Escena con texturas")
    tex_scene.childs += [scaled_table_cover, skybox]

    color_scene = sg.SceneGraphNode("Escena con colores")
    color_scene.childs += [table_node, borders_node]

    scene = sg.SceneGraphNode("Escena")
    scene.childs += [tex_scene, color_scene]
    return scene