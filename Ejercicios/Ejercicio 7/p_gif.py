""" Visualizacion de la escena mostrada en el gif de u-cursos """

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

# Clase para manejar una camara que se mueve en coordenadas polares
class PolarCamera:
    def __init__(self):
        self.center = np.array([0.0, 0.0, -0.5]) # centro de movimiento de la camara y donde mira la camara
        self.theta = 0                           # coordenada theta, angulo de la camara
        self.rho = 6                             # coordenada rho, distancia al centro de la camara
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
        self.showAxis = False

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

    # Se instancia un controller
    controller = Controller()
    # Se conecta el metodo on_key del controller para manejar el input del teclado
    glfw.set_key_callback(window, controller.on_key)

    # Different shader programs for different lighting strategies
    phongPipeline = ls.SimplePhongShaderProgram() 

    # This shader program does not consider lighting
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory

    # SPUShape de los ejes de referencia
    gpuAxis = createGPUShape(mvpPipeline, bs.createAxis(4))

    # Se cran los nodos, esferas se generan en shapes3d
    scene = createScene(phongPipeline)
    cube1 = createCube1(phongPipeline)
    cube2 = createCube2(phongPipeline)
    sphere = createSphereNode(0.5, 0.3, 0.3, phongPipeline)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()
    r = 0.5
    g = 0
    b = 0.25

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
        
        # Se actualiza la camara segun delta e internamente segun el input 
        controller.update_camera(delta)
        # Se obtiene la referencia de la camara
        camera = controller.get_camera() 
        # Se obtiene la matriz de vista actualizada 
        viewMatrix = camera.update_view()

        # Setting up the projection transform
        projection = tr.perspective(60, float(width) / float(height), 0.1, 100)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

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

        # Posicion de la fuente de luz que rota en el tiempo
        lightposition = [1.5*np.cos(t1), 1.5*np.sin(t1), 2.3]

        # valores de los coeficientes de eiluminacion que varian con el tiempo
        r = np.abs(((0.5*t1+0.00) % 2)-1)
        g = np.abs(((0.5*t1+0.33) % 2)-1)
        b = np.abs(((0.5*t1+0.66) % 2)-1)

        # Setting all uniform shader variables
        
        # Dibujar con el pipeline de ilumiacion normal
        glUseProgram(lightingPipeline.shaderProgram)

        # Entregar a los shaders los coeficientes de iluminacion ambiente, difuso y especular
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), r, g, b)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), r, g, b)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), r, g, b)

        # Entregar a los shaders los coeficientes de reflexion de los objetos ambiente, difuso y especular
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)

        # Entregar valores a los shaders de la posicion de luz, posicion de camara y shininess
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), lightposition[0], lightposition[1], lightposition[2])
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), camera.eye[0], camera.eye[1], camera.eye[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 10)
        
        # Entregar valores a los shaders los coeficientes de atenuacion
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        # Entregar valores a los shaders de las matrices para la proyeccion de la camara
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, viewMatrix)

        # Se dibujan los objetos
        sg.drawSceneGraphNode(scene, lightingPipeline, "model")
        sg.drawSceneGraphNode(cube1, lightingPipeline, "model")
        sg.drawSceneGraphNode(cube2, lightingPipeline, "model")
        sg.drawSceneGraphNode(sphere, lightingPipeline, "model")      
        
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    gpuAxis.clear()
    scene.clear()
    cube1.clear()
    cube2.clear()
    sphere.clear()

    glfw.terminate()