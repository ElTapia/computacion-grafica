# Script para almacenar los puntos y curvas de las distintas partes del modelo

import numpy as np
import grafica.ex_curves as cv

class ModelMovement:

    def __init__(self):
        self.rightArm = RightArmMovement()
        self.rightArm.set_points()

        self.leftArm = LeftArmMovement()
        self.leftArm.set_points()


    def update(self, t):
        self.rightArm.update(t)
        self.leftArm.update(t)


class RightArmMovement:

    def __init__(self):

        self.theta_x = 0
        self.theta_y = 0
        self.theta_z = 0

        self.points_theta_x = []
        self.points_theta_y = []
        self.points_theta_z = []

        self.times_theta_x = []
        self.times_theta_y = []
        self.times_theta_z = []

        self.curve = cv.evalCRCurveTime


    def set_points_theta_x(self):

        # puntos mov brazo derecho en eje x
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 4.5,   0,   0]]).T
        P3 = np.array([[5,     0,   0]]).T

        self.points_theta_x = [P0, P1, P2, P3]
        self.times_theta_x  = [0, 4.5]


    def set_points_theta_y(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,            0]]).T
        P1 = np.array([[ 0,     0,            0]]).T
        P2 = np.array([[ 1,     -np.pi/1.5,   0]]).T
        P3 = np.array([[ 1.5,   0,            0]]).T
        P4 = np.array([[ 2,     -np.pi/1.5,   0]]).T
        P5 = np.array([[ 2.5,   0,            0]]).T
        P6 = np.array([[ 3,     -np.pi/1.5,   0]]).T
        P7 = np.array([[ 3.5,   0,            0]]).T
        P8 = np.array([[ 4,     -np.pi/1.5,   0]]).T
        P9 = np.array([[ 4.5,   0,            0]]).T
        P10 = np.array([[5,     0,            0]]).T

        self.points_theta_y = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10]
        self.times_theta_y  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]


    def set_points_theta_z(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,         0]]).T
        P1 = np.array([[ 0,     0,         0]]).T
        P2 = np.array([[ 1,     np.pi/2,   0]]).T
        P3 = np.array([[ 3.5,   np.pi/2,   0]]).T
        P4 = np.array([[ 4.5,   0,         0]]).T
        P5 = np.array([[5,      0,         0]]).T

        self.points_theta_z = [P0, P1, P2, P3, P4, P5]
        self.times_theta_z  = [0, 1, 3.5, 4.5]


    def set_points(self):

        self.set_points_theta_x()
        self.set_points_theta_y()
        self.set_points_theta_z()


    def update_theta_x(self, t):
        self.theta_x = self.curve(t, self.points_theta_x, self.times_theta_x)[1]


    def update_theta_y(self, t):
        self.theta_y = self.curve(t, self.points_theta_y, self.times_theta_y)[1]


    def update_theta_z(self, t):
        self.theta_z = self.curve(t, self.points_theta_z, self.times_theta_z)[1]


    def update(self, t):
        self.update_theta_x(t)
        self.update_theta_y(t)
        self.update_theta_z(t)


class LeftArmMovement:

    def __init__(self):

        self.theta_x = 0
        self.theta_y = 0
        self.theta_z = 0

        self.points_theta_x = []
        self.points_theta_y = []
        self.points_theta_z = []

        self.times_theta_x = []
        self.times_theta_y = []
        self.times_theta_z = []

        self.curve = cv.evalCRCurveTime


    def set_points_theta_x(self):

        # puntos mov brazo derecho en eje x
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 4.5,   0,   0]]).T
        P3 = np.array([[5,      0,   0]]).T

        self.points_theta_x = [P0, P1, P2, P3]
        self.times_theta_x  = [0, 4.5]


    def set_points_theta_y(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[ -1,    0,          0]]).T
        P1 = np.array([[ 0,     0,          0]]).T
        P2 = np.array([[ 1,     0,          0]]).T
        P3 = np.array([[ 1.5,   np.pi/1.5,  0]]).T
        P4 = np.array([[ 2,     0,          0]]).T
        P5 = np.array([[ 2.5,   np.pi/1.5,  0]]).T
        P6 = np.array([[ 3,     0,          0]]).T
        P7 = np.array([[ 3.5,   np.pi/1.5,  0]]).T
        P8 = np.array([[ 4,     0,          0]]).T
        P9 = np.array([[4.5,    0,          0]]).T
        P10 = np.array([[5,     0,          0]]).T

        self.points_theta_y = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10]
        self.times_theta_y  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]


    def set_points_theta_z(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,         0]]).T
        P1 = np.array([[ 0,     0,         0]]).T
        P2 = np.array([[ 1,     -np.pi/2,   0]]).T
        P3 = np.array([[ 4,     -np.pi/2,   0]]).T
        P4 = np.array([[ 4.5,   0,         0]]).T
        P5 = np.array([[ 5,     0,         0]]).T

        self.points_theta_z = [P0, P1, P2, P3, P4, P5]
        self.times_theta_z  = [0, 1, 3.5, 4.5]


    def set_points(self):

        self.set_points_theta_x()
        self.set_points_theta_y()
        self.set_points_theta_z()


    def update_theta_x(self, t):
        self.theta_x = self.curve(t, self.points_theta_x, self.times_theta_x)[1]


    def update_theta_y(self, t):
        self.theta_y = self.curve(t, self.points_theta_y, self.times_theta_y)[1]


    def update_theta_z(self, t):
        self.theta_z = self.curve(t, self.points_theta_z, self.times_theta_z)[1]


    def update(self, t):
        self.update_theta_x(t)
        self.update_theta_y(t)
        self.update_theta_z(t)