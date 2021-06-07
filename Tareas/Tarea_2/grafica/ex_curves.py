# coding=utf-8
"""Hermite and Bezier curves using python, numpy and matplotlib"""

import numpy as np
#import matplotlib.pyplot as mpl
#from mpl_toolkits.mplot3d import Axes3D

__author__ = "Daniel Calderon"
__license__ = "MIT"


def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T


def hermiteMatrix(P1, P2, T1, T2):
    
    # Generate a matrix concatenating the columns
    G = np.concatenate((P1, P2, T1, T2), axis=1)
    
    # Hermite base matrix is a constant
    Mh = np.array([[1, 0, -3, 2], [0, 0, 3, -2], [0, 1, -2, 1], [0, 0, -1, 1]])    
    
    return np.matmul(G, Mh)


def bezierMatrix(P0, P1, P2, P3):
    
    # Generate a matrix concatenating the columns
    G = np.concatenate((P0, P1, P2, P3), axis=1)

    # Bezier base matrix is a constant
    Mb = np.array([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]])
    
    return np.matmul(G, Mb)


def catmullRomMatrix(P0, P1, P2, P3):
    # Generate a matrix concatenating the columns
    G = np.concatenate((P0, P1, P2, P3), axis=1)

    # Camull-Rom base matrix is a constant
    Mcr = 1/2*np.array([[0, -1, 2, -1], [2, 0, -5, 3], [0, 1, 4, -3], [0, 0, -1, 1]])

    return np.matmul(G, Mcr)    


def plotCurve(ax, curve, label, color=(0,0,1)):

    xs = curve[:, 0]
    ys = curve[:, 1]
    zs = curve[:, 2]

    ax.plot(xs, ys, zs, label=label, color=color)


# M is the cubic curve matrix, N is the number of samples between 0 and 1
def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)

    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)

    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T

    return curve

def evalCurveTime(M, t):
    T = generateT(t)
    curve_point = np.matmul(M, T)
    return curve_point


def matricesCRCurve(points):
    control_points = [points[0], points[len(points)-1]]
    matrices = []

    for i in range(len(points)-3):
        Mcr = catmullRomMatrix(points[i], points[i+1], points[i+2], points[i+3])
        matrices += [Mcr]
    return matrices


def evalCRCurveTime(t, points, times):
    matrices = matricesCRCurve(points)
    N_curves = len(matrices)
    curve_point = evalCurveTime(matrices[0], t)

    for i in range(1, N_curves):
        if times[i] <= t < times[i+1]:
            normalized_t = (t-times[i]) / (times[i+1]-times[i])
            curve_point = evalCurveTime(matrices[i], normalized_t)

    return curve_point

if __name__ == "__main__":

    # Number of samples to plot
    N = 100

    # Setting up the matplotlib display for 3D
    fig = mpl.figure()
    ax = fig.gca(projection='3d')

    """
    Example for Catmull-Rom curve
    """

    P0_prima = np.array([[-1, 0, 0]]).T
    P0 = np.array([[0, 0, 0]]).T
    P1 = np.array([[1, -np.pi/2, 0]]).T
    P2 = np.array([[2, np.pi/4, 0]]).T
    P3 = np.array([[3, -np.pi/2.2, 0]]).T
    P4 = np.array([[4, np.pi/2.2, 0]]).T
    P5 = np.array([[5, np.pi/4, 0]]).T
    P6 = np.array([[6, np.pi/4, 0]]).T

    
    points = [P0_prima, P0, P1, P2, P3, P4, P5, P6]
    matrices = matricesCRCurve(points)

    catmullRomCurve = np.ndarray(shape=(N, 3), dtype=float)
    ts = np.linspace(0.0, 5.0, N)

    for i in range(N):
        if 0<= ts[i] <= 1:
            T = generateT(ts[i])
            catmullRomCurve[i, 0:3] = np.matmul(matrices[0], T).T

        elif 1 <= ts[i] <= 2:
            T = generateT(ts[i]-1)
            catmullRomCurve[i, 0:3] = np.matmul(matrices[1], T).T
        
        elif 2 <= ts[i] <= 3:
            T = generateT(ts[i]-2)
            catmullRomCurve[i, 0:3] = np.matmul(matrices[2], T).T

        elif 3 <= ts[i] <= 4:
            T = generateT(ts[i]-3)
            catmullRomCurve[i, 0:3] = np.matmul(matrices[3], T).T

        elif 4 <= ts[i] <= 5:
            T = generateT(ts[i]-4)
            catmullRomCurve[i, 0:3] = np.matmul(matrices[4], T).T

    plotCurve(ax, catmullRomCurve, "Catmull-Rom curve")

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.legend()
    mpl.show()