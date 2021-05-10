# coding=utf-8
"""Transformation matrices for computer graphics"""

import numpy as np

__author__ = "Daniel Calderon"
__license__ = "MIT"

def identity():
    return np.identity(4, dtype=np.float32)


def uniformScale(s):
    return np.array([
        [s,0,0,0],
        [0,s,0,0],
        [0,0,s,0],
        [0,0,0,1]], dtype = np.float32)


def scale(sx, sy, sz):
    return np.array([
        [sx,0,0,0],
        [0,sy,0,0],
        [0,0,sz,0],
        [0,0,0,1]], dtype = np.float32)


def rotationX(theta):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [1,0,0,0],
        [0,cos_theta,-sin_theta,0],
        [0,sin_theta,cos_theta,0],
        [0,0,0,1]], dtype = np.float32)


def rotationY(theta):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [cos_theta,0,sin_theta,0],
        [0,1,0,0],
        [-sin_theta,0,cos_theta,0],
        [0,0,0,1]], dtype = np.float32)


def rotationZ(theta):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [cos_theta,-sin_theta,0,0],
        [sin_theta,cos_theta,0,0],
        [0,0,1,0],
        [0,0,0,1]], dtype = np.float32)


def rotationA(theta, axis):
    s = np.sin(theta)
    c = np.cos(theta)

    assert axis.shape == (3,)

    x = axis[0]
    y = axis[1]
    z = axis[2]

    return np.array([
        # First row
        [c + (1 - c) * x * x,
        (1 - c) * x * y - s * z,
        (1 - c) * x * z + s * y,
        0],
        # Second row
        [(1 - c) * x * y + s * z,
        c + (1 - c) * y * y,
        (1 - c) * y * z - s * x,
        0],
        # Third row
        [(1 - c) * x * z - s * y,
        (1 - c) * y * z + s * x,
        c + (1 - c) * z * z,
        0],
        # Fourth row
        [0,0,0,1]], dtype = np.float32)


def translate(tx, ty, tz):
    return np.array([
        [1,0,0,tx],
        [0,1,0,ty],
        [0,0,1,tz],
        [0,0,0,1]], dtype = np.float32)


def shearing(xy, yx, xz, zx, yz, zy):
    return np.array([
        [ 1, xy, xz, 0],
        [yx,  1, yz, 0],
        [zx, zy,  1, 0],
        [ 0,  0,  0, 1]], dtype = np.float32)


def matmul(mats):
    out = mats[0]
    for i in range(1, len(mats)):
        out = np.matmul(out, mats[i])

    return out
