
# * Tarea 1 Beauchefville
#TODO: Arreglar stop de personaje

import sys
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

# Inicializa parámetros

Z = int(sys.argv[1])
H = int(sys.argv[2])
T = int(sys.argv[3])
P = float(sys.argv[4])

print("Inicia el juego")
print("{} zombies".format(Z))
print("{} humanos".format(H))
print("{} segundos".format(T))
print("{} probabilidad de contagio".format(P))


#############################################################################

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
        self.stop = False  # Detiene el controlador al finalizar juego
        self.detector_glasses = False  #  Gafas detectoras de contagiados

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

    # Detiene al personaje
    if controller.stop:
        controller.is_d_pressed = False
        controller.is_a_pressed = False
        controller.is_w_pressed = False
        controller.is_s_pressed = False

    # Caso de detecar la barra espaciadora, se cambia el metodo de dibujo
    if key == glfw.KEY_SPACE and action ==glfw.PRESS:
        controller.detector_glasses = not controller.detector_glasses

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
    title = "Tarea 1 - Beauchefville"

    ########################## Extras para que funcione en MAC ################################

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    ############################################################################################

    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    ############################### Extra para que funcione en MAC ########################################

    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    #######################################################################################################

    # Pipelines para shapes con colores interpolados y texturas, respectivamente
    pipeline = es.SimpleTransformShaderProgram()
    tex_pipeline = es.SimpleTextureTransformShaderProgram()
    infected_pipeline = es.InfectedTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)


    # Grafo de escena del background
    # TODO: Redefinir createScene
    mainScene = createScene(pipeline)

    # Shapes con texturas
    hinata_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/hinata.png")
    zombie_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/zombie.png")
    human_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/kageyama.png")
    store_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/store.png")
    you_win_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/you_win.png")
    game_over_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/game_over.png")

    # Se crean nodos para cada shape
    hinataNode = sg.SceneGraphNode("hinata")
    hinataNode.childs = [hinata_png]

    storeNode = sg.SceneGraphNode("store")
    storeNode.childs = [store_png]

    you_winNode = sg.SceneGraphNode("win")
    you_winNode.transform = tr.matmul([tr.scale(0, 0, 0)])
    you_winNode.childs = [you_win_png]

    game_overNode = sg.SceneGraphNode("lose")
    game_overNode.transform = tr.matmul([tr.scale(0, 0, 0)])
    game_overNode.childs = [game_over_png]

    # Se instancia el modelo
    player = Player(0.2)

    # Se indican las referencias del nodo y el controller al modelo
    player.set_model(hinataNode)
    player.set_controller(controller)

    # Posición store
    x_store, y_store = -0.78, 0.8

    def spawn_humans(P, N, y_human, infectedHumans, notInfectedHumans):

        x_human = np.random.uniform(-0.58, 0.58, N)

        humans = np.empty(N, dtype=object)

        for i in range(N):
            humanNode = sg.SceneGraphNode("human")
            humanNode.childs = [human_png]

            human = Human(x_human[i], y_human, 0.2, P)
            human.set_model(humanNode)
            human.update()

            humans[i] = human

            if human.is_infected:
                infectedHumans.childs += [human.model]

            else:
                notInfectedHumans.childs += [human.model]

        return humans

    def spawn_zombies(P, N, y_zombie, zombiesNode):

        x_zombie = np.random.uniform(-0.58, 0.58, N)
        zombies = np.empty(N, dtype=object)

        for i in range(N):
            zombieNode = sg.SceneGraphNode("zombie")
            zombieNode.childs = [zombie_png]

            # Se crean los modelos de zombie, se indican su nodo y se actualiza
            zombie = Zombie(x_zombie[i], y_zombie, 0.35)
            zombie.set_model(zombieNode)
            zombie.update()

            zombies[i] = zombie
            zombiesNode.childs += [zombieNode]

        return zombies

    def entity_stop(entities):
        for entity in entities:
                    entity.stop = True

    infectedHumansNode = sg.SceneGraphNode("infected humans")
    notInfectedHumansNode = sg.SceneGraphNode("not infected humans")
    zombiesNode = sg.SceneGraphNode("zombies")

    store = Store(x_store, y_store, 0.5)
    store.set_model(storeNode)
    store.update()

    # Crea primeros humanos
    humans = spawn_humans(P, H, 0, infectedHumansNode, notInfectedHumansNode)
    # Crea primeros zombies
    zombies = spawn_zombies(P, Z, 0, zombiesNode)

    # Se crean el grafo de escena con textura y se agregan las cargas
    tex_scene = sg.SceneGraphNode("textureScene")
    tex_scene.childs = [zombiesNode, infectedHumansNode, notInfectedHumansNode, storeNode, hinataNode, you_winNode, game_overNode]

    def win():
        you_winNode.transform = tr.matmul([tr.scale(2, 2, 1)])
        player.update(0, True)
        entity_stop(zombies)
        entity_stop(humans)

    def lose():
        game_overNode.transform = tr.matmul([tr.scale(2, 2, 1)])
        player.update(0, True)
        entity_stop(zombies)
        entity_stop(humans)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    t_spawn = 0
    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

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

        if t_spawn is not None:
            t_spawn += 0.001
            if t_spawn >= T:
                t_spawn = 0

        # Si llega a la tienda, gana
        if player.collision_store(store):
            win()

        if t_spawn == 0:
            # Spawnea humanos despues de T segundos
            new_humans = spawn_humans(P, H, 0, infectedHumansNode, notInfectedHumansNode)
            humans = np.append(humans, new_humans)

            # Spawnea zombies despues de T segundos
            new_zombies = spawn_zombies(P, H, 0, zombiesNode)
            zombies = np.append(zombies, new_zombies)

        for human in humans:
            # Avanza humano
            human.update()
            # Ve si colisiona con humano infectado
            player.infected(human)

        for zombie in zombies:
            # Avanza zombie
            zombie.update()

            # Si toca un zombie, pierde
            if player.collision_zombie(zombie):
                t_spawn = None
                lose()


        # Se llama al metodo del player para actualizar su posicion
        player.update(delta)

        # Se dibuja el grafo de escena principal
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(mainScene, pipeline, "transform")

        # Se dibuja el grafo de escena con texturas
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")

        if controller.detector_glasses:
            glUseProgram(infected_pipeline.shaderProgram)
            sg.drawSceneGraphNode(infectedHumansNode, infected_pipeline, "transform")

            if player.is_infected:
                glUseProgram(infected_pipeline.shaderProgram)
                sg.drawSceneGraphNode(hinataNode, infected_pipeline, "transform")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    mainScene.clear()
    tex_scene.clear()

    glfw.terminate()