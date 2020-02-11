import numpy as np


def getAngleBetween(a, b, c):
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)

def line_angle(a, b):
    return getAngleBetween(a, a + np.array([1, 0]), b)

def getBoundingCorners(hull, corners):
    max_angle_colinear = 2

    l = len(hull.vertices)

    angles = [(np.array(corners[hull.vertices[i]]), \
                getAngleBetween(np.array(corners[hull.vertices[i]]), \
                np.array(corners[hull.vertices[(i-1)%l]]), \
                np.array(corners[hull.vertices[(i+1)%l]])))
                    for i in range(l)]

    angles.sort(key=lambda x: x[1], reverse=True)

    points = [x[0] for x in angles[:6]]

    return points


def distBetween(point, point2):
    return np.power((point[0] - point2[0]), 2) + np.power((point[1] - point2[1]), 2)

def getPointsBounding2Faces(points, orientation):
    if orientation == 'X':
        points = sorted(points, key=lambda point: point[1])
        face1 = points[0:4]
        face2 = points[2:]
    else:
        points = sorted(points, key=lambda point: point[0])
        face1 = points[0:4]
        face2 = points[2:]
    return face1, face2

def angle_dif(a, b):
    return min((a - b) % 360, (b - a) % 360)

def get_points_3_faces_general(points):
    edges = [(i, j) for i in range(len(points)) for j in range(i)]
    angles = [line_angle(points[i], points[j]) for (i, j) in edges]
    diffs = [(i, j, edges[i], edges[j], angle_dif(angles[i], angles[j])) for i in range(len(angles)) for j in range(i)]
    diffs.sort(key=lambda x: x[4])
    print(diffs)
    edge_pair1 = diffs[0]
    edge_pair2 = diffs[1]
    print(angles[0], angles[1])
    print(edge_pair1, edge_pair2)

def get_points_3_faces(points):
    points = np.array(points)

    bottom = np.argmax(points[:,1])
    top = np.argmin(points[:,1])

    left0, left1 = np.argsort(points[:,0])[:2]
    if points[left0, 1] <= points[left1, 1]:
        top_left = left0
        bottom_left = left1
    else:
        top_left = left1
        bottom_left = left0

    right0, right1 = np.argsort(points[:,0])[-2:]
    if points[right0, 1] <= points[right1, 1]:
        top_right = right0
        bottom_right = right1
    else:
        top_right = right1
        bottom_right = right0

    return top, top_right, bottom_right, bottom, bottom_left, top_left