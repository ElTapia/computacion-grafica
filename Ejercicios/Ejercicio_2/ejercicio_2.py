"""P5) [Efectos con Shaders] Realice un par de shaders, donde el primero solo dibuje los píxeles con un tono verde
 y el segundo represente un modo atardecer. Además agregue la funcionalidad de que se puedan alternar entre los shaders
apretando teclas. Con [Q] activa el primer efecto, y con [W] activa el segundo ejemplo"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from gpu_shape import GPUShape, SIZE_IN_BYTES

# A class to store the application control
class Controller:
    fillPolygon = True
    effect1 = False
    effect2 = False


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    elif key == glfw.KEY_Q:
        controller.effect1 = not controller.effect1

    elif key == glfw.KEY_W:
        controller.effect2 = not controller.effect2

    else:
        print('Unknown key')
    
# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices

# * Shader original

class SimpleShaderProgram:

    def __init__(self):

        vertex_shader = """
            #version 410

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                gl_Position = vec4(position, 1.0f);
                newColor = color;
            }
            """

        fragment_shader = """
            #version 410
            in vec3 newColor;

            out vec4 outColor;
            void main()
            {
                outColor = vec4(newColor, 1.0f);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color specification => 3*4 + 3*4 = 24 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

# * Shader noche
class NolightShaderProgram:

    def __init__(self):

        vertex_shader = """
            #version 410

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                gl_Position = vec4(position, 1.0f);
                newColor = color;
            }
            """

        fragment_shader = """
            #version 410
            in vec3 newColor;

            out vec4 outColor;
            void main()
            {
                vec3 finalColor = newColor;
                if (newColor.g < newColor.b +0.2|| newColor.r < newColor.b +0.2)
                {
                    finalColor = vec3(newColor.r*0.15, newColor.g*0.15, newColor.b*0.3);
                }
                outColor = vec4(finalColor, 1.0f);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color specification => 3*4 + 3*4 = 24 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

# * Shader atardecer
class SunsetShaderProgram:

    def __init__(self):

        vertex_shader = """
            #version 410

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                gl_Position = vec4(position, 1.0f);
                newColor = color;
            }
            """

        fragment_shader = """
            #version 410
            in vec3 newColor;

            out vec4 outColor;
            void main()
            {   
                vec3 finalColor = vec3((newColor.r + 0.4) , newColor.g + 0.2, newColor.b * 0.1 );
                outColor = vec4(finalColor, 1.0f);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color specification => 3*4 + 3*4 = 24 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

# * Cielo
def create_sky(y0, y1):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -1.0, y0, 0.0,  0.0, 1.0, 1.0,
         1.0, y0, 0.0,  0.0, 1.0, 1.0,
         1.0, y1, 0.0,  0.8, 1.0, 1.0,
        -1.0, y1, 0.0,  0.8, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)

# * ground
def create_ground(y0, y1):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -1.0, y0, 0.0,  0.54, 0.55, 0.55,
         1.0, y0, 0.0,  0.54, 0.55, 0.55,
         1.0, y1, 0.0,  0.23, 0.23, 0.23,
        -1.0, y1, 0.0,  0.23, 0.23, 0.23]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)

# * grass
def create_grass(y0, y1):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -1.0, y0, 0.0,  0.0, 0.66, 0.22,
         1.0, y0, 0.0,  0.0, 0.66, 0.22,
         1.0, y1, 0.0,  0.0, 0.76, 0.11,
        -1.0, y1, 0.0,  0.00, 0.76, 0.11]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)

# * Ovni
def create_ovni(x0, y0, width, height):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions                                    colors
         x0,         y0,                  0.0,  0.66, 0.66, 0.66,
         x0 + width/2,  y0 - height,      0.0,  0.66, 0.66, 0.66,
         x0 + width/2,  y0 - height *0.4, 0.0,  0.77, 0.77, 0.77,

         x0 + width/2,  y0 - height,      0.0,  0.99, 0.99, 0.99,
         x0 + width, y0,                  0.0,  0.99, 0.99, 0.99,
         x0 + width/2,  y0 - height *0.4, 0.0,  0.79, 0.79, 0.79,

         x0,         y0,                  0.0,  0.77, 0.77, 0.77,
         x0 + width/2,  y0 - height *0.4, 0.0,  0.66, 0.66, 0.66,
         x0 + width, y0,                  0.0,  0.66, 0.66, 0.66,

         # capsula                                       colors
         x0 + width/4,      y0 - height/10,     0.0,   0.77, 0.77, 0.77,
         x0 + width*0.65 ,  y0 + height * 0.5,  0.0,   0.55, 0.55, 0.55,
         x0 + width/3.3, y0 + height * 0.5,     0.0,   0.55, 0.55, 0.55,
         x0 + width*0.7,  y0 - height/10,       0.0,   0.77, 0.77, 0.77,]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices =  [0, 1, 2,
                3, 4, 5,
                6, 7, 8,
                9, 10, 11,
                9, 10, 12]

    return Shape(vertices, indices)


# * Montaña
def create_mountain(x0, y0, width, height):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
         x0, y0, 0.0,                       0.3, 0.15, 0.1,
         x0 + width, y0, 0.0,           0.3, 0.15, 0.1,
         x0 + width*0.5, y0 + height*1.25, 0.0,  0.6, 0.31, 0.17,

         x0 + width*0.4, y0 + height, 0.0,      1.0, 1.0, 1.0,
         x0 + width*0.6, y0 + height, 0.0,      1.0, 1.0, 1.0,
         x0 + width*0.4, y0 + height*0.8, 0.0,  1.0, 1.0, 1.0,
         x0 + width*0.6, y0 + height*0.8, 0.0,  1.0, 1.0, 1.0,
         x0 + width*0.5, y0 + height*1.25, 0.0,  1.0, 1.0, 1.0,]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                3, 4, 5,
                3, 4, 6,
                3, 4, 7]

    return Shape(vertices, indices)

# * edificio
def create_building(x0, y0, height, width=0.4):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        x0, y0,     0.0,  0.388, 0.388, 0.388,
        x0+width, y0, 0.0,  0.388, 0.388, 0.388,
        x0+width, y0+height, 0.0,  0.490, 0.490, 0.490,
        x0, y0+height,     0.0,  0.490, 0.490, 0.490,
        
        # ventanas        colors
        x0+width*0.2, y0+height*0.3, 0.0,        1, 1, 0,
        x0+width*0.4, y0+height*0.3, 0.0,        1, 1, 0,
        x0+width*0.4, y0+height*0.4, 0.0,   1, 1, 0,
        x0+width*0.2, y0+height*0.4, 0.0,   1, 1, 0,
        
        x0+width*0.6, y0+height*0.3, 0.0,        1, 1, 0,
        x0+width*0.8, y0+height*0.3, 0.0,        1, 1, 0,
        x0+width*0.8, y0+height*0.4, 0.0,   1, 1, 0,
        x0+width*0.6, y0+height*0.4, 0.0,   1, 1, 0,

        x0+width*0.6, y0+height*0.5, 0.0,        1, 1, 0,
        x0+width*0.8, y0+height*0.5, 0.0,        1, 1, 0,
        x0+width*0.8, y0+height*0.6, 0.0,   1, 1, 0,
        x0+width*0.6, y0+height*0.6, 0.0,   1, 1, 0,

        x0+width*0.2, y0+height*0.5, 0.0,        1, 1, 0,
        x0+width*0.4, y0+height*0.5, 0.0,        1, 1, 0,
        x0+width*0.4, y0+height*0.6, 0.0,   1, 1, 0,
        x0+width*0.2, y0+height*0.6, 0.0,   1, 1, 0,

        x0+width*0.2, y0+height*0.7, 0.0,        1, 1, 0,
        x0+width*0.4, y0+height*0.7, 0.0,        1, 1, 0,
        x0+width*0.4, y0+height*0.8, 0.0,   1, 1, 0,
        x0+width*0.2, y0+height*0.8, 0.0,   1, 1, 0,

        x0+width*0.6, y0+height*0.7, 0.0,        1, 1, 0,
        x0+width*0.8, y0+height*0.7, 0.0,        1, 1, 0,
        x0+width*0.8, y0+height*0.8, 0.0,   1, 1, 0,
        x0+width*0.6, y0+height*0.8, 0.0,   1, 1, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0,
                4, 5, 6,
                6, 7, 4,
                8, 9, 10,
                10, 11, 8,
                12, 13, 14,
                14, 15, 12,
                16, 17, 18,
                18, 19, 16,
                20, 21, 22,
                22, 23, 20,
                24, 25, 26,
                26, 27, 24]

    return Shape(vertices, indices)

# * carretera
def create_street(x0, y0, height):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        x0, y0, 0.0,        0.23, 0.23, 0.23,
         -x0, y0, 0.0,        0.23, 0.23, 0.23,
         -x0, y0*height, 0.0, 0.1, 0.1, 0.1,
        x0, y0*height, 0.0, 0.1, 0.1, 0.1,

    # Lineas divisorias calle        colors
        x0+0.1, y0+0.3, 0.0,        1, 1, 1,
        x0+0.4, y0+0.3, 0.0,        1, 1, 1,
        x0+0.4, y0*1.7*height, 0.0,   1, 1, 1,
        x0+0.1, y0*1.7*height, 0.0,   1, 1, 1,
        
        x0+0.6, y0+0.3, 0.0,        1, 1, 1,
        x0+0.9, y0+0.3, 0.0,        1, 1, 1,
        x0+0.9, y0*1.7*height, 0.0,   1, 1, 1,
        x0+0.6, y0*1.7*height, 0.0,   1, 1, 1,
        
        x0+1.1, y0+0.3, 0.0,        1, 1, 1,
        x0+1.4, y0+0.3, 0.0,        1, 1, 1,
        x0+1.4, y0*1.7*height, 0.0,   1, 1, 1,
        x0+1.1, y0*1.7*height, 0.0,   1, 1, 1,
        
        x0+1.6, y0+0.3, 0.0,        1, 1, 1,
        x0+1.9, y0+0.3, 0.0,        1, 1, 1,
        x0+1.9, y0*1.7*height, 0.0,   1, 1, 1,
        x0+1.6, y0*1.7*height, 0.0,   1, 1, 1]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0,
                4, 5, 6,
                6, 7, 4,
                8, 9, 10,
                10, 11, 8,
                12, 13, 14,
                14, 15, 12,
                16, 17, 18,
                18, 19, 16]

    return Shape(vertices, indices)


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE,       glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(width, height, "Ejercicio: Escena de edificios con montaña de fondo", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Setting up the clear screen color
    glClearColor(0.2, 0.2, 0.2, 1.0)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # * Creating our shader program and telling OpenGL to use it
    simplePipeline = SimpleShaderProgram()
    NolightPipeline = NolightShaderProgram()
    sunsetPipeline = SunsetShaderProgram()

    # * Creating shapes on GPU memory
    sky_shape = create_sky(y0=-0.2, y1=1.0)
    gpu_sky = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_sky)
    NolightPipeline.setupVAO(gpu_sky)
    sunsetPipeline.setupVAO(gpu_sky)
    gpu_sky.fillBuffers(sky_shape.vertices, sky_shape.indices, GL_STATIC_DRAW)

    ground_shape = create_ground(y0=-1.0, y1=-0.3)
    gpu_ground = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_ground)
    NolightPipeline.setupVAO(gpu_ground)
    sunsetPipeline.setupVAO(gpu_ground)
    gpu_ground.fillBuffers(ground_shape.vertices, ground_shape.indices, GL_STATIC_DRAW)

    street_shape = create_street(x0=-1.0, y0=-0.9, height=0.4)
    gpu_street = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_street)
    NolightPipeline.setupVAO(gpu_street)
    sunsetPipeline.setupVAO(gpu_street)
    gpu_street.fillBuffers(street_shape.vertices, street_shape.indices, GL_STATIC_DRAW)

    building_1_shape = create_building(x0=-0.8, y0=-0.3, height=0.7)
    gpu_building_1 = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_building_1)
    NolightPipeline.setupVAO(gpu_building_1)
    sunsetPipeline.setupVAO(gpu_building_1)
    gpu_building_1.fillBuffers(building_1_shape.vertices, building_1_shape.indices, GL_STATIC_DRAW)

    building_2_shape = create_building(x0=-0.2, y0=-0.3, height=1)
    gpu_building_2 = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_building_2)
    NolightPipeline.setupVAO(gpu_building_2)
    sunsetPipeline.setupVAO(gpu_building_2)
    gpu_building_2.fillBuffers(building_2_shape.vertices, building_2_shape.indices, GL_STATIC_DRAW)

    building_3_shape = create_building(x0=0.4, y0=-0.3, height=0.5)
    gpu_building_3 = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_building_3)
    NolightPipeline.setupVAO(gpu_building_3)
    sunsetPipeline.setupVAO(gpu_building_3)
    gpu_building_3.fillBuffers(building_3_shape.vertices, building_3_shape.indices, GL_STATIC_DRAW)

    grass_shape = create_grass(y0=-0.3, y1=0.0)
    gpu_grass = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_grass)
    NolightPipeline.setupVAO(gpu_grass)
    sunsetPipeline.setupVAO(gpu_grass)
    gpu_grass.fillBuffers(grass_shape.vertices, grass_shape.indices, GL_STATIC_DRAW)

    ovni_shape = create_ovni(x0=-0.8, y0=0.8, width=0.1, height=0.05)
    gpu_ovni = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_ovni)
    NolightPipeline.setupVAO(gpu_ovni)
    sunsetPipeline.setupVAO(gpu_ovni)
    gpu_ovni.fillBuffers(ovni_shape.vertices, ovni_shape.indices, GL_STATIC_DRAW)

    mountain_shape = create_mountain(x0=-0.5, y0=0.0, width=1, height=0.8)
    gpu_mountain = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_mountain)
    NolightPipeline.setupVAO(gpu_mountain)
    sunsetPipeline.setupVAO(gpu_mountain)
    gpu_mountain.fillBuffers(mountain_shape.vertices, mountain_shape.indices, GL_STATIC_DRAW)

# * Recordar cambiar figuras
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        if (controller.effect1):
            glUseProgram(NolightPipeline.shaderProgram)
            NolightPipeline.drawCall(gpu_sky)
            NolightPipeline.drawCall(gpu_ground)
            NolightPipeline.drawCall(gpu_street)
            NolightPipeline.drawCall(gpu_grass)
            NolightPipeline.drawCall(gpu_ovni)
            NolightPipeline.drawCall(gpu_mountain)
            NolightPipeline.drawCall(gpu_building_1)
            NolightPipeline.drawCall(gpu_building_2)
            NolightPipeline.drawCall(gpu_building_3)
        elif (controller.effect2):
            glUseProgram(sunsetPipeline.shaderProgram)
            sunsetPipeline.drawCall(gpu_sky)
            sunsetPipeline.drawCall(gpu_ground)
            sunsetPipeline.drawCall(gpu_street)
            sunsetPipeline.drawCall(gpu_grass)
            sunsetPipeline.drawCall(gpu_ovni)
            sunsetPipeline.drawCall(gpu_mountain)
            sunsetPipeline.drawCall(gpu_building_1)
            sunsetPipeline.drawCall(gpu_building_2)
            sunsetPipeline.drawCall(gpu_building_3)
        else:
            glUseProgram(simplePipeline.shaderProgram)
            simplePipeline.drawCall(gpu_sky)
            simplePipeline.drawCall(gpu_ground)
            simplePipeline.drawCall(gpu_street)
            simplePipeline.drawCall(gpu_grass)
            simplePipeline.drawCall(gpu_ovni)
            simplePipeline.drawCall(gpu_mountain)
            simplePipeline.drawCall(gpu_building_1)
            simplePipeline.drawCall(gpu_building_2)
            simplePipeline.drawCall(gpu_building_3)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpu_sky.clear()
    gpu_ground.clear()
    gpu_grass.clear()
    gpu_ovni.clear()
    gpu_mountain.clear()
    gpu_building_1.clear()
    gpu_building_2.clear()
    gpu_building_3.clear()
    gpu_street.clear()

    glfw.terminate()