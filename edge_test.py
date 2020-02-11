import cv2
import numpy as np
import imageio
import matplotlib.pyplot as plt
from skimage.restoration import denoise_tv_chambolle

filename = 'data/checkered_on_greenscreen.png'
img = imageio.imread(filename)
R = np.sqrt(img.shape[0]**2 + img.shape[1]**2)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

edges = cv2.Canny(gray, 15, 200)

n = 100
lines = cv2.HoughLines(edges, 2, 2 * np.pi / n, 75)
lines = lines[:,0,:]
theta_threshold = 1 * np.pi / n

def rot(P):
	return np.array([-P[1], P[0]])

def polar_to_cart(rho, theta):
	a = np.cos(theta)
	b = np.sin(theta)
	cx = rho * a
	cy = rho * b
	x0 = cx - b
	y0 = cy + a
	P0 = np.array([x0, y0])
	V = np.array([b, -a])
	V /= np.linalg.norm(V)
	return P0, V

def line_dist(rho1, theta1, rho2, theta2):
	theta = (theta1 + theta2) / 2.0
	P0, _ = polar_to_cart(rho1, theta1)
	Q0, _ = polar_to_cart(rho2, theta2)
	_, V = polar_to_cart(rho1, theta)
	t = np.dot(Q0 - P0, rot(V)) / np.dot(rot(V), rot(V))
	return abs(t) * np.linalg.norm(rot(V))


parallel = {i: [j for j in range(lines.shape[0]) if i != j and abs(lines[i][1] - lines[j][1]) <= theta_threshold] for i in range(lines.shape[0])}
furthest = {}

for i in parallel:
	max_j = -1
	max_dist = 0
	for j in parallel[i]:
		dist = line_dist(*lines[i], *lines[j])
		if max_j == -1 or dist > max_dist:
			max_j = j
			max_dist = dist
	furthest[i] = j

fig, (ax0, ax1) = plt.subplots(1, 2)

ax0.imshow(gray, cmap='gray')
ax0.set_title('Original Image')
ax0.set_xticks([])
ax0.set_yticks([])

for i in range(lines.shape[0]):
	rho, theta = lines[i]
	P0, V = polar_to_cart(rho, theta)
	A = P0 + 2*R*V
	B = P0 - 2*R*V
	ax0.plot([A[0], B[0]], [A[1], B[1]], c='r')

ax1.imshow(edges, cmap='gray')
ax1.set_title('Edge Image')
ax1.set_xticks([])
ax1.set_yticks([])

plt.show()
