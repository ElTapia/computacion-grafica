""" Ejercicio 5 [Drive simulator] """

import glfw
import OpenGL.GL.shaders
import numpy as np
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from shapes import *
from model import *


# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# Clase controlador con variables para manejar el estado de ciertos botones
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.is_w_pressed = False
        self.is_s_pressed = False
        self.is_a_pressed = False
        self.is_d_pressed = False


# we will use the global controller as communication with the callback function
controller = Controller()

# This function will be executed whenever a key is pressed or released
def on_key(window, key, scancode, action, mods):
    
    global controller
    
    # Caso de detectar la tecla [W], actualiza estado de variable
    if key == glfw.KEY_W:
        if action ==glfw.PRESS:
            controller.is_w_pressed = True
        elif action == glfw.RELEASE:
            controller.is_w_pressed = False

    # Caso de detectar la tecla [S], actualiza estado de variable
    if key == glfw.KEY_S:
        if action ==glfw.PRESS:
            controller.is_s_pressed = True
        elif action == glfw.RELEASE:
            controller.is_s_pressed = False

    # Caso de detectar la tecla [A], actualiza estado de variable
    if key == glfw.KEY_A:
        if action ==glfw.PRESS:
            controller.is_a_pressed = True
        elif action == glfw.RELEASE:
            controller.is_a_pressed = False

    # Caso de detectar la tecla [D], actualiza estado de variable
    if key == glfw.KEY_D:
        if action ==glfw.PRESS:
            controller.is_d_pressed = True
        elif action == glfw.RELEASE:
            controller.is_d_pressed = False

    # Caso de detecar la barra espaciadora, se cambia el metodo de dibujo
    if key == glfw.KEY_SPACE and action ==glfw.PRESS:
        controller.fillPolygon = not controller.fillPolygon

    # Caso en que se cierra la ventana
    elif key == glfw.KEY_ESCAPE and action ==glfw.PRESS:
        glfw.set_window_should_close(window, True)



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    # Creating a glfw window
    width = 800
    height = 800
    title = "Ejercicio 5 - Drive simulator"
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE,       glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Pipeline para dibujar shapes con colores interpolados
    pipeline = es.SimpleTransformShaderProgram()
    # Pipeline para dibujar shapes con texturas
    tex_pipeline = es.SimpleTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Grafo de escena del auto
    car = createCar(pipeline) 
    # Grafo de escena del background
    mainScene = createScene(pipeline)
    # Se a??ade el auto a la escena principal
    mainScene.childs += [car]

    # Se instancia el modelo
    player = Player(1)
    # Se indican las referencias del nodo y el controller al modelo
    player.set_model(mainScene)
    player.set_controller(controller)

    # Shape con textura de la carga
    garbage = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "sprites/bag.png")


    # Se crean cuatro nodos de carga
    garbage1Node = sg.SceneGraphNode("garbage1")
    garbage1Node.childs = [garbage]

    garbage2Node = sg.SceneGraphNode("garbage2")
    garbage2Node.childs = [garbage]

    garbage3Node = sg.SceneGraphNode("garbage3")
    garbage3Node.childs = [garbage]

    garbage4Node = sg.SceneGraphNode("garbage4")
    garbage4Node.childs = [garbage]

    # Se crean el grafo de escena con textura y se agregan las cargas
    tex_scene = sg.SceneGraphNode("textureScene")
    tex_scene.childs = [garbage1Node, garbage2Node, garbage3Node, garbage4Node]

    # Posici??n cargas
    y = np.array([-0.55, -0.75])
    index = np.random.randint(0, 2, 4)
    new_y = y[index]
    y1, y2, y3, y4 = new_y

    # Se crean los modelos de la carga, se indican su nodo y se actualiza
    carga1 = Carga(0, y1, 0.1)
    carga1.set_model(garbage1Node)
    carga1.update()

    carga2 = Carga(0, y2, 0.1)
    carga2.set_model(garbage2Node)
    carga2.update()

    carga3 = Carga(0, y3, 0.1)
    carga3.set_model(garbage3Node)
    carga3.update()

    carga4 = Carga(0, y4, 0.1)
    carga4.set_model(garbage4Node)
    carga4.update()

    # Lista con todas las cargas
    cargas = [carga1, carga2, carga3, carga4]

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

        # Actualiza posici??n fondo
        player.pos[0]-=0.003
        player.pos[1]-=0.003
        player.pos[2]-=0.003

        # Actualiza posicion cargas
        carga1.pos[0] = player.pos[0]-0.5
        carga2.pos[0] = player.pos[1]+1
        carga3.pos[0] = player.pos[1]+1.4
        carga4.pos[0] = player.pos[2]+0.3

        carga1.update()
        carga2.update()
        carga3.update()
        carga4.update()

        if carga4.pos[0]-0.39 > 3.4:
            index = np.random.randint(0, 2, 4)
            new_y = y[index]
            y1, y2, y3, y4 = new_y

            carga1.pos[1] = y1
            carga2.pos[1] = y2
            carga3.pos[1] = y3
            carga4.pos[1] = y4

            carga1.update()
            carga2.update()
            carga3.update()
            carga4.update()

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Se llama al metodo del player para detectar colisiones
        player.collision(cargas)
        # Se llama al metodo del player para actualizar su posicion
        player.update(delta)

        # Se crea el movimiento de giro del rotor
        rotor = sg.findNode(mainScene, "rtRotor")
        rotor.transform = tr.rotationZ(t1)

        # Se dibuja el grafo de escena principal
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(mainScene, pipeline, "transform")

        # Se dibuja el grafo de escena con texturas
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    mainScene.clear()
    tex_scene.clear()

    glfw.terminate()