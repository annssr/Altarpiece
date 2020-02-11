import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.restoration import denoise_tv_chambolle
from computeH import computeH
from scipy.spatial import ConvexHull
from getBoundingCorners import getBoundingCorners, getPointsBounding2Faces, get_points_3_faces
from verifyNumberOfFaces import getNumberOfFacesShowing

# filename = 'data/checkered_on_greenscreen_sideways-up_view.png'
# filename = 'data/checkered_on_greenscreen.png'
filename = 'data/blobs_on_greenscreen_corner_view.png'

img = cv2.imread(filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
num_corners = 100
dst = cv2.goodFeaturesToTrack(gray, num_corners, 0.01, 10)
dst = np.int0(dst)

blue = img[:,:,0]
img[:,:,0] = img[:,:,2]
img[:,:,2] = blue

# Uncomment to see the corners
# for corner in dst:
#     x,y = corner.ravel()
#     cv2.circle(img,(x,y), 10, [0,255,0], -1)

corners = np.array([corner.ravel() for corner in dst])

hull = ConvexHull(corners)
# for simplex in hull.simplices:
#     first_corner = tuple(corners[simplex, 0].tolist())
#     second_corner = tuple(corners[simplex, 1].tolist())
#     if first_corner in points_dict:
#         points_dict[first_corner].append(second_corner)
#     else:
#         points_dict[first_corner] = [second_corner]
#
#     if second_corner in points_dict:
#         points_dict[second_corner].append(first_corner)
#     else:
#         points_dict[second_corner] = [first_corner]
#
#     plt.plot(first_corner, second_corner, 'k-', c='r')
# plt.show()
# print(points_dict)

points = getBoundingCorners(hull, corners)

faces, orientation = getNumberOfFacesShowing(points)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return np.array([x, y])

if faces == 2:
    face1, face2 = getPointsBounding2Faces(points, orientation)

    mapping_points = np.array([[0,0], [0, 200], [200, 0], [200, 200] ])
    H = computeH(np.array(face1), mapping_points)

    new_img = cv2.warpPerspective(img, H, (200, 200))

    H_2 = computeH(np.array(face2), mapping_points)
    new_img_2 = cv2.warpPerspective(img, H, dsize=(200, 200))

    extracted_texture_img = np.zeros((200, 400, 3))

    for i in range(extracted_texture_img.shape[0]):
        for j in range(extracted_texture_img.shape[1]):
            if j >= 200:
                extracted_texture_img[i, j] = new_img_2[i, j - 200]
            else:
                extracted_texture_img[i, j] = new_img[i, j]

    extracted_texture_img /= 255.0
    plt.title("Extracted Texture")
    plt.imshow(extracted_texture_img)
    plt.show()

    plt.title("Face 1")
    plt.imshow(new_img)
    plt.show()

    plt.title("Face 2")
    plt.imshow(new_img_2)
    plt.show()


    plt.imshow(img)
    for x in face1:
        plt.plot(x[0], x[1], 'ro')
    for x in face2:
        plt.plot(x[0], x[1], 'bo')
else:
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    I = get_points_3_faces(points)
    top, top_right, bottom_right, bottom, bottom_left, top_left = np.array(points)[np.array(I, dtype=np.int32)]
    
    v1 = top_left - bottom_left
    v2 = top_right - bottom_right
    v_up = (v1 + v2) / 2

    v1 = top_left - top
    v2 = bottom - bottom_right
    v_left = (v1 + v2) / 2

    v1 = top_right - top
    v2 = bottom - bottom_left
    v_right = (v1 + v2) / 2

    center1 = line_intersection((top_right, top_right + v_left), (bottom, bottom + v_up))
    center2 = line_intersection((top_right, top_right + v_left), (top_left, top_left + v_right))
    center3 = line_intersection((top_left, top_left + v_right), (bottom, bottom + v_up))
    center = (center1 + center2 + center3) / 3

    plt.imshow(img)
    for i in range(len(I)):
        plt.plot(*points[I[i]], colors[i] + 'o')
    plt.plot(*center1, 'ko')
    plt.plot(*center2, 'ko')
    plt.plot(*center3, 'ko')
    plt.plot(*center, 'ko')

plt.title(str(faces) + " Faces")
plt.show()
