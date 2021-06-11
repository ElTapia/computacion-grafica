# Script para almacenar los puntos y curvas de las distintas partes del modelo

from abc import ABC, abstractmethod
import numpy as np
import grafica.ex_curves as cv


class ModelMovement:

    def __init__(self):
        self.body = CompleteModel()
        self.body.set_points()
        
        self.rightArm = RightArmMovement()
        self.rightArm.set_points()

        self.completeRightArm = CompleteRightArmMovement()
        self.completeRightArm.set_points()

        self.leftArm = LeftArmMovement()
        self.leftArm.set_points()

        self.completeLeftArm = CompleteLeftArmMovement()
        self.completeLeftArm.set_points()

        self.rightLeg = RightLegMovement()
        self.rightLeg.set_points()

        self.rightFoot = RightFootMovement()
        self.rightFoot.set_points()

        self.leftLeg = LeftLegMovement()
        self.leftLeg.set_points()

        self.leftFoot = LeftFootMovement()
        self.leftFoot.set_points()


    def update(self, t):
        self.body.update(t)
        self.rightArm.update(t)
        self.completeRightArm.update(t)
        self.leftArm.update(t)
        self.completeLeftArm.update(t)
        self.rightLeg.update(t)
        self.rightFoot.update(t)
        self.leftLeg.update(t)
        self.leftFoot.update(t)


# Clase abstracta para agrupar piezas móviles
class AbstractPart(ABC):
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

        self.matrices_x = []
        self.matrices_y = []
        self.matrices_z = []

        self.curve = cv.evalCRCurveTime


    @abstractmethod
    def set_points_theta_x(self):
        pass


    @abstractmethod
    def set_points_theta_y(self):
        pass


    @abstractmethod
    def set_points_theta_z(self):
        pass


    def set_points(self):

        self.set_points_theta_x()
        self.set_points_theta_y()
        self.set_points_theta_z()


    def update_theta_x(self, t):
        self.theta_x = self.curve(t, self.matrices_x, self.times_theta_x)[1]


    def update_theta_y(self, t):
        self.theta_y = self.curve(t, self.matrices_y, self.times_theta_y)[1]


    def update_theta_z(self, t):
        self.theta_z = self.curve(t, self.matrices_z, self.times_theta_z)[1]


    def update(self, t):
        self.update_theta_x(t)
        self.update_theta_y(t)
        self.update_theta_z(t)


# Antebrazo y mano derecha
class RightArmMovement(AbstractPart):

    def __init__(self):
        super().__init__()


    def set_points_theta_x(self):

        # puntos mov brazo derecho en eje x
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 10,   0,   0]]).T
        P3 = np.array([[ 11,     0,   0]]).T

        self.points_theta_x = [P0, P1, P2, P3]
        self.matrices_x = cv.matricesCRCurve(self.points_theta_x)
        self.times_theta_x  = [0, 10]


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

        P10 = np.array([[ 5,     0,            0]]).T
        P11 = np.array([[ 5.5,   0,            0]]).T
        P12 = np.array([[ 6,     0,            0]]).T
        P13 = np.array([[ 6.5,   0,            0]]).T
        P14 = np.array([[ 7,     0,            0]]).T
        P15 = np.array([[ 7.5,   0,            0]]).T
        P16 = np.array([[ 8,     0,            0]]).T
        P17 = np.array([[ 8.5,   0,            0]]).T
        P18 = np.array([[ 9,     0,            0]]).T
        P19 = np.array([[ 9.5,   0,            0]]).T
        P20 = np.array([[ 10,    0,            0]]).T
        P21 = np.array([[ 11,    0,            0]]).T

        self.points_theta_y = [P0,  P1,  P2,  P3,  P4,  P5,  P6,  P7,  P8,  P9,
                               P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21]
        self.matrices_y = cv.matricesCRCurve(self.points_theta_y)

        self.times_theta_y  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                               5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]


    def set_points_theta_z(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,         0]]).T
        P1 = np.array([[ 0,     0,         0]]).T
        P2 = np.array([[ 1,     np.pi/2,   0]]).T
        P3 = np.array([[ 3.5,   np.pi/2,   0]]).T
        P4 = np.array([[ 4.5,   0,         0]]).T
        P5 = np.array([[10,      0,         0]]).T
        P6 = np.array([[11,      0,         0]]).T

        self.points_theta_z = [P0, P1, P2, P3, P4, P5, P6]
        self.matrices_z = cv.matricesCRCurve(self.points_theta_z)
        self.times_theta_z  = [0, 1, 3.5, 4.5, 10]


# Brazo completo derecho
class CompleteRightArmMovement(AbstractPart):

    def __init__(self):
        super().__init__()


    def set_points_theta_x(self):

        # puntos mov brazo derecho en eje x
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 10,   0,   0]]).T
        P3 = np.array([[11,     0,   0]]).T

        self.points_theta_x = [P0, P1, P2, P3]
        self.matrices_x = cv.matricesCRCurve(self.points_theta_x)
        self.times_theta_x  = [0, 10]


    def set_points_theta_y(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,           0]]).T
        P1 = np.array([[ 0,     0,           0]]).T
        P2 = np.array([[ 1,     np.pi/2,     0]]).T
        P3 = np.array([[ 2,     np.pi/2.2,     0]]).T
        P4 = np.array([[ 3,     np.pi/2.2,     0]]).T
        P5 = np.array([[ 4,     np.pi/2,     0]]).T
        P6 = np.array([[ 4.5,   0,           0]]).T
        P7 = np.array([[ 10,     0,           0]]).T
        P8 = np.array([[ 11,     0,           0]]).T
        

        self.points_theta_y = [P0, P1, P2, P3, P4, P5, P6, P7, P8]
        self.matrices_y = cv.matricesCRCurve(self.points_theta_y)
        self.times_theta_y  = [0, 1, 2, 3, 4, 4.5, 10]


    def set_points_theta_z(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 10,   0,   0]]).T
        P3 = np.array([[ 11,     0,   0]]).T

        self.points_theta_z = [P0, P1, P2, P3]
        self.matrices_z = cv.matricesCRCurve(self.points_theta_z)
        self.times_theta_z  = [0, 10]


# Antebrazo y mano izquierda
class LeftArmMovement(AbstractPart):

    def __init__(self):
        super().__init__()


    def set_points_theta_x(self):

        # puntos mov brazo derecho en eje x
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 10,   0,   0]]).T
        P3 = np.array([[11,      0,   0]]).T

        self.points_theta_x = [P0, P1, P2, P3]
        self.matrices_x = cv.matricesCRCurve(self.points_theta_x)
        self.times_theta_x  = [0, 10]


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

        P11 = np.array([[ 5.5,   0,            0]]).T
        P12 = np.array([[ 6,     0,            0]]).T
        P13 = np.array([[ 6.5,   0,            0]]).T
        P14 = np.array([[ 7,     0,            0]]).T
        P15 = np.array([[ 7.5,   0,            0]]).T
        P16 = np.array([[ 8,     0,            0]]).T
        P17 = np.array([[ 8.5,   0,            0]]).T
        P18 = np.array([[ 9,     0,            0]]).T
        P19 = np.array([[ 9.5,   0,            0]]).T
        P20 = np.array([[ 10,    0,            0]]).T
        P21 = np.array([[ 11,    0,            0]]).T

        self.points_theta_y = [P0,  P1,  P2,  P3,  P4,  P5,  P6,  P7,  P8,  P9,  P10,
                               P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21]
        self.matrices_y = cv.matricesCRCurve(self.points_theta_y)
        self.times_theta_y  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                                5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]


    def set_points_theta_z(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,         0]]).T
        P1 = np.array([[ 0,     0,         0]]).T
        P2 = np.array([[ 1,     -np.pi/2,   0]]).T
        P3 = np.array([[ 4,     -np.pi/2,   0]]).T
        P4 = np.array([[ 4.5,   0,         0]]).T
        P5 = np.array([[ 10,     0,         0]]).T
        P6 = np.array([[ 11,     0,         0]]).T

        self.points_theta_z = [P0, P1, P2, P3, P4, P5, P6]
        self.matrices_z = cv.matricesCRCurve(self.points_theta_z)
        self.times_theta_z  = [0, 1, 3.5, 4.5, 10]


# Brazo completo izquierdo
class CompleteLeftArmMovement(AbstractPart):

    def __init__(self):
        super().__init__()


    def set_points_theta_x(self):

        # puntos mov brazo derecho en eje x
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 10,   0,   0]]).T
        P3 = np.array([[11,     0,   0]]).T

        self.points_theta_x = [P0, P1, P2, P3]
        self.matrices_x = cv.matricesCRCurve(self.points_theta_x)
        self.times_theta_x  = [0, 10]


    def set_points_theta_y(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,           0]]).T
        P1 = np.array([[ 0,     0,           0]]).T
        P2 = np.array([[ 1,     -np.pi/2,     0]]).T
        P3 = np.array([[ 2,     -np.pi/2.2,     0]]).T
        P4 = np.array([[ 3,     -np.pi/2.2,     0]]).T
        P5 = np.array([[ 4,     -np.pi/2,     0]]).T
        P6 = np.array([[ 4.5,     0,           0]]).T
        P7 = np.array([[ 10,      0,           0]]).T
        P8 = np.array([[ 11,      0,           0]]).T

        self.points_theta_y = [P0, P1, P2, P3, P4, P5, P6, P7, P8]
        self.matrices_y = cv.matricesCRCurve(self.points_theta_y)
        self.times_theta_y  = [0, 1, 2, 3, 4, 4.5, 10]


    def set_points_theta_z(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 10,    0,   0]]).T
        P3 = np.array([[ 11,    0,   0]]).T

        self.points_theta_z = [P0, P1, P2, P3]
        self.matrices_z = cv.matricesCRCurve(self.points_theta_z)
        self.times_theta_z  = [0, 10]


# Pierna derecha
class RightLegMovement(AbstractPart):

    def __init__(self):

        super().__init__()


    def set_points_theta_x(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,            0]]).T
        P1 = np.array([[ 0,     0,            0]]).T
        P2 = np.array([[ 1,     -np.pi/4,   0]]).T
        P3 = np.array([[ 1.5,   0,            0]]).T
        P4 = np.array([[ 2,     -np.pi/4,   0]]).T
        P5 = np.array([[ 2.5,   0,            0]]).T
        P6 = np.array([[ 3,     -np.pi/4,   0]]).T
        P7 = np.array([[ 3.5,   0,            0]]).T
        P8 = np.array([[ 4,     -np.pi/4,   0]]).T
        P9 = np.array([[ 4.5,   0,            0]]).T
        P10 = np.array([[5,     0,            0]]).T

        P11 = np.array([[ 5.5,   0,            0]]).T
        P12 = np.array([[ 6,     0,            0]]).T
        P13 = np.array([[ 6.5,   0,            0]]).T
        P14 = np.array([[ 7,     0,            0]]).T
        P15 = np.array([[ 7.5,   0,            0]]).T
        P16 = np.array([[ 8,     0,            0]]).T
        P17 = np.array([[ 8.5,   0,            0]]).T
        P18 = np.array([[ 9,     0,            0]]).T
        P19 = np.array([[ 9.5,   0,            0]]).T
        P20 = np.array([[ 10,    0,            0]]).T
        P21 = np.array([[ 11,    0,            0]]).T

        self.points_theta_x = [P0,  P1,  P2,  P3,  P4,  P5,  P6,  P7,  P8,  P9,  P10,
                               P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21]
        self.matrices_x = cv.matricesCRCurve(self.points_theta_x)
        self.times_theta_x  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                                5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]


    def set_points_theta_y(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,            0]]).T
        P1 = np.array([[ 0,     0,            0]]).T
        P2 = np.array([[ 1,     np.pi/1.2,   0]]).T
        P3 = np.array([[ 1.5,   0,            0]]).T
        P4 = np.array([[ 2,     np.pi/1.2,   0]]).T
        P5 = np.array([[ 2.5,   0,            0]]).T
        P6 = np.array([[ 3,     np.pi/1.2,   0]]).T
        P7 = np.array([[ 3.5,   0,            0]]).T
        P8 = np.array([[ 4,     np.pi/1.2,   0]]).T
        P9 = np.array([[ 4.5,   0,            0]]).T
        P10 = np.array([[10,     0,            0]]).T
        P11 = np.array([[11,     0,            0]]).T

        self.points_theta_y = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11]
        self.matrices_y = cv.matricesCRCurve(self.points_theta_y)
        self.times_theta_y  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 10]

    def set_points_theta_z(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 10,    0,   0]]).T
        P3 = np.array([[ 11,     0,   0]]).T

        self.points_theta_z = [P0, P1, P2, P3]
        self.matrices_z = cv.matricesCRCurve(self.points_theta_z)
        self.times_theta_z  = [0, 10]


# Pie derecho
class RightFootMovement(AbstractPart):

    def __init__(self):

        super().__init__()


    def set_points_theta_x(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 10,   0,   0]]).T
        P3 = np.array([[ 11,     0,   0]]).T

        self.points_theta_x = [P0, P1, P2, P3]
        self.matrices_x = cv.matricesCRCurve(self.points_theta_x)
        self.times_theta_x  = [0, 10]


    def set_points_theta_y(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,            0]]).T
        P1 = np.array([[ 0,     0,            0]]).T
        P2 = np.array([[ 1,     -np.pi/1.2,   0]]).T
        P3 = np.array([[ 1.5,   0,            0]]).T
        P4 = np.array([[ 2,     -np.pi/1.2,   0]]).T
        P5 = np.array([[ 2.5,   0,            0]]).T
        P6 = np.array([[ 3,     -np.pi/1.2,   0]]).T
        P7 = np.array([[ 3.5,   0,            0]]).T
        P8 = np.array([[ 4,     -np.pi/1.2,   0]]).T
        P9 = np.array([[ 4.5,   0,            0]]).T
        P10 = np.array([[5,     0,            0]]).T

        P11 = np.array([[ 5.5,   0,            0]]).T
        P12 = np.array([[ 6,     0,            0]]).T
        P13 = np.array([[ 6.5,   0,            0]]).T
        P14 = np.array([[ 7,     0,            0]]).T
        P15 = np.array([[ 7.5,   0,            0]]).T
        P16 = np.array([[ 8,     0,            0]]).T
        P17 = np.array([[ 8.5,   0,            0]]).T
        P18 = np.array([[ 9,     0,            0]]).T
        P19 = np.array([[ 9.5,   0,            0]]).T
        P20 = np.array([[ 10,    0,            0]]).T
        P21 = np.array([[ 11,    0,            0]]).T

        self.points_theta_y = [P0,  P1,  P2,  P3,  P4,  P5,  P6,  P7,  P8,  P9,  P10,
                               P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21]
        self.matrices_y = cv.matricesCRCurve(self.points_theta_y)
        self.times_theta_y  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                                5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]


    def set_points_theta_z(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,            0]]).T
        P1 = np.array([[ 0,     0,            0]]).T
        P2 = np.array([[ 1,     -np.pi/2,   0]]).T
        P3 = np.array([[ 1.5,   0,            0]]).T
        P4 = np.array([[ 2,     -np.pi/2,   0]]).T
        P5 = np.array([[ 2.5,   0,            0]]).T
        P6 = np.array([[ 3,     -np.pi/2,   0]]).T
        P7 = np.array([[ 3.5,   0,            0]]).T
        P8 = np.array([[ 4,     -np.pi/2,   0]]).T
        P9 = np.array([[ 4.5,   0,            0]]).T
        P10 = np.array([[5,     0,            0]]).T

        P11 = np.array([[ 5.5,   0,            0]]).T
        P12 = np.array([[ 6,     0,            0]]).T
        P13 = np.array([[ 6.5,   0,            0]]).T
        P14 = np.array([[ 7,     0,            0]]).T
        P15 = np.array([[ 7.5,   0,            0]]).T
        P16 = np.array([[ 8,     0,            0]]).T
        P17 = np.array([[ 8.5,   0,            0]]).T
        P18 = np.array([[ 9,     0,            0]]).T
        P19 = np.array([[ 9.5,   0,            0]]).T
        P20 = np.array([[ 10,    0,            0]]).T
        P21 = np.array([[ 11,    0,            0]]).T

        self.points_theta_z = [P0,  P1,  P2,  P3,  P4,  P5,  P6,  P7,  P8,  P9,  P10,
                               P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21]
        self.matrices_z = cv.matricesCRCurve(self.points_theta_z)
        self.times_theta_z  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                                5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]


# Pierna izquierda
class LeftLegMovement(AbstractPart):

    def __init__(self):

        super().__init__()


    def set_points_theta_x(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,            0]]).T
        P1 = np.array([[ 0,     0,            0]]).T
        P2 = np.array([[ 1,     0,            0]]).T
        P3 = np.array([[ 1.5,   -np.pi/4,     0]]).T
        P4 = np.array([[ 2,     0,            0]]).T
        P5 = np.array([[ 2.5,   -np.pi/4,     0]]).T
        P6 = np.array([[ 3,     0,            0]]).T
        P7 = np.array([[ 3.5,   -np.pi/4,     0]]).T
        P8 = np.array([[ 4,     0,            0]]).T
        P9 = np.array([[ 4.5,   0,            0]]).T
        P10 = np.array([[5,     0,            0]]).T

        P11 = np.array([[ 5.5,   0,            0]]).T
        P12 = np.array([[ 6,     0,            0]]).T
        P13 = np.array([[ 6.5,   0,            0]]).T
        P14 = np.array([[ 7,     0,            0]]).T
        P15 = np.array([[ 7.5,   0,            0]]).T
        P16 = np.array([[ 8,     0,            0]]).T
        P17 = np.array([[ 8.5,   0,            0]]).T
        P18 = np.array([[ 9,     0,            0]]).T
        P19 = np.array([[ 9.5,   0,            0]]).T
        P20 = np.array([[ 10,    0,            0]]).T
        P21 = np.array([[ 11,    0,            0]]).T

        self.points_theta_x = [P0,  P1,  P2,  P3,  P4,  P5,  P6,  P7,  P8,  P9,  P10,
                               P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21]
        self.matrices_x = cv.matricesCRCurve(self.points_theta_x)
        self.times_theta_x  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                                5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]


    def set_points_theta_y(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,            0]]).T
        P1 = np.array([[ 0,     0,            0]]).T
        P2 = np.array([[ 1,     0,            0]]).T
        P3 = np.array([[ 1.5,   -np.pi/1.2,    0]]).T
        P4 = np.array([[ 2,     0,            0]]).T
        P5 = np.array([[ 2.5,   -np.pi/1.2,    0]]).T
        P6 = np.array([[ 3,     0,            0]]).T
        P7 = np.array([[ 3.5,   -np.pi/1.2,    0]]).T
        P8 = np.array([[ 4,     0,            0]]).T
        P9 = np.array([[ 4.5,   0,            0]]).T
        P10 = np.array([[5,     0,            0]]).T

        P11 = np.array([[ 5.5,   0,            0]]).T
        P12 = np.array([[ 6,     0,            0]]).T
        P13 = np.array([[ 6.5,   0,            0]]).T
        P14 = np.array([[ 7,     0,            0]]).T
        P15 = np.array([[ 7.5,   0,            0]]).T
        P16 = np.array([[ 8,     0,            0]]).T
        P17 = np.array([[ 8.5,   0,            0]]).T
        P18 = np.array([[ 9,     0,            0]]).T
        P19 = np.array([[ 9.5,   0,            0]]).T
        P20 = np.array([[ 10,    0,            0]]).T
        P21 = np.array([[ 11,    0,            0]]).T

        self.points_theta_y = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10,
                               P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21]
        self.matrices_y = cv.matricesCRCurve(self.points_theta_y)
        self.times_theta_y  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                                5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]


    def set_points_theta_z(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 10,   0,   0]]).T
        P3 = np.array([[ 11,     0,   0]]).T

        self.points_theta_z = [P0, P1, P2, P3]
        self.matrices_z = cv.matricesCRCurve(self.points_theta_z)
        self.times_theta_z  = [0, 10]


# Pie izquierdo
class LeftFootMovement(AbstractPart):

    def __init__(self):

        super().__init__()


    def set_points_theta_x(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,   0]]).T
        P1 = np.array([[ 0,     0,   0]]).T
        P2 = np.array([[ 10,   0,   0]]).T
        P3 = np.array([[ 11,     0,   0]]).T

        self.points_theta_x = [P0, P1, P2, P3]
        self.matrices_x = cv.matricesCRCurve(self.points_theta_x)
        self.times_theta_x  = [0, 10]


    def set_points_theta_y(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,            0]]).T
        P1 = np.array([[ 0,     0,            0]]).T
        P2 = np.array([[ 1,     0,   0]]).T
        P3 = np.array([[ 1.5,   np.pi/1.2,            0]]).T
        P4 = np.array([[ 2,     0,   0]]).T
        P5 = np.array([[ 2.5,   np.pi/1.2,            0]]).T
        P6 = np.array([[ 3,     0,   0]]).T
        P7 = np.array([[ 3.5,   np.pi/1.2,            0]]).T
        P8 = np.array([[ 4,     0,   0]]).T
        P9 = np.array([[ 4.5,   0,            0]]).T
        P10 = np.array([[5,     0,            0]]).T

        P11 = np.array([[ 5.5,   0,            0]]).T
        P12 = np.array([[ 6,     0,            0]]).T
        P13 = np.array([[ 6.5,   0,            0]]).T
        P14 = np.array([[ 7,     0,            0]]).T
        P15 = np.array([[ 7.5,   0,            0]]).T
        P16 = np.array([[ 8,     0,            0]]).T
        P17 = np.array([[ 8.5,   0,            0]]).T
        P18 = np.array([[ 9,     0,            0]]).T
        P19 = np.array([[ 9.5,   0,            0]]).T
        P20 = np.array([[ 10,    0,            0]]).T
        P21 = np.array([[ 11,    0,            0]]).T

        self.points_theta_y = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10,
                               P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21]
        self.matrices_y = cv.matricesCRCurve(self.points_theta_y)
        self.times_theta_y  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                                5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]


    def set_points_theta_z(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,            0]]).T
        P1 = np.array([[ 0,     0,            0]]).T
        P2 = np.array([[ 1,     0,            0]]).T
        P3 = np.array([[ 1.5,   np.pi/2,      0]]).T
        P4 = np.array([[ 2,     0,            0]]).T
        P5 = np.array([[ 2.5,   np.pi/2,      0]]).T
        P6 = np.array([[ 3,     0,            0]]).T
        P7 = np.array([[ 3.5,   np.pi/2,      0]]).T
        P8 = np.array([[ 4,     0,            0]]).T
        P9 = np.array([[ 4.5,   0,            0]]).T
        P10 = np.array([[5,     0,            0]]).T

        P11 = np.array([[ 5.5,   0,            0]]).T
        P12 = np.array([[ 6,     0,            0]]).T
        P13 = np.array([[ 6.5,   0,            0]]).T
        P14 = np.array([[ 7,     0,            0]]).T
        P15 = np.array([[ 7.5,   0,            0]]).T
        P16 = np.array([[ 8,     0,            0]]).T
        P17 = np.array([[ 8.5,   0,            0]]).T
        P18 = np.array([[ 9,     0,            0]]).T
        P19 = np.array([[ 9.5,   0,            0]]).T
        P20 = np.array([[ 10,    0,            0]]).T
        P21 = np.array([[ 11,    0,            0]]).T

        self.points_theta_z = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10,
                               P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21]
        self.matrices_z = cv.matricesCRCurve(self.points_theta_z)
        self.times_theta_z  = [0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                                5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]


class CompleteModel():
    def __init__(self):

        self.height = 0
        self.points = []
        self.matrices = []
        self.times = []
        self.curve = cv.evalCRCurveTime


    def set_points(self):

        # puntos mov brazo derecho en eje y
        P0 = np.array([[-1,     0,            0]]).T
        P1 = np.array([[ 0,     0,            0]]).T
        P2 = np.array([[ 1,     0,            0]]).T
        P3 = np.array([[ 1.25,   0.5,    0]]).T
        P4 = np.array([[ 1.5,   0,    0]]).T
        P5 = np.array([[ 1.75,   0.5,    0]]).T
        P6 = np.array([[ 2,     0,            0]]).T
        P7 = np.array([[ 2.25,   0.5,    0]]).T
        P8 = np.array([[ 2.5,   0,    0]]).T
        P9 = np.array([[ 2.75,   0.5,    0]]).T
        P10 = np.array([[ 3,     0,            0]]).T
        P11 = np.array([[ 3.25,   0.5,    0]]).T
        P12 = np.array([[ 3.5,   0,    0]]).T
        P13 = np.array([[ 3.75,   0.5,    0]]).T
        P14 = np.array([[ 4,     0,            0]]).T
        P15 = np.array([[ 4.25,   0,            0]]).T
        P16 = np.array([[ 4.5,   0,            0]]).T

        P17 = np.array([[ 4.75,     0,            0]]).T
        P18 = np.array([[ 5,     0,            0]]).T
        P19 = np.array([[ 5.25,   0.5,    0]]).T
        P20 = np.array([[ 5.5,   0,    0]]).T
        P21 = np.array([[ 5.75,   0.5,    0]]).T
        P22 = np.array([[ 6,     0,            0]]).T
        P23 = np.array([[ 6.25,   0.5,    0]]).T
        P24 = np.array([[ 6.5,   0,    0]]).T
        P25 = np.array([[ 6.75,   0.5,    0]]).T
        P26 = np.array([[ 7,     0,            0]]).T
        P27 = np.array([[ 7.25,   0.5,    0]]).T
        P28 = np.array([[ 7.5,   0,    0]]).T
        P29 = np.array([[ 7.75,   0.5,    0]]).T
        P30 = np.array([[ 8,     0,            0]]).T
        P31 = np.array([[ 8.25,   0.5,            0]]).T
        P32 = np.array([[ 8.5,   0,            0]]).T
        P33 = np.array([[ 8.75,     0.5,            0]]).T
        P34 = np.array([[ 9,   0,            0]]).T
        P35 = np.array([[ 9.25,   0.5,            0]]).T
        P36 = np.array([[ 9.5,   0,            0]]).T
        P37 = np.array([[ 9.75,   0.5,            0]]).T
        P38 = np.array([[ 10,   0,            0]]).T
        P39 = np.array([[ 11,     0,            0]]).T

        self.points = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20,
                       P21, P22, P23, P24, P25, P26, P27, P28, P29, P30, P31, P32, P33, P34, P35, P36, P37, P38, P39]
        self.matrices = cv.matricesCRCurve(self.points)
        self.times  = [0, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5,
                       5.25, 5.5, 5.75, 6, 6.25, 6.5, 6.75, 7, 7.25, 7.5, 7.75, 8, 8.25, 8.5, 8.75, 9,
                       9.25, 9.5, 9.75, 10]


    def update(self, t):
        self.height = self.curve(t, self.matrices, self.times)[1]


class CamMovement():
    def __init__(self):
        self.points = []

        self.pos = []

        self.times = []
        self.matrices = []
        self.curve = cv.evalCRCurveTime

    def set_points(self):
        z_translate = 0.35
        scale = 50
        P0 = np.array([[-0.3, -0.25, 0+z_translate]]).T*scale
        P1 = np.array([[-0.5, 0.25, 0.15+z_translate]]).T*scale
        P2 = np.array([[-0.15, 0.15, 0+z_translate]]).T*scale
        P3 = np.array([[0, 0.5, -0.15+z_translate]]).T*scale
        P4 = np.array([[0.15, 0.15, 0+z_translate]]).T*scale
        P5 = np.array([[0.4, 0.25, 0.15+z_translate]]).T*scale
        P6 = np.array([[0.15, -0.15, 0+z_translate]]).T*scale
        P7 = np.array([[0.4, -0.5, -0.15+z_translate]]).T*scale
        P8 = np.array([[0, -0.25, 0+z_translate]]).T*scale
        P9 = np.array([[-0.4, -0.5, 0.15+z_translate]]).T*scale
        P10 = np.array([[-0.25, -0.15, 0+z_translate]]).T*scale
        P11 = np.array([[-0.5, 0.25, 0.15+z_translate]]).T*scale
        P12 = np.array([[-0.15, 0.25, 0+z_translate]]).T*scale

        self.points = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12]
        self.matrices = cv.matricesCRCurve(self.points)
        self.times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


    def update(self, t):
        self.pos = self.curve(t, self.matrices, self.times).T[0]


class lightMovement():
    def __init__(self):
        self.points = []

        self.pos_z = []

        self.times = []
        self.matrices = []
        self.curve = cv.evalCRCurveTime


    def set_points(self):

        max_z = 6.0
        min_z = 1.0

        P0 = np.array([[-1,    max_z,       0]]).T
        P1 = np.array([[0,     max_z,       0]]).T
        P2 = np.array([[1,     min_z,      0]]).T
        P3 = np.array([[2,     max_z,       0]]).T
        P4 = np.array([[3,   max_z,       0]]).T

        self.points = [P0, P1, P2, P3, P4]
        self.matrices = cv.matricesCRCurve(self.points)
        self.times = [0, 1, 2]


    def update(self, t):
        self.pos_z = self.curve(t, self.matrices, self.times)[1]