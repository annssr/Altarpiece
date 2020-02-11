
def getNumberOfFacesShowing(points):
    x_points = []
    y_points = []

    for point in points:
        x_points.append(point[0])
        y_points.append(point[1])

    x_aligned = isPointsAligned(x_points)
    y_aligned = isPointsAligned(y_points)

    if x_aligned:
        return 2, 'X'
    elif y_aligned:
        return 2, 'Y'
    else:
        return 3, None

def isPointsAligned(points):
    points = sorted(points)
    group1 = points[:3]
    group2 = points[3:]

    return verifyGroup(group1) and verifyGroup(group2)


def verifyGroup(group):
    return abs(group[0] - group[1]) < 50 and abs(group[1] - group[2]) < 50
