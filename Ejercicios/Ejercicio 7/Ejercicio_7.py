""" P2] Se presenta una escena con objetos dibujados con diferentes materiales a la escena base """
""" Se usa imgui para generar un menu y controlar variables de reflexion para el material de los objetos """

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.performance_monitor as pm
import grafica.lighting_shaders as ls
import grafica.scene_graph as sg
from shapes3d import *

import imgui
from imgui.integrations.glfw import GlfwRenderer

# Clase para manejar una camara que se mueve en coordenadas polares
class PolarCamera:
    def __init__(self):
        self.center = np.array([0.0, 0.0, -0.5]) # centro de movimiento de la camara y donde mira la camara
        self.theta = 0                           # coordenada theta, angulo de la camara
        self.rho = 5                             # coordenada rho, distancia al centro de la camara
        self.eye = np.array([0.0, 0.0, 0.0])     # posicion de la camara
        self.height = 0.5                        # altura fija de la camara
        self.up = np.array([0, 0, 1])            # vector up
        self.viewMatrix = None                   # Matriz de vista
    
    # Añadir ángulo a la coordenada theta
    def set_theta(self, delta):
        self.theta = (self.theta + delta) % (np.pi * 2)

    # Añadir distancia a la coordenada rho, sin dejar que sea menor o igual a 0
    def set_rho(self, delta):
        if ((self.rho + delta) > 0.1):
            self.rho += delta
    
    # Actualizar la matriz de vista
    def update_view(self):
        # Se calcula la posición de la camara con coordenadas poleras relativas al centro
        self.eye[0] = self.rho * np.sin(self.theta) + self.center[0]
        self.eye[1] = self.rho * np.cos(self.theta) + self.center[1]
        self.eye[2] = self.height + self.center[2]

        # Se genera la matriz de vista
        viewMatrix = tr.lookAt(
            self.eye,
            self.center,
            self.up
        )
        return viewMatrix

# Clase para manejar el controlador y la camara polar
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True

        # Variables para controlar la camara
        self.is_up_pressed = False
        self.is_down_pressed = False
        self.is_left_pressed = False
        self.is_right_pressed = False

        # Se crea instancia de la camara
        self.polar_camera = PolarCamera()

    # Entregar la referencia a la camara
    def get_camera(self):
        return self.polar_camera

    # Metodo para ller el input del teclado
    def on_key(self, window, key, scancode, action, mods):

        # Caso de detectar la tecla [UP], actualiza estado de variable
        if key == glfw.KEY_UP:
            if action == glfw.PRESS:
                self.is_up_pressed = True
            elif action == glfw.RELEASE:
                self.is_up_pressed = False

        # Caso de detectar la tecla [DOWN], actualiza estado de variable
        if key == glfw.KEY_DOWN:
            if action == glfw.PRESS:
                self.is_down_pressed = True
            elif action == glfw.RELEASE:
                self.is_down_pressed = False

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

        # Caso de detectar Control izquierdo, se cambia el metodo de dibujo
        elif key == glfw.KEY_LEFT_CONTROL:
            if action == glfw.PRESS:
                self.showAxis = not self.showAxis


    #Funcion que recibe el input para manejar la camara y controlar sus coordenadas
    def update_camera(self, delta):
        # Camara rota a la izquierda
        if self.is_left_pressed:
            self.polar_camera.set_theta(-2 * delta)

        # Camara rota a la derecha
        if self.is_right_pressed:
            self.polar_camera.set_theta( 2 * delta)
        
        # Camara se acerca al centro
        if self.is_up_pressed:
            self.polar_camera.set_rho(-5 * delta)

        # Camara se aleja del centro
        if self.is_down_pressed:
            self.polar_camera.set_rho(5 * delta)

def transformGuiOverlay(lightPos, ka, kd, ks):
    # Funcion para actualizar el menu

    # start new frame context
    imgui.new_frame()

    # open new window context
    imgui.begin("Material control", False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)

    # draw text label inside of current window
    imgui.text("Configuration sliders")

    # Posicion x de la fuente de luz
    edited, lightPos[0] = imgui.slider_float("light position X", lightPos[0], -2.3, 2.3)
    # Posicion y de la fuente de luz
    edited, lightPos[1] = imgui.slider_float("light position Y", lightPos[1], -2.3, 2.3)
    # Posicion z de la fuente de luz
    edited, lightPos[2] = imgui.slider_float("light position Z", lightPos[2], -2.3, 2.3)
    
    # Coeficiente de reflexion ambiental
    edited, ka = imgui.color_edit3("ka", ka[0], ka[1], ka[2])
    # Boton para reiniciar la reflexion ambiental
    if imgui.button("clean ka"):
        ka = (1.0, 1.0, 1.0)

    # Coeficiente de reflexion difusa
    edited, kd = imgui.color_edit3("kd", kd[0], kd[1], kd[2])
    # Boton para reiniciar la reflexion difusa
    if imgui.button("clean kd"):
        kd = (1.0, 1.0, 1.0)

    # Coeficiente de reflexion especular
    edited, ks = imgui.color_edit3("ks", ks[0], ks[1], ks[2])
    # Boton para reiniciar la reflexion especular
    if imgui.button("clean ks"):
        ks = (1.0, 1.0, 1.0)

    # close current window context
    imgui.end()

    # pass all drawing comands to the rendering pipeline
    # and close frame context
    imgui.render()
    imgui.end_frame()

    return lightPos, ka, kd, ks

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800
    title = "P0 - Scene"

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

     # Different shader programs for different lighting strategies
    phongPipeline = ls.SimplePhongShaderProgram()
    phongTexPipeline = ls.SimpleTexturePhongShaderProgram() # Pipeline para dibujar texturas

    # This shader program does not consider lighting
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = createGPUShape(mvpPipeline, bs.createAxis(4))

    scene = createScene(phongPipeline)

    R1 = 0.8         # Radio mayor 1
    r1 = 0.2         # Radio menor 1
    torus1 = createTexTorusNode1(phongTexPipeline, R1, r1)

    R2 = 0.6         # Radio mayor 2
    r2 = 0.3         # Radio menor 2
    torus2 = createTexTorusNode2(phongTexPipeline, R2, r2)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    # initilize imgui context (see documentation)
    imgui.create_context()
    impl = GlfwRenderer(window)

    # IMPORTANTE!! si usa imgui debe conectar los input con on_key despues de inicializar imgui, de lo contrario no funcionan los input 
    # Se instancia un controller
    controller = Controller()
    # Se conecta el metodo on_key del controller para manejar el input del teclado
    glfw.set_key_callback(window, controller.on_key)

    # valores que controlara el menu de imgui
    lightPos = [0, 0, 2.3]
    ka = [0.2, 0.2, 0.2] 
    kd = [0.5, 0.5, 0.5]
    ks = [1.0, 1.0, 1.0] 

    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1
        
        impl.process_inputs()
        # Using GLFW to check for input events
        glfw.poll_events()

        controller.update_camera(delta)
        camera = controller.get_camera()
        viewMatrix = camera.update_view()

        # Setting up the projection transform
        projection = tr.perspective(60, float(width) / float(height), 0.1, 100)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # imgui function
        lightPos, ka, kd, ks = \
            transformGuiOverlay(lightPos, ka, kd, ks)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # The axis is drawn without lighting effects
        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawCall(gpuAxis, GL_LINES)

        lightingPipeline = phongPipeline
        # Setting all uniform shader variables
        
        glUseProgram(lightingPipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 0.25, 0.25, 0.25)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), lightPos[0], lightPos[1], lightPos[2])
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)

        # Dibujo de la escena base
        sg.drawSceneGraphNode(scene, lightingPipeline, "model")

        # Se debe cambiara los coeficientes de reflexion si se quiere dibujar con otro material
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), ka[0], ka[1], ka[2])
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), kd[0], kd[1], kd[2])
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), ks[0], ks[1], ks[2])
        
        # Se dibuja la esfera normal
        #sg.drawSceneGraphNode(torus1, lightingPipeline, "model")
        #sg.drawSceneGraphNode(cube2, lightingPipeline, "model")
        #sg.drawSceneGraphNode(sphere, lightingPipeline, "model")
        
        # Pipeline para dibujar texturas
        glUseProgram(phongTexPipeline.shaderProgram)
        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "La"), 0.25, 0.25, 0.25)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ld"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "lightPosition"), lightPos[0], lightPos[1], lightPos[2])
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        glUniform1ui(glGetUniformLocation(phongTexPipeline.shaderProgram, "shininess"), 100)

        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(phongTexPipeline.shaderProgram, "quadraticAttenuation"), 0.01)
        
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ka"), ka[0], ka[1], ka[2])
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Kd"), kd[0], kd[1], kd[2])
        glUniform3f(glGetUniformLocation(phongTexPipeline.shaderProgram, "Ks"), ks[0], ks[1], ks[2])

        glUniformMatrix4fv(glGetUniformLocation(phongTexPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phongTexPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)

        sg.drawSceneGraphNode(torus1, phongTexPipeline, "model")
        sg.drawSceneGraphNode(torus2, phongTexPipeline, "model")
        
        # Drawing the imgui texture over our drawing
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        impl.render(imgui.get_draw_data())

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    gpuAxis.clear()
    impl.shutdown()
    scene.clear()
    #cube1.clear()
    #cube2.clear()
    #sphere.clear()
    torus1.clear()

    glfw.terminate()