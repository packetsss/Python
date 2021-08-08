from .settings import *

import math
import numpy as np
from scipy.spatial.distance import cdist

def distance_between_two_points(p1, p2):
    dist_diff = p1 - p2
    return np.hypot(*dist_diff)

def inverse_angle(angle, calibrator=0):
    return (180 - angle) + calibrator

def get_center_from_pred(prediction):
    return (int((prediction[0] + prediction[2]) / 2), int((prediction[1] + prediction[3]) / 2))

def closest_node(node, nodes):
    dist = cdist([node], nodes)
    print(dist.min())
    return nodes[dist.argmin()]