import numpy as np
from PyGame3d.vector import Vector3

def create_lookAt (eye:Vector3,target:Vector3,up=Vector3(0,1,0)) -> np.ndarray :

    z_axis = (eye-target).normalized()
    x_axis = up.cross(z_axis).normalized()
    y_axis = z_axis.cross(x_axis)

    return np.array([
        [x_axis.x, x_axis.y, x_axis.z, -x_axis.dot(eye)],
        [y_axis.x, y_axis.y, y_axis.z, -y_axis.dot(eye)],
        [z_axis.x, z_axis.y, z_axis.z, -z_axis.dot(eye)],
        [0,         0,         0,          1.0]
    ], dtype='f4').T