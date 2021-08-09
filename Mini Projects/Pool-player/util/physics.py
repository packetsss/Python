import math
import numpy as np
from scipy.spatial.distance import cdist

def distance_between_two_points(p1, p2):
    dist_diff = p1 - p2
    return np.hypot(*dist_diff)

def point_in_rectangle(point, rect):
    x1, x2, y1, y2 = rect
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False

def inverse_angle(angle, calibrator=0):
    return (180 - angle) + calibrator

def get_center_from_pred(prediction):
    return np.array([int((prediction[0] + prediction[2]) / 2), int((prediction[1] + prediction[3]) / 2)])

def closest_node(node, nodes):
    dist = cdist([node], nodes)
    return nodes[dist.argmin()]

def general_line_eqtn(pt1, pt2):
    # Ax + By = C ::from:: y = mx + b
    (x1, y1), (x2, y2) = pt1, pt2
    a = y1 - y2
    b = x2 - x1
    c = (x1 - x2) * y1 + (y2 - y1) * x1
    return a, b, c

def check_collision(a, b, c, x, y, radius):
    # finding the distance of line from center.
    dist = ((abs(a * x + b * y + c)) /
            math.sqrt(a * a + b * b))
    
    return radius >= dist

def circle_line_segment_intersection(circle_center, circle_radius, pt1, pt2, full_line=True, tangent_tol=1e-9):
    """ Find the points at which a circle intersects a line-segment.  This can happen at 0, 1, or 2 points.

    :param circle_center: The (x, y) location of the circle center
    :param circle_radius: The radius of the circle
    :param pt1: The (x, y) location of the first point of the segment
    :param pt2: The (x, y) location of the second point of the segment
    :param full_line: True to find intersections along full line - not just in the segment.  False will just return intersections within the segment.
    :param tangent_tol: Numerical tolerance at which we decide the intersections are close enough to consider it a tangent
    :return Sequence[Tuple[float, float]]: A list of length 0, 1, or 2, where each element is a point at which the circle intercepts a line segment.
    """

    (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2)**.5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

    if discriminant < 0:  # No intersection between circle and line
        return None
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**.5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant**.5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
            fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
            intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
        if len(intersections) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
            return [intersections[0]]
        else:
            return intersections