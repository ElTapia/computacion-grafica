# coding=utf-8
"""Tarea 3b: Pool party"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import random
import sys
import json
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.basic_shapes as bs
import grafica.lighting_shaders as ls
import grafica.transformations as tr
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from model import *

__author__ = "Sebastián Tapia"
__license__ = "MIT"

# Parameters

jsonFile = str(sys.argv[1])
configuration = open(jsonFile,)
params = json.load(configuration)

NUMBER_OF_CIRCLES = 16
CIRCLE_DISCRETIZATION = 20
RADIUS = 0.028875
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
BORDER_WIDTH = 1.46
BORDER_HEIGHT = 2.74
GRAVITY = 0.98

MU = params["fricción"]
C = params["restitución"]

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.useGravity = False

        # Variables para controlar la camara
        self.is_left_pressed = False
        self.is_right_pressed = False

        ###########################################################
        # Se crea instancia de la camara
        self.polar_camera = PolarCamera()
        ###########################################################

        self.heatMap = False

    # Entregar la referencia a la camara
    def get_camera(self):
        return self.polar_camera

    # Metodo para leer el input del teclado
    def on_key(self, window, key, scancode, action, mods):

        # Caso de detectar la tecla [RIGHT], actualiza estado de variable
        if key == glfw.KEY_RIGHT:
            if action == glfw.PRESS:
                self.is_right_pressed = True
            elif action == glfw.RELEASE:
                self.is_right_pressed = False

        # Caso de detectar la tecla [LEFT], actualiza estado de variable
        if key == glfw.KEY_LEFT:
            if action == glfw.PRESS:
                self.is_left_pressed = True
            elif action == glfw.RELEASE:
                self.is_left_pressed = False
        
        # Caso de detectar la barra espaciadora, se cambia el metodo de dibujo
        if key == glfw.KEY_SPACE:
            if action == glfw.PRESS:
                self.fillPolygon = not self.fillPolygon

        # Caso en que se cierra la ventana
        if key == glfw.KEY_ESCAPE:
            if action == glfw.PRESS:
                glfw.set_window_should_close(window, True)

        # Activa vista desde arriba
        if key == glfw.KEY_1:
            if action == glfw.PRESS:
                self.polar_camera.camera_to_up = not self.polar_camera.camera_to_up

        # Activa el heatMAp
        if key == glfw.KEY_TAB:
            if action == glfw.PRESS:
                controller.heatMap = not controller.heatMap


    #Funcion que recibe el input para manejar la camara y controlar sus coordenadas
    def update_camera(self, delta):

        # Camara rota a la izquierda
        if self.is_left_pressed and not self.polar_camera.camera_to_up:
            self.polar_camera.set_theta(-2 * delta)

        # Camara rota a la derecha
        if self.is_right_pressed and not self.polar_camera.camera_to_up:
            self.polar_camera.set_theta( 2 * delta)



# we will use the global controller as communication with the callback function
controller = Controller()

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit(1)

    # Creating a glfw window
    title = "Pool party"
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.SAMPLES, 4)
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Creating our shader program and telling OpenGL to use it
    color_pipeline = ls.MultiplePhongShaderProgram()
    normal_tex_pipeline = ls.MultipleTexturePhongShaderProgram()
    heatMap_tex_pipeline = ls.HeatMapTexturePhongShaderProgram()

    tex_pipeline = normal_tex_pipeline

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Creating shapes on GPU memory
    circles = []
    positions = []
    first_pos = np.array([0, -0.15, 0])
    first_row = [first_pos]

    second_pos = first_pos + np.array([RADIUS, -np.sqrt(3)*RADIUS, 0])
    third_pos = first_pos + np.array([-RADIUS, -np.sqrt(3)*RADIUS, 0])

    second_row = [second_pos, third_pos]

    fourth_pos = second_pos + np.array([RADIUS, -np.sqrt(3)*RADIUS, 0])
    fifth_pos = second_pos + np.array([-RADIUS, -np.sqrt(3)*RADIUS, 0])
    sixth_pos = third_pos + np.array([-RADIUS, -np.sqrt(3)*RADIUS, 0])

    third_row = [fourth_pos, fifth_pos, sixth_pos]

    seventh_pos = fourth_pos + np.array([RADIUS, -np.sqrt(3)*RADIUS, 0])
    eighth_pos = fourth_pos + np.array([-RADIUS, -np.sqrt(3)*RADIUS, 0])
    nineth_pos = fifth_pos + np.array([-RADIUS, -np.sqrt(3)*RADIUS, 0])
    tenth_pos = sixth_pos + np.array([-RADIUS, -np.sqrt(3)*RADIUS, 0])

    fourth_row = [seventh_pos, eighth_pos, nineth_pos, tenth_pos]

    eleventh_pos = seventh_pos + np.array([RADIUS, -np.sqrt(3)*RADIUS, 0])
    twelfth_pos = seventh_pos + np.array([-RADIUS, -np.sqrt(3)*RADIUS, 0])
    thirteenth_pos = eighth_pos + np.array([-RADIUS, -np.sqrt(3)*RADIUS, 0])
    fourteenth_pos = nineth_pos + np.array([-RADIUS, -np.sqrt(3)*RADIUS, 0])
    fifteenth_pos = tenth_pos + np.array([-RADIUS, -np.sqrt(3)*RADIUS, 0])

    fifth_row = [eleventh_pos, twelfth_pos, thirteenth_pos, fourteenth_pos, fifteenth_pos]

    positions += first_row + second_row + third_row + fourth_row + fifth_row

    textures = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png", "10.png",
                "11.png", "12.png", "13.png", "14.png", "15.png"]

    for i in range(1, NUMBER_OF_CIRCLES):
        position = positions[i-1]
        velocity = np.array([
            0.0,
            0.0,
            0.0
        ])
        texture = textures[i-1]
        circle = Circle(tex_pipeline, position, velocity, CIRCLE_DISCRETIZATION, RADIUS, texture=texture)
        circles += [circle]

    white_pos = np.array([0, 0.5, 0])
    white_velocity = np.array([0.0, 0.0, 0.0])
    white_ball = Circle(tex_pipeline, white_pos, white_velocity, CIRCLE_DISCRETIZATION, RADIUS, texture="white.png")

    offset = 0.1
    holes_radius = RADIUS
    hole1 = np.array([BORDER_WIDTH/2-offset, BORDER_HEIGHT/2-offset, 0])
    hole2 = np.array([BORDER_WIDTH/2-offset, -BORDER_HEIGHT/2+offset, 0])
    hole3 = np.array([-BORDER_WIDTH/2+offset, BORDER_HEIGHT/2-offset, 0])
    hole4 = np.array([-BORDER_WIDTH/2+offset, -BORDER_HEIGHT/2+offset, 0])
    hole5 = np.array([BORDER_WIDTH/2-offset,  0, 0])
    hole6 = np.array([-BORDER_WIDTH/2+offset, 0, 0])
    holes_pos = [hole1, hole2, hole3, hole4, hole5, hole6]

    scene = create_scene(color_pipeline, tex_pipeline, BORDER_WIDTH, BORDER_HEIGHT, RADIUS)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    # View and projection
    projection = tr.perspective(60, float(WINDOW_WIDTH)/float(WINDOW_HEIGHT), 0.1, 100)

    epsilon = 1e-1 # tolerancia disparo

    spotConcentration = 8
    spot_dir = [0, 0, -1]
    light_pos1 = [0, -3.5, 5] 
    light_pos2 = [0, 1.5, 3.2] 
    
    Ld1 = [0.7, 0.7, 0.7]
    Ld2 = [0.7, 0.7, 0.7]
    
    Ls1 = [1.0, 1.0, 1.0]
    Ls2 = [1.0, 1.0, 1.0]
    

    # Application loop
    while not glfw.window_should_close(window):

        can_shoot = True # switch para poder lanzar bola blanca

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        # Activa heatMap
        if controller.heatMap:
            tex_pipeline = heatMap_tex_pipeline
        else:
            tex_pipeline = normal_tex_pipeline

        # Using the time as the t parameter
        t = glfw.get_time()

        deltaTime = perfMonitor.getDeltaTime()
        delta = deltaTime

        controller.update_camera(delta)
        camera = controller.get_camera()
        viewMatrix = camera.update_view(white_ball.position)

        camera.can_shoot = can_shoot

        # Physics!
        for circle in circles:
            # moving each circle
            circle.action(deltaTime, MU, GRAVITY)

            # checking and processing collisions against the border
            collideWithBorder(circle, BORDER_WIDTH, BORDER_HEIGHT)
            for hole in holes_pos:
                collideWithHole(circles, circle, hole, holes_radius)

            if np.fabs(circle.velocity[0])> epsilon or np.fabs(circle.velocity[1]) > epsilon:
                can_shoot = False

        if np.fabs(white_ball.velocity[0])> epsilon or np.fabs(white_ball.velocity[1]) > epsilon:
            can_shoot = False

        if glfw.get_key(window, glfw.KEY_ENTER) == glfw.PRESS and can_shoot:
            forward_vector = (camera.center - camera.eye)/np.linalg.norm(camera.center - camera.eye)

            force = 3
            white_ball.velocity = np.array([force*forward_vector[0], force*forward_vector[1], 0.0])


        white_ball.action(deltaTime, MU, GRAVITY)
        collideWithBorder(white_ball, BORDER_WIDTH, BORDER_HEIGHT)

        # checking and processing collisions among circles
        for i in range(len(circles)):
            for j in range(i+1, len(circles)):
                if areColliding(circles[i], circles[j]):
                    collide(circles[i], circles[j], C)

            if areColliding(circles[i], white_ball):
                    collide(circles[i], white_ball, C)


        # Clearing the screen
        glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
        # Enabling transparencies

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Drawing (no texture)
        glUseProgram(color_pipeline.shaderProgram)

        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "spotDirection1"), spot_dir[0], spot_dir[1], spot_dir[2])
        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "spotDirection2"), spot_dir[0], spot_dir[1], spot_dir[2])

        glUniform1f(glGetUniformLocation(color_pipeline.shaderProgram, "spotConcentration"), spotConcentration)
    
        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "La"), 0.7, 0.7, 0.7)

        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "Ld1"), Ld1[0], Ld1[1], Ld1[2])
        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "Ld2"), Ld2[0], Ld2[1], Ld2[2])

        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "Ls1"), Ls1[0], Ls1[1], Ls1[2])
        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "Ls2"), Ls2[0], Ls2[1], Ls2[2])

        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "Ka"), 0.7, 0.7, 0.7)
        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "Kd"), 0.7, 0.7, 0.7)
        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "lightPosition0"), 0, -1, 50)
        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "lightPosition1"), 0, 1, 50)
        
        glUniform3f(glGetUniformLocation(color_pipeline.shaderProgram, "viewPosition"), camera.get_eye()[0], camera.get_eye()[1], camera.get_eye()[2])
        glUniform1ui(glGetUniformLocation(color_pipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(color_pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(color_pipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(color_pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(color_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(color_pipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)

        sg.drawSceneGraphNode(sg.findNode(scene, "Escena con colores"), color_pipeline, "model")


        # Drawing (texture)
        glUseProgram(tex_pipeline.shaderProgram)

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "spotDirection1"), spot_dir[0], spot_dir[1], spot_dir[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "spotDirection2"), spot_dir[0], spot_dir[1], spot_dir[2])

        glUniform1f(glGetUniformLocation(tex_pipeline.shaderProgram, "spotConcentration"), spotConcentration)
    
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "La"), 0.7, 0.7, 0.7)

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ld1"), Ld1[0], Ld1[1], Ld1[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ld2"), Ld2[0], Ld2[1], Ld2[2])

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ls1"), Ls1[0], Ls1[1], Ls1[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ls2"), Ls2[0], Ls2[1], Ls2[2])

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ka"), 0.7, 0.7, 0.7)
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Kd"), 0.7, 0.7, 0.7)
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "lightPosition0"), light_pos1[0], light_pos1[1], light_pos1[2])
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "lightPosition1"), light_pos2[0], light_pos2[1], light_pos2[2])
        
        glUniform3f(glGetUniformLocation(tex_pipeline.shaderProgram, "viewPosition"), camera.get_eye()[0], camera.get_eye()[1], camera.get_eye()[2])
        glUniform1ui(glGetUniformLocation(tex_pipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(tex_pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(tex_pipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(tex_pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(tex_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(tex_pipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)

        # drawing all the circles
        for i in range(len(circles)):
            circles[i].draw("model")

        white_ball.draw("model")
        tex_scene = sg.findNode(scene, "Escena con texturas")
        sg.drawSceneGraphNode(tex_scene, tex_pipeline, "model")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    for circle in circles:
        circle.gpuShape.clear()
    white_ball.gpuShape.clear()
    scene.clear()

    glfw.terminate()
