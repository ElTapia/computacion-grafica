
# * Tarea 1 Beauchefville

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
import math

# Initialize parameters

Z = int(sys.argv[1])
H = int(sys.argv[2])
T = float(sys.argv[3])
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

# Controller class to drive states of some keys
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.is_w_pressed = False
        self.is_s_pressed = False
        self.is_a_pressed = False
        self.is_d_pressed = False
        self.stop = False              # Stops the controller when game is finished
        self.detector_glasses = False  # Detector glasses of infected people

# we will use the global controller as communication with the callback function
controller = Controller()

# This function will be executed whenever a key is pressed or released
def on_key(window, key, scancode, action, mods):
    
    global controller

    # Detects [W] key, update state
    if key == glfw.KEY_W:
        if action ==glfw.PRESS:
            controller.is_w_pressed = True
        elif action == glfw.RELEASE:
            controller.is_w_pressed = False

    # Detects [S] key, update state
    if key == glfw.KEY_S:
        if action ==glfw.PRESS:
            controller.is_s_pressed = True
        elif action == glfw.RELEASE:
            controller.is_s_pressed = False

    # Detects [A] key, update state
    if key == glfw.KEY_A:
        if action ==glfw.PRESS:
            controller.is_a_pressed = True
        elif action == glfw.RELEASE:
            controller.is_a_pressed = False

    # Detects [D] key, update state
    if key == glfw.KEY_D:
        if action ==glfw.PRESS:
            controller.is_d_pressed = True
        elif action == glfw.RELEASE:
            controller.is_d_pressed = False

    # Stops the player
    if controller.stop:
        controller.is_d_pressed = False
        controller.is_a_pressed = False
        controller.is_w_pressed = False
        controller.is_s_pressed = False

    # Space key activates detector glasses
    if key == glfw.KEY_SPACE and action ==glfw.PRESS:
        controller.detector_glasses = not controller.detector_glasses

    # Close the window
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

    ################################# Extras for Mac ##########################################
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

    ################################# Extra for Mac ###########################################
    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    #######################################################################################################

    # Pipelines for shapes with interpolated colors, textures and detector glasses
    pipeline = es.SimpleTransformShaderProgram()
    tex_pipeline = es.SimpleTextureTransformShaderProgram()
    infected_pipeline = es.InfectedTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Background scene graph
    mainScene = createScene(pipeline)

    # Shapes with textures
    hinata_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/hinata.png", GL_STREAM_DRAW)
    zombie_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/zombie.png", GL_DYNAMIC_DRAW)
    human_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/kageyama.png", GL_DYNAMIC_DRAW)
    store_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/store.png", GL_STATIC_DRAW)
    you_win_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/you_win.png", GL_DYNAMIC_DRAW)
    game_over_png = createTextureGPUShape(bs.createTextureQuad(1,1), tex_pipeline, "Sprites/game_over.png", GL_DYNAMIC_DRAW)

    # Nodes per shape
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

    # Initialize player
    player = Player(0.15)

    # Indicates controller and node references to model
    player.set_model(hinataNode)
    player.set_controller(controller)

###########################################################################################
    # Let define some auxiliar functions

    # Spawn N humans on screen and divide infected with not infected humans
    def spawn_humans(P, N, infectedHumans, notInfectedHumans):

        x_human = np.random.uniform(-0.58, 0.58, N)
        y_human = np.random.choice([-1.2, 1.2], N)

        infectedHumansList = []
        notInfectedHumansList = []

        for i in range(N):
            human = Human(x_human[i], y_human[i], 0.15, P)

            if human.is_infected:

                infectedHumanNode = sg.SceneGraphNode("infected human {}".format(i))
                infectedHumanNode.childs = [human_png]

                human.set_model(infectedHumanNode)
                human.update()

                infectedHumansList += [human]
                infectedHumans.childs += [infectedHumanNode]

            else:

                humanNode = sg.SceneGraphNode("human {}".format(i))

                humanNode.childs = [human_png]

                human.set_model(humanNode)
                human.update()

                notInfectedHumansList += [human]
                notInfectedHumans.childs += [humanNode]

        return infectedHumansList, notInfectedHumansList

    # Spawn N zombies on screen
    def spawn_zombies(N, zombiesNode):

        x_zombie = np.random.uniform(-0.58, 0.58, N)
        y_zombie = np.random.choice([-1.2, 1.2], N)

        zombies = np.empty(N, dtype=object)

        for i in range(N):
            zombieNode = sg.SceneGraphNode("zombie {}".format(i))
            zombieNode.childs = [zombie_png]

            # Se crean los modelos de zombie, se indican su nodo y se actualiza
            zombie = Zombie(x_zombie[i], y_zombie[i], 0.25)
            zombie.set_model(zombieNode)
            zombie.update()

            zombies[i] = zombie
            zombiesNode.childs += [zombieNode]

        return zombies


    # Stop all the entities that receive
    def entity_stop(entities):
        for entity in entities:
            entity.stop = True


    # Expands "you win" message
    def win(t):
        y_scale = t
        x_scale = t+0.2

        if 0 < t < 2.51:
            you_winNode.transform = tr.matmul([tr.scale(x_scale, y_scale, 1), tr.rotationZ(-t*10)])

        player.update(0, True)
        entity_stop(zombies)
        entity_stop(humans)


    # Expands "game over" message
    def lose(t):

        y_scale = t
        x_scale = t+0.2

        if 0 < t < 2.51:
            game_overNode.transform = tr.matmul([tr.scale(x_scale, y_scale, 1), tr.rotationZ(-t*10)])

        player.update(0, True)
        entity_stop(zombies)
        entity_stop(humans)

###############################################################################################

    # Set infected, not infected and zombies nodes
    infectedHumansNode = sg.SceneGraphNode("infected humans")
    notInfectedHumansNode = sg.SceneGraphNode("not infected humans")

    # Store Position
    x_store, y_store = -0.78, 0.8

    # Set store model with init position
    store = Store(x_store, y_store, 0.55)
    store.set_model(storeNode)
    store.update()

    # Create first H humans
    infectedHumans, notInfectedHumans = spawn_humans(P, H, infectedHumansNode, notInfectedHumansNode)
    humans = infectedHumans + notInfectedHumans

    # Crea First Z zombies
    zombiesNode = sg.SceneGraphNode("zombies")
    zombies = spawn_zombies(Z, zombiesNode)

    # Zombies are severe infected humans
    infectedHumansNode.childs += [zombiesNode]

    humansNode = sg.SceneGraphNode("humans")
    humansNode.childs = [infectedHumansNode, notInfectedHumansNode, hinataNode]

    # Create scene graph with textures and add elements
    tex_scene = sg.SceneGraphNode("textureScene")
    tex_scene.childs = [storeNode, humansNode]


    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Initialize spawn time for humans and zombies
    t_spawn = 0

    # Initialize time for lose
    t_lose = 0

    # Initialize time for win
    t_win = 0

    # Initialize time for infected player
    t_infected = 0

    # Application loop
    while not glfw.window_should_close(window):

        # Time variables
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

        # Se crea el movimiento de giro del rotor
        for i in range(6):
            top = sg.findNode(mainScene, "tops shearing {}".format(i))
            top.transform = tr.shearing(0.15*math.sin(t1*1.5), 0, 0, 0, 0, 0)

        # Resets time spawn when reach T
        if t_spawn is not None:
            t_spawn += delta
            if t_spawn >= T:
                t_spawn = 0

        # Reach store -> Win
        if player.collision_store(store):
            # Set time spawn to None to stop spawning entities
            t_infected = False
            t_spawn = None
            t_win += delta
            win(t_win)

        # Check some interactions for all humans on screen
        for human in humans:
            # Move human
            human.update()

        for human in notInfectedHumans:
            for infected_human in infectedHumans:
                # Check if human touch an infected human
                human.infected(infected_human)

                # Check if player touch an infected human
                player.infected(infected_human)

            for zombie in zombies:
                human.touch_zombie(zombie)

        for human in notInfectedHumans:
            if human.is_infected:
                infected = notInfectedHumans.pop(notInfectedHumans.index(human))
                infectedHumans += [infected]
                infectedHumansNode.childs += [human.model]

                humans = infectedHumans + notInfectedHumans

        if player.is_infected and t_infected is not None:
            t_infected += delta
            if t_infected >= T:
                t_infected = 0

        if player.prob_become_zombie(P) and t_infected==0:
            # Set time spawn to None to stop spawning entities
            t_infected = None

        if t_infected == None:
            t_spawn = None
            t_lose += delta
            lose(t_lose)


        # Check some zombie interactions
        for zombie in zombies:
            # Move zombie
            zombie.update()

            # If player touch a zombie -> Game over
            if player.collision_zombie(zombie):
                # Set time spawn to None to stop spawning entities
                t_spawn = None
                t_lose += delta
                lose(t_lose)

        # Time to spawn entities
        if t_spawn == 0:

            # Spawn humans after T seconds
            newInfectedHumans, newNotInfectedHumans = spawn_humans(P, H, infectedHumansNode, notInfectedHumansNode)
            infectedHumans += newInfectedHumans
            notInfectedHumans +=  newNotInfectedHumans
            humans = infectedHumans + notInfectedHumans

            # Spawn zombies after T seconds
            new_zombies = spawn_zombies(Z, zombiesNode)
            zombies = np.append(zombies, new_zombies)

        # Update player position
        player.update(delta)

        # Draw background scenegraph
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(mainScene, pipeline, "transform")

        # Draw texture scene graph
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(tex_scene, tex_pipeline, "transform")

        # Activates detector glasses
        if controller.detector_glasses:

            # Change color to green to infected humans
            glUseProgram(infected_pipeline.shaderProgram)
            sg.drawSceneGraphNode(infectedHumansNode, infected_pipeline, "transform")

            # Change player´s color if is infected
            if player.is_infected:
                glUseProgram(infected_pipeline.shaderProgram)
                sg.drawSceneGraphNode(sg.findNode(tex_scene, "hinata"), infected_pipeline, "transform")

        # Draw you win and game over
        glUseProgram(tex_pipeline.shaderProgram)
        sg.drawSceneGraphNode(you_winNode, tex_pipeline, "transform")
        sg.drawSceneGraphNode(game_overNode, tex_pipeline, "transform")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    mainScene.clear()
    tex_scene.clear()

    glfw.terminate()